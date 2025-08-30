from enum import Enum


class Extension(Enum):
    JPEG = b"\xff\xd8\xff"
    PNG = b"\x89PNG\r\n\x1a\n"
    GIF87A = b"GIF87a"
    GIF89A = b"GIF89a"
    WEBP = b"RIFF"
    WEBP_SUBSTRING = b"WEBP"
