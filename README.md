# colab-run

Turn colab form metadata into command line arguments

## Usage

THIS PACKAGE ISN'T PUBLISHED TO PIP

Install using the following.

VVVVVVVVVVVVVVVVVVVVV

`pip install git+https://github.com/brysgo/colab-run`

^^^^^^^^^^^^^^^^^^^^^

Run with

`colab-run --help` - prints a help message

`colab-run ./path/to/colab.py --help` - prints available options for colab file

`colab-run ./path/to/colab.py` - converts the file with options included (TODO: make this run the file instead)

## Todos

- [ ] make colab-run actually run the script
- [ ] support custom text in dropdown
- [ ] support range checking
- [ ] add runtime support for pretty colab things
