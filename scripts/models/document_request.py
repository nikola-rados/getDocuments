from logging import getLogger
from typing import Dict
import requests

from models.document import Document
from models.document_auth import DocumentAuth


logger = getLogger(__name__)


class DocumentRequest:
    def __init__(
        self,
        document: Document,
        url: str,
        auth: DocumentAuth,
        request_agency_identifier_id: str,
        request_part_id: str,
        application_code: str,
        court_division_code: str = "I",
    ) -> None:
        self.document = document
        self.url = url
        self.auth = auth
        self.request_agency_identifier_id = request_agency_identifier_id
        self.request_part_id = request_part_id
        self.application_code = application_code
        self.court_division_code = court_division_code

    @property
    def payload(self) -> Dict:
        return {
            "documentId": self.document.document_id,
            "fileId": self.document.file_id,
            "courtDivisionCd": self.court_division_code,
        }

    @property
    def headers(self) -> Dict:
        return {
            "RequestAgencyIdentifierId": self.request_agency_identifier_id,
            "RequestPartId": self.request_part_id,
            "ApplicationCd": self.application_code,
        }

    def request(self) -> requests.Response:
        logger.debug(f"Attempting connection to: {self.url}")
        try:
            response = requests.get(
                self.url,
                params=self.payload,
                headers=self.headers,
                auth=self.auth.auth,
            )

        except Exception as e:
            logger.error(f"Encountered error, returning `None`: {e}")
            response = None

        return response
