**Author: Dagmara Przygocka**
### What is the choice of three static analysis tools ?

For the Mini Twit project the team decided to use the following linter tools:
- Flake8: 
    We chose Flake 8 due to:
        - easy set up, 
        - low rate of false positives,
        - support of Python3+,
        - popular Python linter with broad online community support,
        - combines several other tools: pycodestyle(pep8), pyflakes, mccabe,
        - provides feedback on issues related to style, syntax, and potential errors.
    Flake8 supports storing its configuration setup.cfg, tox.ini, or .flake8. We decided to use .flake8 with extendedn default setup presented below.
    ```
    [flake8]
    //ignoring error code E203, which is related to whitespace around operators
    extend-ignore = E203
    //list of excluded directories or files from being analyzed by flake8
    exclude = .git,__pycache__,docs/source/conf.py,old,build,dist,ITU_MiniTwitFlask
    //maximum complexity of a block of code before flake8 reports it as an error
    max-complexity = 10
    //maximum allowed length of a line of code, including whitespace and comments
    max-line-length = 100
    ```

- Black: 
    We chose Black due to:
        - support of Python3.7+,
        - code formating capabilities,
        - automatically reformats Python code to follow a consistent style,
        - large online community support,
        - ability identify and fix some common syntax errors (missing parentheses or brackets).
    In the project we used configuration file for black called pyproject.toml with following setup: 
    ```
    [tool.black]
    // maximum line length that Black should allow before wrapping lines.
    line-length = 100
    //list of directories or files that Black should exclude from formatting
    exclude = "ITU_MiniTwitFlask"
    ```
- Bandit: 
    We chose Bandit due to:
        - capabilities to indentify security vulnerabilities and weaknesses in Python code,
        - recommendations and solutions for fixing the security threads,
        - ease of integration,
        - meets industry-standard security requirements,
        - large online community support.
    The Bandit configuration file is called bandit.yml and contains where we specified which file or directory should be excluded from the analysis. The bandit.yml file content look as follows:
    ```
    exclude_dirs:
        - "./ITU_MiniTwitFlask/**"
    ```

In order to make development process easier we decided to create separate github action where the above tools are run against the pull request. The pipline setup is in file called static-check-branch.yml and contains:
```
---
name: Static check

//the pipline will be run on any branch but main
on:
  push:
    branches:
      - '**'
      - '!main'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install flake8
          pip install bandit
          pip install black
          pip install -r ./ITU_MiniTwit/requirements.txt
          pip install -r ./Minitwit-api/requirements.txt

      - name: Run Black
        run: |
          black .
        continue-on-error: false
      
      - name: Show Black changes
        run: git diff

      - name: Run Flake8
        run: |
          flake8
        continue-on-error: true

      - name: Run Bandit
        run: |
          bandit -r . --configfile bandit.yml --severity=high
        continue-on-error: true
```

    


