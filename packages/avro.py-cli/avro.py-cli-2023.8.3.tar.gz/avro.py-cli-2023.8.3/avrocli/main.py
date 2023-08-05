# SPDX-License-Identifier: MIT


# Import local modules.
from typing import Tuple, Union

# Import avro.py .
import avro

# Import third-party modules.
import click
import pyclip
from rich.console import Console
from rich.table import Table

# Initializing Rich.
console = Console()


# Setting up the default group for Click.
@click.group()
def cli():
    pass


# parse --text yourtexthere
@cli.command()
@click.option(
    '-t',
    '--text',
    required=True,
    multiple=True,
    type=str,
    help='Text you want to parse.',
)
@click.option('--ascii', help='Returns the parsed text in ASCII.', is_flag=True)
def parse(text: Union[str, Tuple[str]], ascii: bool) -> None:
    '''
    Parses input text into Bangla, matches and replaces using avrodict.
    '''

    # Form a Table() instance for the --view-table flag.
    table = Table()
    table.add_column('Raw', style='cyan', no_wrap=True, justify='center')
    table.add_column('Bengali (copied to clipboard)', style='magenta', justify='center')

    # Define a new function for pre-processing the texts given by the user.
    def subparse_click(text: str):
        parsed_text = avro.parse(text) if not ascii else avro.parse(text, in_ascii=True)
        table.add_row(f'{text}\n', f'{parsed_text}')

        return parsed_text

    # Processing.
    parsed = []
    for t in tuple(text):
        parsed.append(subparse_click(t))

    # Post-processing and modifying the clipboard.
    pyclip.copy('\n\n'.join(parsed))

    console.line()
    console.print(table, justify='center')
    console.line()


# reverse --text yourtexthere
@cli.command()
@click.option(
    '-t',
    '--text',
    required=True,
    multiple=True,
    type=str,
    help='Text you want to reverse.',
)
def reverse(text: Union[str, Tuple[str]]) -> None:
    '''
    Reverses input text to English Roman script.
    '''

    # Form a Table() instance for the --view-table flag.
    table = Table()
    table.add_column('Bengali', style='cyan', no_wrap=True, justify='center')
    table.add_column('Reversed (copied to clipboard)', style='magenta', justify='center')

    # Define a new function for pre-processing the texts given by the user.
    def subreverse_click(text: str):
        reversed_text = avro.reverse(text)
        table.add_row(f'{text}\n', f'{reversed_text}')

        return reversed_text

    # Processing.
    reversed = []
    for t in tuple(text):
        reversed.append(subreverse_click(t))

    # Post-processing and modifying the clipboard.
    pyclip.copy('\n\n'.join(reversed))

    console.line()
    console.print(table, justify='center')
    console.line()
