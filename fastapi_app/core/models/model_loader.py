import pkgutil
import importlib
from pathlib import Path


def load_models_from_package(package_name: str):
    """
    Импортирует все модули внутри указанного пакета.
    Нужно для того, чтобы SQLAlchemy зарегистрировал модели в Base.metadata.
    """
    package = importlib.import_module(package_name)
    package_path = Path(package.__file__).parent

    for module in pkgutil.iter_modules([str(package_path)]):
        importlib.import_module(f"{package_name}.{module.name}")


def load_all_models():
    """
    Импортирует модели из всех доменов проекта.
    Просто добавляй сюда новые домены по мере расширения.
    """
    load_models_from_package("domains.users.models")

    # Если добавишь другие домены, добавь сюда:
    # load_models_from_package("fastapi_app.domains.products.models")
    # load_models_from_package("fastapi_app.domains.inventory.models")
