#!/usr/bin/env python

'''README
Usage:
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
    argv[1:])
  exit(0)
'''

# stdlib
from os import path
from pathlib import Path
from typing import List, Dict, Union
from sys import argv, exit, getsizeof
from subprocess import call, check_output
# custom
from toolchain.commands import make_logic, fetch_logic, prune_watched_logic
# 3rd party
try:
  import typer
  from yaml import safe_load, YAMLError
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


def powerjira(config_path:str, agent_path:str, summary_path:str, description_path:str, raw:bool=False, fetch_key:str='') -> None:
  app = typer.Typer()

  @app.command()
  def make(
    config_path:str=config_path, agent_path:str=agent_path, summary_path:str=summary_path, description_path:str=description_path
  ) -> None:
    '''Create Ticket

    Create a jira ticket, only `task` and `epic` types are supported.

    ───Params
    config_path:str :: path to config file for build spec
    agent_path:str :: path to creds file
    summary_path:str :: path to text file containing ticket title (jira calls it the summary)
    description_path:str :: path to text file containing ticket description
    '''
    return make_logic(config_path, agent_path, summary_path, description_path)
  
  @app.command()
  def fetch(
    fetch_key:str, agent_path:str=agent_path, raw:bool=False
  ) -> None:
    '''Fetch ticket

    Print a jira ticket, same output as `make` command.

    ───Params
    fetch_key:str :: issue key to search for
    agent_path:str :: path to creds file
    raw:bool :: whether to print raw json dump
    '''
    return fetch_logic(fetch_key, agent_path, raw)
  
  @app.command()
  def prune_watched(
    agent_path:str=agent_path
  ) -> None:
    '''Prune Watched Issues

    Stop watching all watched issues with status DONE.

    ───Params
    agent_path:str :: path to creds file
    '''
    return prune_watched_logic(agent_path)
  
  if (__name__ == "powerjira") or (__name__ == '__main__'):
    app()


## Local Testing
# powerjira(argv)
