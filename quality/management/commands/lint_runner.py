# -*- coding: utf-8 -*-
"""
   :synopsis: code quality module for lint checking.

.. module:: quality.lint_runner
.. moduleauthor:: Chris Bartlett <chris.bartlett@therealbuzzgroup.com>
"""
import os
import re
import subprocess
import sys

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.encoding import force_text

from common.utils.terminal import Terminal


class LintIssue(object):
    """Process lint runner errors."""

    REGEX_FLAKE8 = re.compile(
        r'(?P<module>[^:]+):(?P<line>\d+):(?P<col>\d+):' +
        r'\s*(?P<code>\w+)\s+(?P<msg>.*)'
    )

    REGEX_PYDOCSTYLE = re.compile(
        r'(?P<module>.+):(?P<line>\d+)\s+(?P<class>.+):\s+'
        r'(?P<code>[a-zA-Z]\d+):\s+(?P<msg>.*)'
    )

    REGEX_PYLINT = re.compile(
        r'(?P<module>.+[.py]):(?P<line>\d+):(?P<col>\d+):\s+'
        r'(?P<code>[A-Z]\d+):\s+(?P<msg>.*)'
    )

    FLAKE8_TYPE_MAP = {
        'F': 'error',
        'E': 'standards',
        'W': 'standards',
    }

    PYDOCSTYLE_TYPE_MAP = {
        '1': 'missing',
        '2': 'whitespace',
        '3': 'quote',
        '4': 'content',
    }

    PYLINT_TYPE_MAP = {
        'F': 'error',
        'E': 'error',
        'W': 'warning',
        'C': 'standards',
        'R': 'refactor',
        'I': 'info',
    }

    SEVERITY = {
        'error': 5,
        'warning': 4,
        'standards': 3,
        'refactor': 2,
        'info': 1,
    }
    SEVERITY_THRESHOLD = 1

    @classmethod
    def from_flake8(cls, issue):
        """
        Return a LintIssue from flake8.

        :param issue: the flake8 issue output
        :type issue: re.MatchObject
        :return: lint issue
        :rtype: quality.lint.LintIssue
        """
        code = issue.group('code')
        return LintIssue(
            module=issue.group('module'),
            line=issue.group('line'),
            col=issue.group('col'),
            code=code,
            message=issue.group('msg'),
            src='pyflakes' if code.startswith('F') else 'pep8',
            type_=cls.FLAKE8_TYPE_MAP.get(code[:1].upper(), 'unknown')
        )

    @classmethod
    def from_pydocstyle(cls, issue):
        """
        Return a LintIssue from pydocstyle.

        :param issue: the pydocstyle issue output
        :type issue: re.MatchObject
        :return: lint issue
        :rtype: quality.lint.LintIssue
        """
        code = issue.group('code')
        return LintIssue(
            module=issue.group('module'),
            line=issue.group('line'),
            col='',
            code=code,
            message=issue.group('msg'),
            src='pydocstyle',
            type_=cls.PYDOCSTYLE_TYPE_MAP.get(code[1], 'unknown')
        )

    @classmethod
    def from_pylint(cls, issue):
        """
        Return a LintIssue from pylint.

        :param issue: the pylint issue output
        :type issue: re.MatchObject
        :return: lint issue
        :rtype: quality.lint.LintIssue
        """
        code = issue.group('code')
        return LintIssue(
            module=issue.group('module'),
            line=issue.group('line'),
            col=issue.group('col'),
            code=code,
            message=issue.group('msg'),
            src='pylint',
            type_=cls.PYLINT_TYPE_MAP.get(code[0], 'unknown')
        )

    def __init__(self, module, line, col, code, message, src, type_):
        """Lint runner Issue."""
        super(LintIssue, self).__init__()
        self.module = module
        self.line = line
        self.col = col
        self.code = code
        self.message = message
        self.src = src
        self.type_ = type_

    def __str__(self):
        """Lint issue string representation."""
        return f'{self.src} [{self.code}] > {self.module} ' \
               f'(line {self.line}) > {self.message}'

    def __repr__(self):
        """Lint issue representation."""
        return f'{self.__class__.__name__}(' \
               f'module={self.module}, ' \
               f'line={self.line}, ' \
               f'col={self.col}, ' \
               f'message={self.message}, ' \
               f'src={self.src}, ' \
               f'type_={self.type_}' \
               f')'

    @property
    def ok(self):
        """
        Return if the Issue is below the threshold severity.

        :return: issue OK or not
        :rtype: bool
        """
        return self.SEVERITY.get(self.type_, 10) <= self.SEVERITY_THRESHOLD


class Command(BaseCommand):
    """Run code quality checkers for lint."""

    TERMINAL_PADDING = 10
    PROJECT_DIR = os.path.abspath(os.path.join(__file__, '../../'))
    PYTHON_PATH = os.path.dirname(sys.executable)

    ALL_LINTERS = ['flake8', 'pydocstyle', 'pylint']

    PYLINT_IGNORE = ['migrations', 'urls']

    help = 'Lint runner - a code quality checker.'

    def __init__(self, *args, **kwargs):
        """Initialise the lint runner."""
        super(Command, self).__init__(*args, **kwargs)
        self.result = None
        self.apps = self.collect_project_apps()

    @staticmethod
    def collect_project_apps():
        """
        Gather all importable project apps into set.

        :return: set of importable project apps
        :rtype: set
        """
        all_apps = set()
        for app in apps.get_app_configs():
            if app.path.startswith(settings.PROJECT_DIR):
                all_apps.add(app.name)

        return all_apps

    def add_arguments(self, parser):
        """
        Parse the arguments supplied or use defaults.

        :return: the command arguments
        :rtype: argparse.Namespace
        """
        parser.add_argument(
            '-l',
            '--linters',
            dest='linters',
            action='store',
            nargs='*',
            default=self.ALL_LINTERS,
            choices=self.ALL_LINTERS,
            help='specify which linter to run (default: all linters)'.format(
                linters=', '.join(self.ALL_LINTERS)
            )
        )
        parser.add_argument(
            '-a',
            '--apps',
            dest='apps',
            nargs='*',
            default=self.apps,
            choices=self.apps,
            help='specify which apps to run lint on (default: all apps)'
        )

    def construct_commands(self, options):
        """
        Iterate through each linter and construct the corresponding command.

        :return: list of commands to run linters
        :rtype: list
        """
        commands = []
        for lint_cleaner in options['linters']:
            construct_command = getattr(
                self,
                f'construct_{lint_cleaner}_command',
                None
            )
            if callable(construct_command):
                commands.append(construct_command())

        return commands

    def construct_flake8_command(self):
        """
        Build the flake8 command.

        :return: flake8 command
        :rtype: list
        """
        flake8 = [
            f"{self.PYTHON_PATH}/flake8",
            "--exclude=migrations",
            "<app placeholder>"
        ]
        return 'flake8', flake8

    def construct_pydocstyle_command(self):
        """
        Build the pydocstyle command.

        :return: pydocstyle command
        :rtype: list
        """
        pydocstyle = [
            f"{self.PYTHON_PATH}/pydocstyle",
            "<app placeholder>"
        ]
        return 'pydocstyle', pydocstyle

    def construct_pylint_command(self):
        """
        Build the pylint command.

        :return: pylint command
        :rtype: list
        """
        rcfile = os.path.join(settings.PROJECT_DIR, 'quality/.pylintrc')
        pylint = [
            f"{self.PYTHON_PATH}/pylint",
            '--load-plugins', 'pylint_django',
            f"--ignore={','.join(self.PYLINT_IGNORE)}",
            '--score=n',  # hide score display
            '--jobs=0',  # optimise number of processors
            f'--rcfile={rcfile}',
            "<app placeholder>"
        ]
        return 'pylint', pylint

    def handle(self, *args, **options):
        """Execute the lint runner using the provided command line args."""
        commands = self.construct_commands(options)
        summary = {}
        for app in sorted(options['apps']):
            ok = True
            issues = []

            for linter, command in commands:
                command[-1] = app
                try:
                    subprocess.check_output(command, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    regex = getattr(LintIssue, f'regex_{linter}'.upper())
                    handler = getattr(LintIssue, f'from_{linter}')

                    for line in regex.finditer(force_text(e.output)):
                        issue = handler(line)
                        if issue and not issue.ok:
                            ok = False
                            issues.append(issue)

            summary[app] = {
                'ok': ok,
                'issues': issues
            }

        title = '          Results          '
        max_padding = len(title) - 6
        Terminal.info(title)
        Terminal.info('-' * len(title))

        for app, data in summary.items():
            padding = ' ' * (max_padding - len(app))

            if data['ok']:
                Terminal.success(
                    app + padding + 'PASSED',
                    style=Terminal.Style.BOLD
                )
            else:
                Terminal.error(
                    app + padding + 'FAILED',
                    style=Terminal.Style.BOLD
                )
                for issue in data['issues']:
                    Terminal.error(' - ' + str(issue))
