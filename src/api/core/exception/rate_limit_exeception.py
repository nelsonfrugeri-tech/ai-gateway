import openai


class RateLimitException(Exception):

    def __init__(self, exception: openai.RateLimitError) -> None:
        self.exception = exception
        super().__init__(str(exception))
