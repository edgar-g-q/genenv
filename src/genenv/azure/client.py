"""Azure client for Autorelease."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


class AzureClient:
    """Azure client for Autorelease."""

    def __init__(self, pat=None, organization=None):
        """Initialize AzureClient."""
        self.pat = pat or os.getenv("AZURE_PERSONAL_ACCESS_TOKEN")
        self.organization = organization or os.getenv("AZURE_ORGANIZATION")
        self.base_url = f"https://dev.azure.com/{self.organization}/"
        self.base_url_feeds = (
            f"https://feeds.dev.azure.com/{self.organization}/"
        )

    def get_projects(self):
        """Get all projects in the organization."""
        url = f"{self.base_url}_apis/projects"
        r = requests.get(url, auth=("", self.pat))
        projects = r.json()["value"]
        return projects

    def get_artifacts(self, project):
        """Get all artifacts in a project."""
        url = f"{self.base_url}{project}/_apis/pipelines"
        r = requests.get(url, auth=("", self.pat))
        artifacts = r.json()["value"]
        return artifacts

    def get_feeds(self, project):
        """Get all feeds in a project."""
        url = f"{self.base_url_feeds}{project}/_apis/packaging/Feeds"
        r = requests.get(url, auth=("", self.pat))
        feeds = r.json()["value"]
        return feeds

    def get_artifact_details(self, project, feed):
        """Get all artifact details in a feed."""
        url = (
            f"{self.base_url_feeds}{project}"
            f"/_apis/packaging/Feeds/{feed}/packages?protocolType=PyPI"
        )
        r = requests.get(url, auth=("", self.pat))
        artifact_details = r.json()["value"]
        return artifact_details

    def get_variable_groups(self, project):
        """Get all variable groups in a project."""
        url = f"{self.base_url}{project}/_apis/distributedtask/variablegroups"
        r = requests.get(url, auth=("", self.pat))
        variable_groups = r.json()["value"]
        return variable_groups
