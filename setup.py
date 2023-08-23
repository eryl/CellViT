# coding: utf-8

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='cellvit',
      version='0.1',
      description='CellViT',
      url='git@git.github.com/TIO-IKIM/CellViT',
      author='Fabian Hörst',
      author_email='fabian.hoerst@uk-essen.de',
      license='Apache 2.0 with Commons Clause',
      packages=['cellvit'],
      install_requires=[],
      dependency_links=[],
      zip_safe=False)
