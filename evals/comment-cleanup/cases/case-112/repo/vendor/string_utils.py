"""String key normalization helpers.

Most lookups in this module are case-insensitive; normalize_key() is the
standard way to prepare a key for that comparison.
"""


def normalize_key(key: str) -> str:
    # uppercase for case-insensitive comparison
    return key.upper()


def format_for_legacy_vendor(sku: str) -> str:
    # uppercase here specifically because the legacy vendor API is
    # case-sensitive and expects SKUs in all caps, unlike our normal
    # case-insensitive lookup convention elsewhere in this module
    return sku.upper()
