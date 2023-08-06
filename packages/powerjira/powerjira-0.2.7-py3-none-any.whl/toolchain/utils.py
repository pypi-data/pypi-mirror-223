# stdlib
from os import path
from pathlib import Path
from typing import List, Dict, Union
from sys import argv, exit, getsizeof
from subprocess import call, check_output
from json import dumps
# 3rd party
try:
  from yaml import safe_load, YAMLError
  from jira import Issue
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


#───Utils────────────────────
def print_issue(issue:Issue, domain:str, new:bool, epic:bool, raw:bool=False) -> None:
  '''prints essential issue info'''
  if raw:
    print(dumps(issue.raw, sort_keys=True, indent=2))
  else:
    borderTailLength = 20
    if new:
      print(f"\n───NEW {issue.fields.issuetype.name.upper()}{'─'*(borderTailLength - len(issue.fields.issuetype.name))}")
    else:
      print(f"\n───EXISTING {issue.fields.issuetype.name.upper()}{'─'*(borderTailLength - len(issue.fields.issuetype.name) - 5)}")
    print(f"Key      │ {issue.key}")
    print(f"Url      │ {domain}/browse/{issue.key}")
    print(f"Type     │ {issue.fields.issuetype.name}")
    print(f"Created  │ {issue.fields.created}")
    print(f"Status   │ {issue.fields.status}")
    print(f"Priority │ {issue.fields.priority}")
    print(f"\n───GIT COMMANDS{'─'*(borderTailLength - 8)}")
    print(f"git checkout -b [feature|bugfix]/{issue.key}_<name-of-feature>")
    print(f"git push origin [feature|bugfix]/{issue.key}_<name-of-feature> -o merge_request.create -o merge_request.target=<parent-branch>")
    if epic:
      print(f"Ticket created under parent: {issue.fields.parent.key}")
    print(f"\nOVERVIEW:\n{issue.fields.reporter} --> {issue.fields.assignee}")
    print(f"───Summary\n{issue.fields.summary}")
    print(f"───Description\n{issue.fields.description}\n")
  return
