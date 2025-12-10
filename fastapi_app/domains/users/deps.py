from fastapi import Depends

from fastapi_app.domains.users.repository.user_repo import UserRepository
from fastapi_app.domains.users.service.user_service import UserService


def get_user_repo() -> UserRepository:
    return UserRepository()


def get_user_service(
    repo: UserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(repo)
