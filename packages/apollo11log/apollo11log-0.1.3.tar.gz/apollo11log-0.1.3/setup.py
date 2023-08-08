# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apollo11log']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['apollo11log = apollo11log:__main__.main']}

setup_kwargs = {
    'name': 'apollo11log',
    'version': '0.1.3',
    'description': 'Prints Apollo 11 Logs is realtime',
    'long_description': "### Install\n```sh\nsudo pip3 install apollo11log #to install system wide\n```\n\n### Run as a CLI app\n```\n$ apollo11log\n[CDR] 00 00:00:04 Roger. Clock.\n[CDR] 00 00:00:13 Roger. We got a roll program.\n[CMP] 00 00:00:15 Roger. Roll.\n[CDR] 00 00:00:34 Roll's complete an\n```\n\n### Run as a systemd service\n\nCreate a unit file - such as `/etc/systemd/system/apollo11.service`\nwith the contents like\n```\n[Unit]\nDescription=apollo11\nAfter=syslog.target\n\n[Service]\nExecStart=/usr/local/bin/apollo11log\nRestart=always\nRestartSec=120\nSyslogIdentifier=apollo11\n\n[Install]\nWantedBy=multi-user.target\n```\n\nThe enable and start the service\n```\nsudo systemctl enable apollo11.service\nsudo systemctl start apollo11.service\n```\n\n### Watch the logs\n```\njournalctl -u apollo11 -f -n\n```",
    'author': 'xss',
    'author_email': 'michaela@michaela.lgbt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xssfox/apollo11log',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
