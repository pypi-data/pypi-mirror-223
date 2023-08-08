""""
Basic Dune Client Class responsible for refreshing Dune Queries
Framework built on Dune's API Documentation
https://duneanalytics.notion.site/API-Documentation-1b93d16e0fa941398e15047f643e003a
"""
from __future__ import annotations

import logging.config
from typing import Dict


# pylint: disable=too-few-public-methods
class BaseDuneClient:
    """
    A Base Client for Dune which sets up default values
    and provides some convenient functions to use in other clients
    """

    BASE_URL = "https://api.dune.com"
    DEFAULT_TIMEOUT = 10

    def __init__(
        self, api_key: str, client_version: str = "v1", performance: str = "medium"
    ):
        self.token = api_key
        self.client_version = client_version
        self.performance = performance
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s")

    @property
    def api_version(self) -> str:
        """Returns client version string"""
        return f"/api/{self.client_version}"

    def default_headers(self) -> Dict[str, str]:
        """Return default headers containing Dune Api token"""
        return {"x-dune-api-key": self.token}
