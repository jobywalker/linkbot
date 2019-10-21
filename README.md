# linkbot
Slackbot to bind message fragments to external links

Linkbot can run anywhere. To get it running, just create its configuration module, `linkconfig.py`, and supply
the following module variables:

### Example `linkconfig.py`

    API_TOKEN='_API_Token_generated_from_your_Slack_instance_'
    UW_SAML_CREDENTIALS = ('_low-privilege-username_', '_password_')
    SERVICE_NOW_CREDENTIALS = ('_api-account_', '_api-key_')
    LINKBOTS = [
        {
            'LINK_CLASS': 'JiraLinkBot',
            'HOST': 'https://jira.example.com',
            'AUTH': UW_SAML_CREDENTIALS
        },
        {
            'LINK_CLASS': 'ServiceNowBot',
            'HOST': 'https://XXXX.service-now.com',
            'AUTH': SERVICE_NOW_CREDENTIALS
        }
    ]

See [Slack Help](https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens) for guidance on generating the value for API_TOKEN

The LINKBOTS list can be any number of dicts supplying, minimally, a `MATCH` and `LINK` key.

`MATCH` is a regular expression that defines what to look for in Slack messages.

`LINK` provides the link and link text linkbot uses in its response.  The format
consists of a link and link text enclosed in angle brackets and separated by the pipe character as in the example above.  Two 
instances of print format characters, %s, are used by linkbot to insert the matched text in the SLACK message in the first, and 
a randomly selected quip in the second.

It's a pretty simple little script.  Pull requests are welcome!


## Setting up the app in Slack

* Create a new app at https://api.slack.com/apps
* Add the app to your workspace
* Grab the Signing Secret (under general) and the Bot User OAuth Access Token (under OAuth) and add them to your secrets. These are the only slack secrets your app requires.
* Enable events, using as your Request URL the url of your newly-running app.
  * Subscribe to all bot events starting with `message.` (`message.im`, `message.groups`, `message.channels`,   `message.mpim`) and save your changes.
* (Optional) Add a slack command, using the same URL that you used earlier. This allows people to use it in DMs and channels where linkbot isn't a member. It'll ask to reinstall the app. Do it.
