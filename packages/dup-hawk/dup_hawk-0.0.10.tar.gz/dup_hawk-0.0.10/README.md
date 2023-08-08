# dup_hawk

🦅 A bot the looks for duplicate issues on a GitHub repo, created especially for competitive security reviews. 

<!-- use html to import an image -->
<p align="center">
  <img src="./img/dups.png" alt="dup-hawk" width="500"/>
</p>


# Getting Started
## Requirements

- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - You'll know you did it right if you can run `git --version` and you see a response like `git version x.x.x`
- [Python](https://www.python.org/downloads/)
  - You'll know you've installed python right if you can run:
    - `python --version` or `python3 --version` and get an output like: `Python x.x.x`
- [pipx](https://pypa.github.io/pipx/installation/)
  - `pipx` is different from [pip](https://pypi.org/project/pip/)
  - You may have to close and re-open your terminal
  - You'll know you've installed it right if you can run:
    - `pipx --version` and see something like `x.x.x.x`
- [poetry](https://python-poetry.org/docs/)
  - You'll know you've installed it right if you can run `poetry --version` and get an output like `Poetry (version 1.4.2)`

## Installation

### pipx

```
pipx install dup_hawk
```

### From Source

```
git clone https://github.com/Cyfrin/dup-hawk
cd dup-hawk
pip install . -e
```

## Quickstart 

```
dup-hawk --help
```

To run the duplicate checker, run:

```
dup-hawk --git-repo-url {URL} --git-pat-token {PAT_TOKEN}
```

And you will have marked the issues on your github repo!

# Tests

```
poetry run pytest
```

## Integration tests

```
poetry run pytest -m ""
```

## Specific tests with pdb and stdout

```
poetry run pytest -k "test_mark_duplicates_from_dfs" --pdb -s
```

# Big TODO

Add mocking unit tests. 
