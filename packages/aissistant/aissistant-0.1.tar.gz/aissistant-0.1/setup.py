from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='aissistant',
    version=0.1,
    packages=find_packages(),
    install_requires=[
        'sentence-transformers',
        'numpy',
        'faiss-gpu'
    ],
    extras_require={
        'gpu': ['faiss-gpu'],
        'cpu': ['faiss-cpu'],
    },
    entry_points={
        'console_scripts': [
            'aissistant=aissistant.cli:main',
        ],
    },
    author='Marko Manninen',
    url='https://github.com/markomanninen/aissistant',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="""Aissistant v0.1

Initialization prompt for persistent conversation vector database and personal profile in ChatGPT using Noteable plugin and aissistant module written by Marko T. Manninen (https://github.com/markomanninen/aissistant/)

Get creative and productive with this initialization script in ChatGPT that utilizes the Noteable plugin. Natively, you can create, edit, and run code and generate data within notebooks as well as in ChatGPT interchangeably, back and forth. By using this initialization prompt, you can use the combined environment to store data and explore past conversations, as well as manage profile information for a more intelligent chat and coding experience.

Copyright © 08/2023
""",
    long_description=long_description,
    long_description_content_type='text/markdown',
)
