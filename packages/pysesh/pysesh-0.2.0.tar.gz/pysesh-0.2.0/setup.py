from setuptools import setup, find_packages

setup(
    name='pysesh',
    version='0.2.0',
    description='A Python Session Manager and Multiplexer, allowing you to manage multiple sessions and their respective states, and switch between them with ease.',
    author='Connor Etherington',
    author_email='connor@concise.cc',
    packages=find_packages(),
    install_requires=[
        'colr',
        'argparse',
        'rich',
        'inquirer',
    ],
    entry_points={
        'console_scripts': [
            'pysesh=pysesh.main:main'
        ]
    }
)
