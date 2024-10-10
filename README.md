
# Adhoc: Auto-Documenting Codebase Changes

Adhoc is a command-line tool designed to automatically document changes in your codebase. By integrating with local language models, it generates detailed explanations of code modifications and compiles them into professional documentation formats such as LaTeX, Markdown, or Word. This tool streamlines the documentation process, making it effortless for developers to maintain up-to-date records of their code evolution.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Committing Changes](#committing-changes)
  - [Generating Documentation](#generating-documentation)
  - [Configuration](#configuration)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features
- **Automatic Documentation**: Generates explanations for code changes using a local Large language models (LLMs).
- **Multiple Output Formats**: Supports documentation in LaTeX, Markdown, and Word formats.
- **Version Control Integration**: Detects code changes and commits through simple commands.
- **Configurable Settings**: Allows customization of output formats and author information via a configuration file.
- **Extensible Design**: Modular structure makes it easy to extend functionalities.

## Installation
To install Adhoc, you can use pip:
```bash
pip install adhoc-python
```
Ensure you have the necessary dependencies listed in the `requirements.txt` file.

## Usage
Adhoc provides a set of commands to initialize your project, commit changes, generate documentation, and configure settings. Below is an explanation of each command and how to use it.

### Initialization
Before using Adhoc, you need to initialize your project:
```bash
adhoc init --model "your ollama model"
```
**What it does**:
- Creates a `.Adhoc` directory in your project root to store configurations and databases.
- Initializes a SQLite database to track code changes.
- Initializes the whole code to work with your choice of LLM and then generates a codebase summary for context.

### Committing Changes
After making changes to your codebase, use the following command to commit those changes and generate explanations:
```bash
adhoc commit -m "Your commit message"
```
**Options**:
- `-m, --message`: (Optional) A commit message describing the changes.

**What it does**:
- Detects changes since the last commit by comparing snapshots.
- Generates explanations for the changes using the LLM, incorporating your commit message if provided.
- Stores the changes and explanations in the database for future reference.

### Generating Documentation
To create documentation of your codebase and its changes, run:
```bash
adhoc generate
```
**What it does**:
- Retrieves the codebase summary and change explanations from the database.
- Generates a documentation file in the format specified in your configuration (latex, markdown, or word).
- The output file (`documentation.tex`, `documentation.md`, or `documentation.docx`) is created in your project directory.

### Configuration
Customize Adhoc settings using the `adhoc config` command:
```bash
adhoc config -d md -u "Your Name"
```
**Options**:
- `-d, --document-format`: Sets the output document format. Accepts `md` for Markdown, `tex` for LaTeX, or `word` for Word documents.
- `-u, --username`: Sets the author name to be used in the documentation.

**What it does**:
- Updates the configuration file (`config.json` in the `.Adhoc` directory) with your preferences.
- The changes affect how documentation is generated and personalized.

**Example**:
```bash
adhoc config -d word -u "Shreyas"
```
- Sets the output format to Word.
- Sets the author name to "Shreyas".

## Requirements
- Python 3.6 or higher

**Dependencies**:
- `jinja2`
- `requests`
- `watchdog`
- `python-docx` (for Word document generation)

Additional dependencies are listed in `requirements.txt`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## A Reflective Note
> "Life is an ad hoc affair. It has to be improvised all the time because of the hard fact that everything we do changes what is. This is distressing to people who would like to see things beautifully planned out and settled once and for all. That cannot be."  
> ― Jane Jacobs


Happy coding!
