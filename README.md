## Installation

Prepare virtual env:

    python3.9 -m venv .venv

Activate venv:

    . .venv/bin/activate

Install dev depencencies:

    pip install -r requirements_dev.txt

## Run

Execute the module you prefer:

* Binary search:

      python -m algorithms.binary_search

* Binary tree:

      python -m algorithms.binary_tree

* Find the biggest box:

      python -m algorithms.binary_tree test
      python -m algorithms.binary_tree <LENGTH> <WIDTH>

* Recursive sum:

      python3.9 -m algorithms.recursive_sum

## Contributing

Format:

    black .
    isort .
