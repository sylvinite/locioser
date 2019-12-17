#!/usr/bin/env python

import click
import pytest

from microSALT import __version__

from click.testing import CliRunner
from unittest.mock import patch

from microSALT import config, logger
from microSALT.cli import root

#DEBUG: This code is only a base. Meaningful assertions need to be implemented

@pytest.fixture
def runner():
  runnah = CliRunner()
  return runnah

def test_version(runner):
  res = runner.invoke(root, '--version')
  assert res.exit_code == 0
  assert __version__ in res.stdout

@patch('microSALT.store.lims_fetcher.Lims.check_version')
def test_groups(check_version, runner):
  """These groups should only return the help text"""
  base = runner.invoke(root, ['analyse'])
  assert base.exit_code == 0
  base = runner.invoke(root, ['utils'])
  assert base.exit_code == 0
  base_invoke = runner.invoke(root, ['utils', 'resync'])
  assert base_invoke.exit_code == 0
  base_invoke = runner.invoke(root, ['utils', 'refer'])
  assert base_invoke.exit_code == 0

@patch('microSALT.store.lims_fetcher.Lims.check_version')
def test_analyse(check_version, runner):
  #All subcommands
  for analysis_type in ['sample', 'project', 'collection']:
    base_invoke = runner.invoke(root, ['analyse', analysis_type])
    assert base_invoke.exit_code == 2

    #Exhaustive parameter test
    typical_run = runner.invoke(root, ['analyse', analysis_type, 'AAA1234', '--input', '/tmp/', '--config', '/tmp/', '--email', '2@2.com'])
    dry_run = runner.invoke(root, ['analyse', analysis_type, 'AAA1234', '--dry'])
    special_run = runner.invoke(root, ['analyse', analysis_type, 'AAA1234', '--qc_only', '--skip_update', '--untrimmed', '--uncareful'])

#TODO: Figure out how to force quit this function
#def test_view(runner):
#  view = runner.invoke(root, ['utils', 'view'])
#  assert view.exit_code == 0

@patch('microSALT.store.lims_fetcher.Lims.check_version')
def test_finish(check_version, runner):
  #All subcommands
  for analysis_type in ['sample', 'project', 'collection']:
    base_invoke = runner.invoke(root, ['utils', 'finish', analysis_type])
    assert base_invoke.exit_code == 2

    #Exhaustive parameter test
    typical_run = runner.invoke(root, ['utils', 'finish', analysis_type, '--email', '2@2.com', '--input', '/tmp/', '--config', '/tmp/', '--report', 'default'])
    special_run = runner.invoke(root, ['utils', 'finish', analysis_type, '--rerun', '--report', 'qc'])
    if analysis_type == 'collection':
      unique_report = runner.invoke(root, ['utils', 'finish', analysis_type, '--report', 'motif_overview'])

@patch('microSALT.store.lims_fetcher.Lims.check_version')
def test_report(check_version, runner):
  base_invoke = runner.invoke(root, ['utils', 'report'])
  assert base_invoke.exit_code == 2

  #Exhaustive parameter test
  for rep_type in ['default','typing','motif_overview','qc','json_dump','st_update']:
    report = '--type {}'.format(rep_type)
    normal_report = runner.invoke(root, ['utils', 'report', 'AAA1234', report, '--email', '2@2.com', '--output', '/tmp/'])
    collection_report = runner.invoke(root, ['utils', 'report', 'AAA1234', report, '--collection'])

@patch('microSALT.store.lims_fetcher.Lims.check_version')
def test_resync(check_version, runner):
  runner.invoke(root, ['utils', 'resync', 'overwrite', 'AAA1234A1'])
  runner.invoke(root, ['utils', 'resync', 'overwrite', 'AAA1234A1', '--force'])

  #Exhaustive parameter test
  for rep_type in ['list', 'report']:
    report = '--type {}'.format(rep_type)
    typical_work = runner.invoke(root, ['utils', 'resync', 'review', '--email 2@2.com', report])
    delimited_work = runner.invoke(root, ['utils', 'resync', 'review', '--skip_update', '--customer', 'custX', report])

@patch('microSALT.store.lims_fetcher.Lims.check_version')
def test_refer(check_version, runner):
  list_invoke = runner.invoke(root, ['utils', 'refer', 'list'])
  assert list_invoke.exit_code == 0

  runner.invoke(root, ['utils', 'refer', 'add', 'Homosapiens_Trams'])
  runner.invoke(root, ['utils', 'refer', 'add', 'Homosapiens_Trams', '--force'])