
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="search-youtube-url",
    version="1.0.0",
    packages=find_packages(),
    py_modules=['search_youtube_url'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'search_youtube_url = search_youtube_url:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
