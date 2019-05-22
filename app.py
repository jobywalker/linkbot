"""Flask app that listens on / and processes slack events and commands."""
import logconfig
from flask import Flask, request, jsonify, abort
import slack
import os
import time
import hmac
import hashlib
import json.decoder
import requests
from functools import partial
from threading import Thread
from queue import Queue
from linkbot import bots, RequestLogger


app = Flask(__name__)
app.config.from_pyfile(os.environ['APP_CONFIG'])
SLACK_SECRET = app.config['SLACK_SIGNING_SECRET']
LINKBOTS = []
for bot in app.config['LINKBOTS']:
    LINKBOTS.append(getattr(bots, bot.get('LINK_CLASS', 'LinkBot'))(bot))
if not LINKBOTS:
    raise Exception('no linkbots defined')
SLACK_CLIENT = slack.WebClient(app.config['SLACK_BOT_TOKEN'])
WEBHOOK_CLIENT = RequestLogger()


@app.route('/', methods=['GET', 'POST'])
def handle_message():
    """A single endpoint handling both events and commands."""
    if request.method == 'GET':
        return jsonify(success=True)  # to pass a health check

    verify_slack_signature()
    if not request.is_json:
        # treat it as a command
        response_url = request.form['response_url']
        text = request.form['text']
        MessageProcessor.queue.put(partial(process_command, text, response_url))
        return jsonify(response_type='in_channel')
    json = request.get_json()
    if 'challenge' in json:
        # This is how Slack verifies our URL to receive events.
        return jsonify(challenge=json['challenge'])
    event = json['event']
    if event['type'] != 'message':
        app.logger.error(f'discarding unhandled event type {event["type"]}')
    if 'bot_id' in event or event.get('subtype') == 'bot_message':
        return '', 200

    text, channel = event['text'], event['channel']
    MessageProcessor.queue.put(partial(process_event, text, channel))
    return '', 200


def verify_slack_signature():
    """
    Verify a slack signature according to
    https://api.slack.com/docs/verifying-requests-from-slack
    """
    if app.debug:
        return
    timestamp = request.headers['X-Slack-Request-Timestamp']
    signature = request.headers['X-Slack-Signature']
    if time.time() - int(timestamp) > 5 * 60:
        app.logger.error('Stale command request.')
        abort(403)
    compstr = f'v0:{timestamp}:'.encode() + request.get_data()
    rhash = hmac.new(SLACK_SECRET.encode(), compstr, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(f'v0={rhash}', signature):
        app.logger.error('Invalid X-Slack-Signature')
        abort(403)


class MessageProcessor(Thread):
    queue = Queue()

    def run(self):
        """Pull messages off the queue and process them."""
        while True:
            func = self.queue.get()
            try:
                func()
            except Exception as e:
                app.logger.exception(e)
            self.queue.task_done()


def process_event(text, channel):
    """Process events by posting matches to the provided channel."""
    for message in links_from_text(text):
        SLACK_CLIENT.chat_postMessage(text=message, channel=channel)


def process_command(text, response_url):
    """Process a slack command by posting a response to the provided url."""
    text = '\n'.join(links_from_text(text))
    if text:
        data = dict(text=text, response_type='in_channel')
        WEBHOOK_CLIENT.post(response_url, json=data)


def links_from_text(text):
    """Search for matches and post any to the original channel."""
    for bot in LINKBOTS:
        for match in bot.match(text):
            app.logger.info(f'{match} match!')
            try:
                yield bot.message(match)
            except Exception as e:
                app.logger.error(e)
                continue


for _ in range(4):
    MessageProcessor().start()
