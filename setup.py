# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 15:50:17 2015

@author: closedloop
"""

from setuptools import setup
import datetime
cur_year = datetime.datetime.today().year

setup(name='financial_planner',
      version=open('VERSION').read(),
      description='Financial Planning Calculations by Astrocyte Research',
      url='https://github.com/AstrocyteResearch/financial-planner',
      author='Sean Kruzel - Astrocyte Research',
      author_email='support@astrocyte.io',
      license='Astrocyte Research - Copyright 2015-{} - All rights reserved'.format(cur_year),
      packages=[
        'financial_planner'
      ],
      install_requires=[],
      include_package_data=True,
      long_description=open('README.md').read(),
      zip_safe=False)
