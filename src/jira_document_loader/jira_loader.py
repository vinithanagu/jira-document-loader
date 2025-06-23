from __future__ import annotations
import warnings
from typing import Iterator
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.utils import get_from_env

# Suppress a known harmless warning from the Jira library
warnings.filterwarnings("ignore", category=DeprecationWarning, module='jira')


class JiraLoader(BaseLoader):
    """
    A Document Loader for loading issues from a Jira project.
    """

    def __init__(self, client: 'JIRA', jql_query: str):
        """
        Initializes the loader with a Jira client and a JQL query.
        """
        self.client = client
        self.jql_query = jql_query
        print("✅ JiraLoader initialized.")

    @classmethod
    def from_credentials(cls, jql_query: str, server_url: str | None = None, username: str | None = None,
                         api_token: str | None = None) -> JiraLoader:
        """
        Convenience constructor that builds the JIRA client for you.

        Args:
            jql_query: The JQL query to fetch issues.
            server_url: Your Jira instance URL. Can also be set as JIRA_SERVER_URL env var.
            username: Your Atlassian email. Can also be set as JIRA_USERNAME env var.
            api_token: Your Jira API token. Can also be set as JIRA_API_TOKEN env var.
        """
        try:
            from jira import JIRA
        except ImportError as ex:
            raise ImportError(
                "Could not import jira python package. "
                "Please install it with `pip install jira`."
            ) from ex

        # Get credentials from arguments or environment variables
        server = server_url or get_from_env("server_url", "JIRA_SERVER_URL")
        user = username or get_from_env("username", "JIRA_USERNAME")
        token = api_token or get_from_env("api_token", "JIRA_API_TOKEN")

        # Create the Jira client
        client = JIRA(server=server, basic_auth=(user, token))

        return cls(client, jql_query)

    def lazy_load(self) -> Iterator[Document]:
        """
        A lazy loader that fetches issues one by one and yields
        LangChain Document objects.
        """
        print(f"⏳ Fetching issues with JQL: '{self.jql_query}'...")
        issues = self.client.search_issues(self.jql_query, maxResults=0)
        print(f"✔ Found {len(issues)} issues. Yielding documents...")

        for issue in issues:
            yield self._issue_to_doc(issue)

    def _issue_to_doc(self, issue: 'JiraIssue') -> Document:
        """Converts a Jira issue into a LangChain Document."""
        page_content = f"Summary: {issue.fields.summary}\n\nDescription: {issue.fields.description or 'No description'}\n\n"

        for comment in issue.fields.comment.comments:
            page_content += f"Comment by {comment.author.displayName}:\n{comment.body}\n\n"

        metadata = {
            "source": issue.self,
            "issue_key": issue.key,
            "status": issue.fields.status.name,
            "reporter": issue.fields.reporter.displayName,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
            "created_at": issue.fields.created,
            "updated_at": issue.fields.updated,
        }
        return Document(page_content=page_content, metadata=metadata)