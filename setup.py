from setuptools import setup
import os

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
version = open(FILE_DIR + '/pybot/etc/VERSION').read().strip()

setup(name='pybot',
      version=version,
      description='A python bot for Telegram',
      url='https://github.com/daanbeverdam/pybot',
      author='Daan Beverdam')
