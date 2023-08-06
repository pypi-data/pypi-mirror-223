# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leanforge',
 'leanforge.lean_canvas',
 'leanforge.lean_canvas.forms',
 'leanforge.lean_canvas.migrations',
 'leanforge.lean_canvas.models',
 'leanforge.lean_canvas.views',
 'leanforge.leanforge']

package_data = \
{'': ['*'],
 'leanforge.lean_canvas': ['templates/*',
                           'templates/lean_canvas/*',
                           'templates/partials/*']}

setup_kwargs = {
    'name': 'leanforge',
    'version': '0.1.0',
    'description': 'LeanForge is a Django package that helps businesses create and refine Lean Canvas Business Plans. With LeanForge, you can easily shape and mold your business strategies using lean methodology principles. It provides a comprehensive set of tools, models, and templates to seamlessly integrate Lean Canvas functionality into your Django projects. Simplify your business planning process, drive continuous improvement, and forge a path to success with LeanForge.',
    'long_description': None,
    'author': 'Ali Tavallaie',
    'author_email': 'a.tavallaie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
