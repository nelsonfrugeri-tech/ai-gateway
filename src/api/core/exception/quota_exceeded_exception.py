class QuotaExceededException(Exception):
    def __init__(self, balance: int):
        self.balance = balance
