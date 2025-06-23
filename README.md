# Jira Loader for LangChain

A simple, installable Python package that provides a `JiraLoader` for use with the LangChain framework. This loader connects to a Jira instance, fetches issues based on a JQL query, and converts them into LangChain `Document` objects, ready for use in RAG pipelines and other LLM applications.

This package follows modern Python packaging standards and is designed to be easy to use and extend.

## Features

* Connects to Jira Cloud or Server instances.
* Uses a JQL query to precisely select which issues to load.
* Loads issue summary, description, and all comments into the document content.
* Enriches each document with useful metadata like issue key, status, reporter, and dates.
* Provides a simple `from_credentials` constructor that can read connection details from environment variables.
* Uses a lazy loader (`lazy_load`) for memory-efficient processing of large numbers of tickets.

## Installation

You can install this package directly from PyPI using pip:

```bash
pip install -i https://test.pypi.org/simple/ jira-document-loader