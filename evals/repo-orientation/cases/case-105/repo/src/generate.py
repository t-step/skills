from vendor.tinyresize import resize


def make_thumbnail(image_bytes: bytes, size: tuple[int, int]) -> bytes:
    return resize(image_bytes, size)
