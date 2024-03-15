# Contributing to ParityVend Python API

Thank you for considering contributing to the ParityVend Python API! We value your time and efforts to help us improve and grow. This document will guide you through the contribution process. Whether it's a bug fix, new feature, or documentation improvement, your help is invaluable in making this project better.

## Code of Conduct

Before contributing, please ensure you have read and understood our [Code of Conduct](https://github.com/ParityVend/parityvend_api_python/blob/main/CODE_OF_CONDUCT.md). We are committed to providing a welcoming and inclusive experience for everyone.

## Getting Help

If you have any questions, need assistance, or want to discuss ideas for improvements, feel free to reach out to us at "help AT ambeteco DOT com". We strive to respond promptly and provide helpful guidance.

## Development Setup

To get started with development, make sure you have the following prerequisites installed:

- Python (version 3.8 or higher)
- Pip (Python package installer)

### Step 1: Clone the Repository

First, clone the repository to your local machine:

```sh
git clone https://github.com/ParityVend/parityvend_api_python.git
cd python_api
```

### Step 2: Set up a Virtual Environment (Optional but Recommended)

It's a good practice to create a virtual environment to isolate project dependencies and avoid conflicts with other Python projects on your system. You can use the built-in `venv` module or a tool like `virtualenv`.

#### Using `venv`

```sh
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### Using `virtualenv`

```sh
pip install virtualenv
virtualenv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

### Step 3: Install Dependencies

With the virtual environment activated (if you chose to use one), install the project dependencies:

```sh
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### Step 4: Run Tests

Before making any changes, ensure that the existing tests pass on your system:

```sh
pytest -rP tests
```

**Note:** To run the tests successfully, you will need to obtain a valid ParityVend API key and set the following environment variables:

- `parityvend_secret_key`
- `parityvend_secret_key_free`

For this, run:

```sh
export PARITYVEND_SECRET_KEY='your-secret-key'
export PARITYVEND_SECRET_KEY_FREE='your-free-key'
```

Or, for Windows:
```cmd
set "parityvend_secret_key=your-secret-key"
set "parityvend_secret_key_free=your-free-key"
```

### Step 5: Make Changes

Now you're ready to start making changes to the codebase! Follow best practices for Python development, write tests for new features or bug fixes, and ensure that all existing tests pass before submitting a pull request.

## Submitting a Pull Request

1. Fork the repository and create a new branch for your changes.
2. Make your changes and commit them with descriptive commit messages.
3. Push your changes to your forked repository.
4. Create a pull request on the main repository, describing your changes and the motivation behind them.

We'll review your pull request as soon as possible and provide feedback or merge it into the main codebase.

## Code Style and Guidelines

To ensure consistency and maintainability, please follow the established code style and guidelines for this project:

* Use Ruff for code formatting and linting.
* Follow the PEP 8 style guide for Python code.
* Write clear and concise commit messages.
* Keep the codebase clean and well-documented.
* Ensure backward compatibility when making changes.

## Other Ways to Contribute
There are many ways to contribute to the project beyond writing code:

* Report Bugs: If you discover a bug, create an issue on the project's GitHub repository with detailed steps to reproduce the issue.
* Improve Documentation: Help us improve the project's documentation by suggesting edits, fixing typos, or writing additional documentation for new features.
* Suggest New Features: Share your ideas on new functionality that you would want to see in the ParityVend Python API.

Thank you for your interest in contributing to the ParityVend Python API! We appreciate your efforts to make this project better.