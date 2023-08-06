# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['powerjira', 'commands', 'utils']
install_requires = \
['PyYAML>=6.0,<7.0', 'jira>=3.4.1,<4.0.0', 'typer>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'powerjira',
    'version': '0.3.4',
    'description': 'A succinct, minimal local jira control plane that can live in your text editor. Interface with tickets fast!',
    'long_description': '# **PowerJira**\n*A succinct local jira control plane.*\n\n<br />\n\n## **Welcome to PowerJira!**\nHate how visually noise and clunky the Jira web-app is? Ever wish you could manage your jira account with a minimalistic interface?\n\nWelcome to the party! 🥳\n\n<br />\n\n### **Table of Contents** 📖\n<hr>\n\n  - [Welcome](#welcome-to-powerjira)\n  - [**Get Started**](#get-started-)\n  - [Usage](#usage-)\n  - [Technologies](#technologies-)\n  - [Contribute](#Contribute-)\n  - [Acknowledgements](#acknowledgements-)\n  - [License/Stats/Author](#license-stats-author-)\n\n<br />\n\n## **Get Started 🚀**\n<hr>\n\n```sh\npip install powerjira\npip install --upgrade powerjira\n```\n\n<br />\n\n## **Usage ⚙**\n<hr>\n\nSet an alias in your shell environment to open up an editor workspace you want to use powerjira in. \\\nThen set another alias to run a script like:\n```python\n# pip install powerjira\n# pip install --upgrade powerjira\n\nfrom powerjira import powerjira\nfrom sys import argv, exit\n\nconfig_path      = \'config.yml\'\nagent_path       = \'agent.yml\'\nsummary_path     = \'summary.txt\'\ndescription_path = \'description.txt\'\n\npowerjira(\n  config_path,\n  agent_path,\n  summary_path,\n  description_path,\n  argv[1:]\n)\nexit(0)\n```\n\nMake your local config files:\n```sh\ntouch summary.txt description.txt config.yml agent.yml\n```\n\nFor the configuration files:\n**config.yml**\n```yaml\nproject  : <project-key>\npriority : <priority>\n\nissue_type : <type>\nepicKey    : # Leave as empty for standalone task or epic\n\nreporter : <reporter-account-id>\nassignee : <assignee-account-id>\n```\n**agent.yml**\n```yaml\ndomain: <host>\n\nuser_name: <email>\ntoken: <jira-access-token>\n```\n\nPresuming you\'ve named said shell alias `pj`, print the help message:\n```sh\npj --help\n```\n\n<br />\n\n## **Technologies 🧰**\n<hr>\n\n  - [PyYAML](https://pypi.org/project/PyYAML/)\n  - [python-jira](https://pypi.org/project/jira/)\n  - [Poetry](https://python-poetry.org/)\n  - [Typer](https://typer.tiangolo.com/)\n\n<br />\n\n## **Contribute 🤝**\n<hr>\n\nFeel free to push PR\'s to help make this tool more extensible/flexible.\n\n<br />\n\n## **Acknowledgements 💙**\n<hr>\n\nThanks to Atlassian for making market-leading tools that kinda frustrate me.\n\n<br />\n\n## **License, Stats, Author 📜**\n<hr>\n\n<img align="right" alt="example image tag" src="https://i.imgur.com/jtNwEWu.png" width="200" />\n\n<!-- badge cluster -->\n\n![PyPI](https://img.shields.io/pypi/v/powerjira)\n![GitHub repo size](https://img.shields.io/github/repo-size/anthonybench/powerjira)\n\n<!-- / -->\nSee [License](LICENSE) for the full license text.\n\nThis repository was authored by *Isaac Yep*. \\\n[PyPi Package](https://pypi.org/project/powerjira/#table-of-contents)\n\n[Back to Table of Contents](#table-of-contents-)',
    'author': 'sleepyboy',
    'author_email': 'anthonybenchyep@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/anthonybench/powerjira',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
