"""LinkBot Configuration"""
import os
get = os.environ.__getitem__  # bomb out if unset

SLACK_SIGNING_SECRET = get('SLACK_SIGNING_SECRET')
SLACK_BOT_TOKEN = get('SLACK_BOT_TOKEN')
LINKBOTS = []

if os.environ.get('SERVICE_NOW_PASSWORD'):
    LINKBOTS.append({
        'LINK_CLASS': 'ServiceNowBot',
        'HOST': get('SERVICE_NOW_HOST'),
        'AUTH': (get('SERVICE_NOW_USER'), get('SERVICE_NOW_PASSWORD')),
        'QUIPS': []
    })

if os.environ.get('UW_SAML_PASSWORD'):
    LINKBOTS.append({
        'LINK_CLASS': 'JiraLinkBot',
        'HOST': get('JIRA_HOST'),
        'AUTH': (get('UW_SAML_USER'), get('UW_SAML_PASSWORD')),
        'QUIPS': []
    })

