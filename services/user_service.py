from typing import Dict, Optional
import repositories.user_respository as user_repository


class UserService:

    @staticmethod
    def register(username: str, name: str, password: str) -> int:
        existing = user_repository.get_user_by_username(username)
        if existing:
            raise ValueError("Username already exists")

        return user_repository.register_user(username, name, password)

    @staticmethod
    def login(username: str, password: str) -> Dict:
        return user_repository.login_user(username, password)


    @staticmethod
    def get_user(user_id: int, acting_user: Dict) -> Dict:
        if acting_user is None:
            raise PermissionError("Not authenticated")

        if acting_user["id"] != user_id and (acting_user["is_admin"] != 1 or acting_user["is_approver"] != 1):
            raise PermissionError("Access denied")

        user = user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return user

    @staticmethod
    def update_user(
            *,
        target_user_id: int,
        acting_user: Dict,
        name: Optional[str] = None,
        password: Optional[str] = None,
        is_admin: Optional[bool] = None,
        is_approver: Optional[bool] = None,
    ) -> None:
        if not acting_user:
            raise PermissionError("Not authenticated")

        if is_admin is True and acting_user["id"] == target_user_id:
            raise ValueError("Admin cannot grant admin to himself")

        user_repository.update_user(
            target_user_id=target_user_id,
            acting_user=acting_user,
            name=name,
            password=password,
            is_admin=is_admin,
            is_approver=is_approver,
        )

    # =========================
    # DELETE
    # =========================

    @staticmethod
    def delete_user(user_id: int, acting_user: Dict) -> None:
        if not acting_user or acting_user["is_admin"] != 1:
            raise PermissionError("Admin only")

        user_repository.delete_user(user_id, acting_user)