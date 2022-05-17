# Note if running in VSCODE, and entire output isn't showing:
# https://github.com/microsoft/debugpy/issues/582
from threading import Thread
import random
import time
from logging import getLogger

from scripts.models.document_request import DocumentRequest


logger = getLogger(__name__)


class ThreadedTest:
    """Runs tests concurrently

    Details on known PROD docs:

    | document ids | size (MB) |
    +--------------+-----------+
    |     22371932 |      1.57 |
    |     22371946 |      3.01 |
    |     22371960 |      5.88 |
    |     22371970 |      11.6 |
    |     22371992 |     17.38 |
    |     22372020 |     22.29 |
    |     22372055 |     35.39 |
    |     22372091 |     58.07 |
    |     22372143 |     97.16 |
    |     22372260 |    155.94 |
    """

    def __init__(
        self,
        document_request: DocumentRequest,
        connections: int = 3,
        test_length_minutes: float = 0.25,
    ) -> None:
        self.document_request = document_request
        self.connections = connections
        self.test_length_minutes = test_length_minutes

    def run_test(self):
        logger.info(
            f"Using {self.connections} connections over {self.test_length_minutes} minutes or {self.test_length_minutes * 60} seconds."
        )
        logger.info(
            f"Physical FileId / JustinFileId: {self.document_request.document.file_id}"
        )
        logger.info("=========================================")

        threads = []
        stop_threads = False
        for index in range(self.connections):
            x = Thread(
                target=self._through_jc_interface,  # if target == "jc" else test_scv_api,
                args=(index, lambda: stop_threads),
            )
            threads.append(x)
            x.start()
        for thread in threads:
            thread.join()

    def _through_jc_interface(self, index, stop) -> None:
        sleep_time_seconds = random.randint(2, self.test_length_minutes * 60)

        logger.info(
            f"Setup - Thread {index+1} - document id: {self.document_request.document.document_id}, document size: {self.document_request.document.size} MB - waiting {sleep_time_seconds} seconds before fetching."
        )

        time.sleep(sleep_time_seconds)

        logger.info(
            f"Fetching - Thread {index} - document id: {self.document_request.document.document_id}, document size: {self.document_request.document.size} MB."
        )

        response = self.document_request.request()

        if response:
            logger.info(
                f"{index} - Response - {response.status_code} - {response.reason} - URL - {response.url}"
            )
            logger.info(
                f"{index} - DocumentId: {self.document_request.document.document_id} - Response Size: {round(len(response.content)/1024/1024,2)} MB - Elapsed: {round(response.elapsed.total_seconds()*1000, 2)} ms"
            )

        else:
            logger.error(
                f"ERROR! - DocumentId: {self.document_request.document.document_id} - Failed to fetch."
            )

        logger.info("=========================================")
