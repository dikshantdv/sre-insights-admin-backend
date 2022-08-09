import uuid


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


class UUIDException(Exception):
    def __init__(self, name: str):
        self.name = name
