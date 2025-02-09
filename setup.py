import os
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='heartbeat',
    version='1.0.0',
    description='Insanely simple health-check library in python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ausaaf Nabi',
    author_email='nabiausaaf@gmail.com',
    url='https://github.com/ausaafnabi/heartbeat',
    packages=find_packages(),
    # install_requires=[
    #     'urllib'
    # ],
    entry_points={
        'console_scripts': [
            'heartbeat=heartbeat.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPL v2.0',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='health check heartbeat',
    project_urls={
        'Documentation': 'https://github.com/ausaafnabi/heartbeat',
        'Source Code': 'https://github.com/ausaafnabi/heartbeat',
        'Issue Tracker': 'https://github.com/ausaafnabi/heartbeat/issues',
    },
    python_requires='>=3.6',
    tests_require=['pytest'],
    setup_requires=['pytest-runner']
)