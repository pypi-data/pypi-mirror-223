#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='django-debug-toolbar-user-panel',
    description="Panel for the Django Debug toolbar to quickly switch between "
        "users.",
    version='2.0.0',
    url='https://chris-lamb.co.uk/projects/django-debug-toolbar-user-panel',

    author="Chris Lamb",
    author_email="chris@chris-lamb.co.uk",
    license='BSD',

    packages=(
        'debug_toolbar_user_panel',
    ),
    package_data={'': [
        'templates/debug_toolbar_user_panel/*',
    ]},
)
