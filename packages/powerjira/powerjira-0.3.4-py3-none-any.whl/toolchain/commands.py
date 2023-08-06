# stdlib
from os import path
from pathlib import Path
from typing import List, Dict, Union
from sys import argv, exit, getsizeof
from subprocess import call, check_output
from pprint import pprint
# custom
from toolchain.utils import *
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
      issue_type  = config['issue_type']
      reporter    = config['reporter']
      assignee    = config['assignee']
      agent       = safe_load(raw_agent)
      domain      = agent['domain']
      user_name   = agent['user_name']
      token       = agent['token']
      if (epicKey) and (issue_type.lower() == 'epic'):
        print(f"Incompatible config values - can't attach epic to epic.")
        exit(1)
    except Exception as e:
      print(f"Config error.\n{e}")
      exit(1)
    ## authenticate
    try:
      jira = JIRA(server=domain, basic_auth=(user_name, token))
    except Exception as e:
      print(f'Authentication error.\n{e}')
      exit(1)
    ## build
    task_issue_blueprint = {
      'project'    : {'key': project},
      'summary'    : summary,
      'description': description,
      'issuetype'  : {'name': issue_type},
      'priority'   : {'name': priority},
      'reporter'   : {'accountId': reporter},
      'assignee'   : {'accountId': assignee},
    }
    epic_issue_blueprint = {
      'project'    : {'key': project},
      'summary'    : summary,
      'description': description,
      'issuetype'  : {'name': issue_type},
      'reporter'   : {'accountId': reporter},
      'assignee'   : {'accountId': assignee},
    }
    ## publish
    try:
      if issue_type.lower() == 'task':
        if epicKey:
          task_issue_blueprint['parent'] = {'key': epicKey}
        newIssue = jira.create_issue(fields=task_issue_blueprint)
        print_issue(issue=newIssue, domain=domain, new=True, epic=False)
        exit(0)
      elif issue_type.lower() == 'epic':
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
    fetch_key:str, agent_path:str, raw:bool=False
  ) -> str:
  '''takes ticket key to search for, prints summary if found'''
  with open(agent_path, 'r') as raw_agent:
    ## load config
    try:
      agent     = safe_load(raw_agent)
      domain    = agent['domain']
      user_name = agent['user_name']
      token     = agent['token']
    except Exception as e:
      print(f"Config error.\n{e}")
      exit(1)
    ## authenticate
    try:
      jira = JIRA(server=domain, basic_auth=(user_name, token))
    except Exception as e:
      print(f"Authentication error.\n{e}")
      exit(1)
    ## fetch
    issue = jira.issue(fetch_key)
    print_issue(issue=issue, domain=domain, new=False, epic=False, raw=raw)
  return

def prune_watched_logic(
  agent_path:str
) -> None:
  '''stops watching all watched issues of status DONE, prints list of pruned issues'''
  with open(agent_path, 'r') as raw_agent:
    ## load config
    try:
      agent     = safe_load(raw_agent)
      domain    = agent['domain']
      user_name = agent['user_name']
      token     = agent['token']
    except Exception as e:
      print(f"Config error.\n{e}")
      exit(1)
    ## authenticate
    try:
      jira = JIRA(server=domain, basic_auth=(user_name, token))
    except Exception as e:
      print(f"Authentication error.\n{e}")
      exit(1)
    ## prune
    watched_issues = jira.search_issues('watcher = currentUser() AND resolution = Done')
    for issue in watched_issues:
      jira.remove_watcher(issue.key, user_name)
      print(f'- stopped watching {issue.key}')
  return
