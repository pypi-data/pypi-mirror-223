class InitialisationError(Exception):
    """
    Exception raised when there is a problem with initialization.

    This exception is raised when there is a problem with initializing an object or setting its initial state. This can happen if the input values are invalid or if there are missing required parameters during object creation.

    Attributes:
        None

    """
    def __init__(self):
        super().__init__()


class SizeError(Exception):
    """
    Exception raised when there is a problem with initialization.

    This exception is raised when there is a problem with initializing an object or setting its initial state. This can happen if the input values are invalid or if there are missing required parameters during object creation.

    Attributes:
        None

    """
    def __init__(self):
        print('Invalid Size!')
        super().__init__()