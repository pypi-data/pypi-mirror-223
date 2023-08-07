import sys
import pickle
import readline
import argparse
from colr import color
from rich.console import Console
from collections import OrderedDict
import inquirer
import pysesh
import os

console = Console()

col = OrderedDict([
    ('n', '#67D0A8'),
    ('w', '#FFCC00'),
    ('d', '#ff2e63'),
    ('s', '#00fc03'),
    ('l', '#F0F0F0'),
])

def cpr(text: str):
    console.print(text)

parser = argparse.ArgumentParser(description='Python Multiplex - A Session Management Utility for Python.')
subparsers = parser.add_subparsers(dest='command')

new_parser = subparsers.add_parser('new', help='Create a new session.')
new_parser.add_argument('name', type=str, help='Name of the new session.')

load_parser = subparsers.add_parser('load', help='Load an existing session.')
load_parser.add_argument('name', type=str, help='Name of the session to load.')

delete_parser = subparsers.add_parser('delete', help='Delete a session.')
delete_parser.add_argument('name', type=str, help='Name of the session to delete.')

list_parser = subparsers.add_parser('list', help='List all available sessions.')

args = parser.parse_args()


DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), 'state'))
REPOSITORY = os.path.join(DIRECTORY, 'sessions.pickle')

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
