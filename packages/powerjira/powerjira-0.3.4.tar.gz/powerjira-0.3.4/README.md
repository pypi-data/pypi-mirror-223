# **PowerJira**
*A succinct local jira control plane.*

<br />

## **Welcome to PowerJira!**
Hate how visually noise and clunky the Jira web-app is? Ever wish you could manage your jira account with a minimalistic interface?

Welcome to the party! 🥳

<br />

### **Table of Contents** 📖
<hr>

  - [Welcome](#welcome-to-powerjira)
  - [**Get Started**](#get-started-)
  - [Usage](#usage-)
  - [Technologies](#technologies-)
  - [Contribute](#Contribute-)
  - [Acknowledgements](#acknowledgements-)
  - [License/Stats/Author](#license-stats-author-)

<br />

## **Get Started 🚀**
<hr>

```sh
pip install powerjira
pip install --upgrade powerjira
```

<br />

## **Usage ⚙**
<hr>

Set an alias in your shell environment to open up an editor workspace you want to use powerjira in. \
Then set another alias to run a script like:
```python
# pip install powerjira
# pip install --upgrade powerjira

from powerjira import powerjira
from sys import argv, exit

config_path      = 'config.yml'
agent_path       = 'agent.yml'
summary_path     = 'summary.txt'
description_path = 'description.txt'

powerjira(
  config_path,
  agent_path,
  summary_path,
  description_path,
  argv[1:]
)
exit(0)
```

Make your local config files:
```sh
touch summary.txt description.txt config.yml agent.yml
```

For the configuration files:
**config.yml**
```yaml
project  : <project-key>
priority : <priority>

issue_type : <type>
epicKey    : # Leave as empty for standalone task or epic

reporter : <reporter-account-id>
assignee : <assignee-account-id>
```
**agent.yml**
```yaml
domain: <host>

user_name: <email>
token: <jira-access-token>
```

Presuming you've named said shell alias `pj`, print the help message:
```sh
pj --help
```

<br />

## **Technologies 🧰**
<hr>

  - [PyYAML](https://pypi.org/project/PyYAML/)
  - [python-jira](https://pypi.org/project/jira/)
  - [Poetry](https://python-poetry.org/)
  - [Typer](https://typer.tiangolo.com/)

<br />

## **Contribute 🤝**
<hr>

Feel free to push PR's to help make this tool more extensible/flexible.

<br />

## **Acknowledgements 💙**
<hr>

Thanks to Atlassian for making market-leading tools that kinda frustrate me.

<br />

## **License, Stats, Author 📜**
<hr>

<img align="right" alt="example image tag" src="https://i.imgur.com/jtNwEWu.png" width="200" />

<!-- badge cluster -->

![PyPI](https://img.shields.io/pypi/v/powerjira)
![GitHub repo size](https://img.shields.io/github/repo-size/anthonybench/powerjira)

<!-- / -->
See [License](LICENSE) for the full license text.

This repository was authored by *Isaac Yep*. \
[PyPi Package](https://pypi.org/project/powerjira/#table-of-contents)

[Back to Table of Contents](#table-of-contents-)