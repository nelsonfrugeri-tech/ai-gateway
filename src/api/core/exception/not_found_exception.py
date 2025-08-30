class NotFoundException(Exception):
    def __init__(self, entity: str):
        self.entity = entity

    def get_entity(self):
        return self.entity
