# -*- coding: utf-8 -*-
"""
  :synopsis: code quality module for coverage checking.

.. module:: quality.management.commands.coverage
.. author:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
import os
import shutil
import subprocess
import sys

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.encoding import force_text

from common.utils.collect_apps import collect_project_apps
from common.utils.terminal import Terminal


class Command(BaseCommand):
    """Run code quality checker for coverage."""

    PYTHON_PATH = os.path.dirname(sys.executable)

    OMIT = [
        '*/tests/*',
        '*/migrations/*',
        '*/urls.py',
        '*/urls.py',
        '*/urls/*',
        '*/wsgi.py',
        '*/settings/*',
        '*/management/*',
        '*/fixtures/*',
        '*/imageuploader/utils/backend/exif.py*',
        '*.venv/*'
    ]

    help = 'Coverage runner - check unit test coverage.'

    def __init__(self, *args, **kwargs):
        """Initialise the coverage runner."""
        super(Command, self).__init__(*args, **kwargs)
        self.apps = collect_project_apps()

    def add_arguments(self, parser):
        """
        Parse the arguments supplied or use defaults.

        :param parser: the command parser
        :type parser: argparse.Namespace
        """
        parser.add_argument(
            '-a',
            '--apps',
            dest='apps',
            nargs='*',
            default=self.apps,
            choices=self.apps,
            help='specify which apps to run lint on (default: all apps)'
        )
        parser.add_argument(
            '-o',
            '--output',
            dest='output',
            default='stdout',
            choices=['html', 'stdout'],
            help='specify whether to print results to terminal '
                 'or output html files to quality/_coverage/'
        )

    def construct_command(self, options):
        """
        Build the coverage command.

        :param options: command arguments
        :type options: dict
        :return: the coverage command
        :rtype: list
        """
        apps = ','.join(options['apps'])
        rcfile = os.path.join(settings.PROJECT_DIR, 'quality/.coveragerc')
        coverage = [
            f'{self.PYTHON_PATH}/coverage',
            'run',
            f'--rcfile={rcfile}',
            f'--source={apps}',
            'manage.py',
            'test',
            '--noinput',
            '--verbosity=2'
        ]
        return coverage

    def output_stdout(self):
        """Output the coverage report to the terminal."""
        try:
            results = subprocess.check_output([
                f'{self.PYTHON_PATH}/coverage',
                'report'
            ])
        except subprocess.CalledProcessError as exc:
            Terminal.error(force_text(exc.output))
            return

        Terminal.success('\nCoverage Report\n')
        for line in force_text(results).split('\n'):
            Terminal.standard(line)

    def output_html(self):
        """Output the coverage HTML report to quality/_coverage."""
        directory = 'quality/_coverage/'
        path = os.path.abspath(os.path.join(settings.PROJECT_DIR, directory))

        try:
            shutil.rmtree(path)
        except OSError:
            pass

        os.makedirs(path)
        try:
            subprocess.check_output([
                '{}/coverage'.format(self.PYTHON_PATH),
                'html',
                '-d',
                directory
            ])
        except subprocess.CalledProcessError as exc:
            Terminal.error(force_text(exc.output))
            return

        Terminal.success(f'Outputted HTML report to: {directory}')

    def handle(self, *args, **options):
        """Execute the coverage runner using the provided command line args."""
        command = self.construct_command(options)
        output = options['output']

        try:
            subprocess.check_call(command)

        except subprocess.CalledProcessError as exc:
            Terminal.error(force_text(exc.output))
            return

        output_handler = getattr(self, f'output_{output}')
        output_handler()
