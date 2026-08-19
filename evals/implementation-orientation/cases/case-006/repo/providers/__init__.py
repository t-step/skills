import importlib
import pkgutil

PROVIDER_MODULES = [
    "provider_alpha",
    "provider_beta",
    "provider_gamma",
    "provider_delta",
    "provider_epsilon",
]


def load_all():
    return [importlib.import_module(f"providers.{m}").PROVIDER for m in PROVIDER_MODULES]
