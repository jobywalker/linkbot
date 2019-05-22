from setuptools import setup

install_requires = ['beautifulsoup4',
                    'slackclient',
                    'jira',
                    'requests',
                    'Flask',
                    'gunicorn[eventlet]']

setup(name='linkbot',
      install_requires=install_requires,
      description='slackbot listening for mentions of jira issues, etc')
