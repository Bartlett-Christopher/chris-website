# -*- coding: utf-8 -*-
"""
   :synopsis: utility function to collect a set of this projects apps.

.. module:: common.utils.collect_apps
.. author:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
from django.apps import apps
from django.conf import settings


def collect_project_apps():
    """
    Gather all project apps into a set.

    :return: set of project apps
    :rtype: set
    """
    all_apps = set()
    for app in apps.get_app_configs():
        if app.path.startswith(settings.PROJECT_DIR):
            all_apps.add(app.name)

    return all_apps
