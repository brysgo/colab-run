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

`colab-run ./path/to/colab.py` - run the file

`colab-run ./path/to/colab.py --colabParam somevalue` - run the file with `colabParam` set to `somevalue`

`colab-run ./path/to/colab.py --print` - print the file with the arguments (for debugging)

## Todos

- [x] make colab-run actually run the script
- [ ] support custom text in dropdown
- [ ] support range checking
- [ ] add runtime support for pretty colab things
- [ ] add support for yaml instead of cli args (thanks mike)
