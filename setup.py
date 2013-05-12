#!/usr/bin/env python

from distutils.core import setup


setup(name='semrush',
      version='0.1',
      description='A client for the SEMRush API',
      author='Tom Linton',
      author_email='tom@brownshoe.co.nz',
      url='http://tomlinton.io',
      packages=['semrush'],
      requires=['requests']
)
