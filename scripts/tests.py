import json
import os
from typing import Dict, List
import logging
import click
from dotenv import load_dotenv

from models.document import Document
from models.document_auth import DocumentAuth
from models.document_request import DocumentRequest
from models.threaded_test import ThreadedTest
from models.constant import *


def get_doc_data(env) -> Dict:
    """Returns document data from JSON files"""
    path = ""
    if env == PROD:
        path = PROD_DOC_DATA_PATH
    elif env == TEST:
        path = TEST_DOC_DATA_PATH
    elif env == DEV:
        path = DEV_DOC_DATA_PATH

    with open(path, "r") as f:
        data = json.load(f)

    return data


def load_auth(env) -> DocumentAuth:
    """Returns auth object to be used"""
    user_name = os.getenv("JC_INTERFACE_USERNAME")
    password = os.getenv(f"JC_INTERFACE_{env}_PASSWORD")
    return DocumentAuth(user_name, password)


def load_target_url(target, env) -> str:
    """Returns target URL from env"""
    if target == WSGW:
        return os.getenv(f"WSGW_URL_{env}")

    elif target == CATS:
        return os.getenv(f"CATS_URL_{env}")


def build_doc_list(doc_data) -> List[Document]:
    """Builds document list to be used in tests"""
    return [
        Document(doc_data["file_id"], doc["id"], doc["size"])
        for doc in doc_data["document_info"]
    ]


def get_application_code(env, target) -> str:
    """Returns appropriate app code"""
    if env == TEST and target == WSGW:
        return os.getenv("SCV_APPLICATION_CODE")
    else:
        return os.getenv("PCSS_APPLICATION_CODE")


@click.command()
@click.option(
    "-e",
    "--env",
    type=click.Choice(["DEV", "TEST", "PROD"]),
    default="DEV",
    help="Target environment",
)
@click.option(
    "-t",
    "--target",
    type=click.Choice(["wsgw", "cats"]),
    default="wsgw",
    help="Web service to target",
)
@click.option(
    "-d",
    "--document-target",
    type=int,
    default=1,
    help="Index of doc to target"
    @ click.option(
        "-c",
        "--connections",
        type=int,
        default=3,
        help="Number of concurrent connctions",
    ),
)
def main(env, target, document_target, connections):
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

    logger.debug("Setting up testing platform")
    documents = build_doc_list(get_doc_data(env))
    document = documents[document_target]

    target_url = load_target_url(target, env)
    auth = load_auth(env)

    request_agency_identifier_id = os.getenv(f"REQUEST_AGENCY_IDENTIFIER_ID_{env}")
    request_part_id = os.getenv(f"REQUEST_PART_ID_{env}")
    application_code = get_application_code(env, target)

    document_request = DocumentRequest(
        document,
        target_url,
        auth,
        request_agency_identifier_id,
        request_part_id,
        application_code,
    )

    test = ThreadedTest(document_request=document_request, connections=connections)
    logger.debug("Set up complete")

    test.run_test()


if __name__ == "__main__":
    main()
