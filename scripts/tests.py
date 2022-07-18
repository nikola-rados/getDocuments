import json
import os
from typing import Dict, List
import logging
from webbrowser import get
import click
from dotenv import load_dotenv

from models.document import Document
from models.document_auth import DocumentAuth
from models.document_request import DocumentRequest
from models.threaded_test import ThreadedTest
from models.constant import *
from models.run_result import RunResult


def get_doc_data() -> List[Document]:
    """Returns document data from JSON files"""
    with open(DOC_DATA_PATH, "r") as f:
        data = json.load(f)

    return data


def load_auth(env) -> DocumentAuth:
    """Returns auth object to be used"""
    user_name = os.getenv("JC_INTERFACE_USERNAME")
    password = os.getenv(f"JC_INTERFACE_{env}_PASSWORD")
    return DocumentAuth(user_name, password)


def load_target_url(web_service, env) -> str:
    """Returns web service URL from env"""
    if web_service == WSGW:
        return os.getenv(f"WSGW_URL_{env}")

    elif web_service == CATS:
        return os.getenv(f"CATS_URL_{env}")


def build_doc_list(doc_data: Dict, env: str, document_ids: List[str]) -> List[Document]:
    """Builds document list to be used in tests"""
    return [
        Document(doc_datum[FILE_ID], str(doc_datum[DOCUMENT_ID]), doc_datum[DOCUMENT_SIZE])
        for doc_datum in doc_data[env] if str(doc_datum[DOCUMENT_ID]) in document_ids
    ]


def get_application_code(env, target) -> str:
    """Returns appropriate app code"""
    if env == TEST and target == WSGW:
        return os.getenv("SCV_APPLICATION_CODE")
    else:
        return os.getenv("PCSS_APPLICATION_CODE")


def get_document_options() -> List[str]:
    return [
        str(document[DOCUMENT_ID]) for env in [DEV, TEST, PROD] 
        for document in get_doc_data()[env]
    ]


@click.command()
@click.option(
    "-e",
    "--env",
    type=click.Choice([DEV, TEST, PROD]),
    default=DEV,
    help="Target environment",
)
@click.option(
    "-w",
    "--web-service",
    type=click.Choice([WSGW, CATS]),
    default=WSGW,
    help="Web service to target",
)
@click.option(
    "-d",
    "--document-ids",
    type=click.Choice(get_document_options()),
    multiple=True,
    help="Document ids for testing"
)
@click.option(
    "-c",
    "--connections",
    type=int,
    default=5,
    help="Number of concurrent connctions",
)
@click.option(
    "-r",
    "--runs",
    type=int,
    default=1,
    help="Number of runs to perform"
)
def main(env, web_service, document_ids, connections, runs):
    """Runs tests"""
    # Do not need dotenv in Openshift
    # load_dotenv()

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            # logging.FileHandler("getDocuments.log"),
            logging.StreamHandler()
        ],
    )
    logger = logging.getLogger(__name__)
    logger.info("=========================================")

    test_docs = build_doc_list(get_doc_data(), env, document_ids)

    target_url = load_target_url(web_service, env)
    auth = load_auth(env)

    request_agency_identifier_id = os.getenv(f"REQUEST_AGENCY_IDENTIFIER_ID_{env}")
    request_part_id = os.getenv(f"REQUEST_PART_ID_{env}")
    application_code = get_application_code(env, web_service)

    doc_requests = [
        DocumentRequest(
            test_doc,
            target_url,
            auth,
            request_agency_identifier_id,
            request_part_id,
            application_code,
        )
        for test_doc in test_docs
    ]
    
    threaded_tests = [
        ThreadedTest(
            document_request=doc_request,
            connections=connections
        )
        for doc_request in doc_requests
    ]

    for threaded_test in threaded_tests:
        results = RunResult()
        for n in range(runs):
            threaded_test.run_test()
            results.add_multiple(threaded_test.results)
        results.print()


if __name__ == "__main__":
    main()
