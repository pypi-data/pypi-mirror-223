# stdlib
from os import path
from pathlib import Path
from typing import List, Dict, Union
from sys import argv, exit, getsizeof
from subprocess import call, check_output
# custom
from utils import *
# 3rd party
try:
  from yaml import safe_load, YAMLError
  from jira import JIRA
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


#───Commands─────────────────
def make_logic(
    config_path:str, agent_path:str, summary_path:str, description_path:str
  ) -> None:
  '''read external files, assemble jira ticket, publishes and prints summary'''

  with open(summary_path, 'r') as summary, open(description_path, 'r') as description, open(config_path, 'r') as raw_config, open(agent_path, 'r') as raw_agent:
    ## load config
    try:
      summary     = summary.read()
      description = description.read()
      config      = safe_load(raw_config)
      project     = config['project']
      priority    = config['priority']
      epicKey     = config['epicKey']
      issueType   = config['issueType']
      reporter    = config['reporter']
      assignee    = config['assignee']
      agent       = safe_load(raw_agent)
      domain      = agent['domain']
      userName    = agent['userName']
      token       = agent['token']
      if (epicKey) and (issueType.lower() == 'epic'):
        print(f"Incompatible config values - can't attach epic to epic.")
        exit(1)
    except Exception as e:
      print(f"Config error.\n{e}")
      exit(1)
    ## authenticate
    try:
      jira = JIRA(server=domain, basic_auth=(userName, token))
    except Exception as e:
      print(f'Authentication error.\n{e}')
      exit(1)
    ## build
    task_issue_blueprint = {
      'project'    : {'key': project},
      'summary'    : summary,
      'description': description,
      'issuetype'  : {'name': issueType},
      'priority'   : {'name': priority},
      'reporter'   : {'accountId': reporter},
      'assignee'   : {'accountId': assignee},
    }
    epic_issue_blueprint = {
      'project'    : {'key': project},
      'summary'    : summary,
      'description': description,
      'issuetype'  : {'name': issueType},
      'reporter'   : {'accountId': reporter},
      'assignee'   : {'accountId': assignee},
    }
    ## publish
    try:
      if issueType.lower() == 'task':
        if epicKey:
          task_issue_blueprint['parent'] = {'key': epicKey}
        newIssue = jira.create_issue(fields=task_issue_blueprint)
        print_issue(issue=newIssue, new=True, epic=False)
        exit(0)
      elif issueType.lower() == 'epic':
        newIssue = jira.create_issue(fields=epic_issue_blueprint)
        print_issue(issue=newIssue, domain=domain, new=True, epic=True)
        exit(0)
      else:
        print(f'Error unsupported issue type.')
        exit(1)
    except Exception as e:
      print(f'Ticket publishing error.\n{e}')

  return


def fetch_logic(
    agent_path:str, fetch_key:str, raw:bool=False
  ) -> str:
  '''takes ticket key to search for, prints summary if found'''
  with open(agent_path, 'r') as raw_agent:
    ## load config
    try:
      agent    = safe_load(raw_agent)
      domain   = agent['domain']
      userName = agent['userName']
      token    = agent['token']
    except Exception as e:
      print(f"Config error.\n{e}")
      exit(1)
    ## authenticate
    try:
      jira = JIRA(server=domain, basic_auth=(userName, token))
    except Exception as e:
      print(f"Authentication error.\n{e}")
      exit(1)
    ## fetch
    issue = jira.issue(fetch_key)
    print_issue(issue=issue, domain=domain, new=False, epic=False, raw=raw)
  return
