# -*- coding: utf-8 -*-
from setuptools import setup
import os

packages = ['vulcansql']
entry_points = {'console_scripts': ['vulcan = vulcansql.cli:run_vulcan']}

# read the contents of your README file
directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, "PUBLIC_README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup_kwargs = {
    'name': 'vulcan-sql',
    'version': '0.8.0',
    'description': 'VulcanSQL turns your SQL templates into data APIs for efficient data sharing. No backend skills required. Empower your data sharing, faster.',
    'long_description': long_description,
    'long_description_content_type': "text/markdown",
    'author': 'Canner Team',
    'author_email': 'contact@cannerdata.com',
    'license': "Apache 2.0",
    'url': 'https://github.com/Canner/vulcan-sql',
    'packages': packages,
    # Set include_package_data to True to add files from MANIFEST.in. to make old python version could find the vulcan executable file.
    'include_package_data': True,
    'entry_points': entry_points,
    'python_requires': '>=3.0.0',
}


setup(**setup_kwargs)

