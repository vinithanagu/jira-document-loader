from setuptools import setup, find_packages

setup(
    name="jira_document_loader",
    version="0.1.0",
    author="vinithan",
    author_email="vinitha2595@gmail.com",
    description="A custom LangChain document loader for Jira.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "langchain-core>=0.1.0",
        "jira>=3.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)