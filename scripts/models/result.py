class Result:
    def __init__(self, document, elapsed, response_size) -> None:
        self.document = document
        self.elapsed = elapsed
        self.response_size = response_size