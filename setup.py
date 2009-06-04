from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='lqn',
      version=version,
      description="Liquidity Network Code",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Liquidity Network Technical Team',
      author_email='liquiditynetwork@feasta.org',
      url='http://theliquiditynetwork.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
