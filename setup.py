from setuptools import setup

install_requires = ['beautifulsoup4',
                    'slackclient',
                    'requests',
                    'Flask',
                    'gunicorn[eventlet]']

tests_require = ['pytest', 'pytest-flake8']

setup(name='linkbot',
      install_requires=install_requires,
      tests_require=tests_require,
      description='slackbot listening for mentions of jira issues, etc')
