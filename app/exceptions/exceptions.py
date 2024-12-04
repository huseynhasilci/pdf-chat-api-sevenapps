class PDFChatApiError(Exception):
    """base exception class"""

    def __init__(self, message: str = "Service is unavailable", name: str = "PDFChatApi", status_code: int = 500):
        self.message = message
        self.name = name
        self.status_code = status_code
        super().__init__(self.message, self.name)


class FileTypeNotSupportedError(PDFChatApiError):
    """If the uploaded file type is not supported."""

    pass


class FileSizeExceedError(PDFChatApiError):
    """If the uploaded file size is bigger then the required size."""

    pass


class PDFNotFoundError(PDFChatApiError):
    """If the uploaded file does not exist."""

    pass
