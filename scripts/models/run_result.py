import logging
from models.result import Result
from typing import List


class RunResult:
    def __init__(self) -> None:
        self.results = []

    def add(self, result: Result) -> None:
        self.results.append(result)

    def add_multiple(self, multi: List[Result]) -> None:
        self.results.extend(multi)

    def print(self) -> None:
        times = [result.elapsed for result in self.results]
        minimum = int(min(times))
        maximum = int(max(times))
        avg = int(sum(times)/len(times))

        result = self.results[0]
        print("========================")
        print(f"Doc ID: {result.document.document_id}")
        print(f"File Size: {result.response_size}")
        print(f"Average (ms): {avg}")
        print(f"Max (ms): {maximum}")
        print(f"Min (ms): {minimum}")
        print("========================")

