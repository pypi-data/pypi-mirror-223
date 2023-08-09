from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discord-ext-interaction',
    version='0.6.1',
    url='https://github.com/gunyu1019/discord-extension-interaction',
    author='gunyu1019',
    description='Framework for Application Commands built on discord.py',
    license='MIT',
    author_email='gunyu1019@yhs.kr',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[],
    install_requires=['Discord-Extension-Interaction>=0.6.0'],
)
