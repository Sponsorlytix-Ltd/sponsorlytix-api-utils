import os


class FileExtension:
    def get_extension(filename: str):
        extension = os.path.splitext(filename)[1][1:]
        return extension
