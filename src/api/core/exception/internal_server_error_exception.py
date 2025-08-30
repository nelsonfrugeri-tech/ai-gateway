class InternalServerErrorException(Exception):
    def __init__(self, exception: Exception = None, message: str = None):
        self.exception = exception
        self.message = message if message else str(exception)
        super().__init__(self.message)
