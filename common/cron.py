# -*- coding: utf-8 -*-
"""
  :synopsis: module containing cron jobs for common app.

.. module: common.cron
.. author: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from importlib import import_module

from background_task.models import Task
from background_task.tasks import tasks as task_manager

TASKS = {
    'common.utils.email': 'send_email'
}


def process_background_tasks():
    """Discover and run background tasks in the common app."""
    for path, func in TASKS.items():
        import_module(path)

        pending_tasks = Task.objects.filter(task_name='.'.join([path, func]))

        for task in pending_tasks:
            task_manager.run_task(task)
