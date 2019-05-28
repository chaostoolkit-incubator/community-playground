# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.types import Activity, Configuration, Experiment, Hypothesis, \
    Journal, Run, Secrets
from chaoslib.exceptions import InterruptExecution
import click
from logzero import logger

__all__ = ["before_activity_control"]


def before_activity_control(context: Activity, **kwargs):
    """
    Prompt for Yes or No to executing an activity.
    """
    logger.info("About to execute activity: " + context.get("name"))
    if click.confirm('Do you want to continue?'):
        logger.info("Continuing: " + context.get("name"))
    else:
        raise InterruptExecution("Experiment manually interrupted")
