# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pandas>=1.2.4,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'schedule>=1.1.0,<2.0.0',
 'yagmail>=0.14.256,<0.15.0']

entry_points = \
{'console_scripts': ['factli = factli.factli:cli']}

setup_kwargs = {
    'name': 'factli',
    'version': '0.2.0',
    'description': 'A Facebook Crowdtangle Client',
    'long_description': '# DBoeS-stats\nCollectors of reputation metrics of public speakers in social media platforms \n\n### About\n\nThe Facebook directory-\n\n1. extracts posts of accounts and creates individual folders containing JSON response for every account (get_posts.py). \n2. extracts content from CrowdTangle and creates CSV files containing the statistics of facebook pages (get_list.py). \n\n### Storing API Access Token \n\nStore your API access token in a python file, name it Access_Token.py and save it in the DBoeS-stats directory.\nIn the file store the access token as:\n```\naccess_token = "API access token generated from your crowd tangle account"\n```\n## Installation\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Clone repository\n3. In the directory run `poetry install`\n4. Run `poetry shell` to start development virtualenv\n5. Run `factli`.\n\n### Cloning this Repo\n\nTo clone this repository type:\n\n```\ngit clone https://github.com/Leibniz-HBI/DBoeS-stats.git\n```\n### Usage\n```\nusage: factli [OPTIONS]\n\nOptions:\n  --list_id TEXT       Saved List ID\n  --count INTEGER      Number of posts returned per call, maximum 100,\n                       defaults to 10\n  --access_token TEXT  Your unique access token\n  --start_date TEXT    Start Date (older), Format=YYYY-MM-DD, if not given\n                       defaults to NULL\n  --end_date TEXT      End Date(newer), Format=YYYY-MM-DD, if not given\n                       defaults to current date\n  --time_frame TEXT    The interval of time to consider from the endDate. Any\n                       valid SQL interval, eg: "1 HOUR" or "30 MINUTE"\n  --log_level TEXT     Level of output detail (DEBUG, INFO, WARNING, ERROR).\n                       Warnings and Errors are               always logged in\n                       respective log-files `errors.log` and `warnings.log`.\n                       Default: ERROR\n  --log_file TEXT      Path to logfile. Defaults to standard output.\n  --sched TEXT         If given, waits "sched" hour(s) and then repeats.\n  --notify TEXT        If given, notify email address in case of unexpected\n                       errors. Needs further setup. See README.\n  --path TEXT          If given, stores the output at the desired location\n                       (Absolute Path needed)\n  --help               Show this message and exit.\n```\nEmail notifications with the `-n` argument use [yagmail](https://pypi.org/project/yagmail/).\n## Output\n\nOutput of get_posts.py stores the raw JSON response in the following folder structure:\n\n\n`Facebook/results/list_id/account_id/start-date_end-date.json`\n\nAn example of the JSON data can be viewed [here](https://github.com/CrowdTangle/API/wiki/Posts).\n\n## Ensure that factli is continuously running, even after restart\nIf your system can run cronjobs, stop twacapic, run `crontab -e` and add the following to your crontab:\n\n```cron\n30 6 * * *    sh -c "cd PATH/TO/YOUR/DBoeS-stats/WORKING/DIRECTORY && PATH/TO/Poetry-env run factli [YOUR ARGUMENTS HERE]" >> out.txt 2>&1\n```\n\nThis will start collection at 0630Hr (GMT) everyday. \n',
    'author': 'Aditya Kumar',
    'author_email': 'a.kumar@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/DBoeS-stats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
