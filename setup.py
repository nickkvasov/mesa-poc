#!/usr/bin/env python3
"""
Setup script for LLM Tourism Simulation System
==============================================

This script allows the package to be installed via pip and distributed
through standard Python package management tools.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "LLM-enhanced tourism simulation system for policy testing and analysis."

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        'mesa>=3.0.0',
        'pandas>=1.3.0', 
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0'
    ]

setup(
    name='llm-tourism-sim',
    version='1.0.0',
    author='LLM Tourism Simulation Team',
    author_email='contact@llm-tourism-sim.org',
    description='LLM-enhanced agent-based tourism simulation for policy testing',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/llm-tourism-sim/llm-tourism-sim',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Researchers',
        'Intended Audience :: Policy Makers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Office/Business :: Tourism',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=3.0',
            'black>=22.0',
            'flake8>=4.0',
            'mypy>=0.900'
        ],
        'docs': [
            'sphinx>=4.0',
            'sphinx-rtd-theme>=1.0'
        ],
        'examples': [
            'jupyter>=1.0',
            'ipykernel>=6.0'
        ]
    },
    entry_points={
        'console_scripts': [
            'tourism-sim=llm_tourism_sim.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'llm_tourism_sim': [
            'data/*.json',
            'data/*.csv'
        ],
    },
    zip_safe=False,
    keywords=[
        'tourism', 'simulation', 'agent-based-modeling', 'policy-testing',
        'large-language-models', 'urban-planning', 'mesa', 'scenarios'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/llm-tourism-sim/llm-tourism-sim/issues',
        'Source': 'https://github.com/llm-tourism-sim/llm-tourism-sim',
        'Documentation': 'https://llm-tourism-sim.readthedocs.io/',
    },
)
