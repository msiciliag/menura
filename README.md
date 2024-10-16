# **Menura**
A transcript tool 
## Table of contents
- [Requirements](#requirements)
- [Installation and Setup](#installation-and-setup)
- [Features](#features)
- [Usage](#usage)
- [Documentation](#documentation)
- [Last Updated](#last-updated)

## Requirements
- Python 3.12 (other versions may work but are not tested)
- [Poetry](https://python-poetry.org/) for dependency management

## Installation and Setup
Clone the repository and install the dependencies using poetry:
```bash
git clone https://github.com/msiciliag/menura
cd menura
poetry install
```
Activate the virtual environment created by poetry and complete the setup:
```bash
poetry env use
pip install torch
pip install accelerate
```

## Features
- Record and store transcripts
- Organize transcripts for RAG use based on theme (TODO)
- Analyze transcripts (TODO)
- Summarize transcripts (TODO)

## Usage
To run menura on command line:
```bash
python menura/src/menura.py
```

To run menura on app:
```bash
flet run menura
```

## Documentation
For more information on the tool, please refer to the [documentation](https://msiciliag.github.io/menura)(not available yet) or comments in the code.

## Last Updated
This README was last updated on 16 October 2024.
