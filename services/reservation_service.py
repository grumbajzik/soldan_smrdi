from typing import Dict, List, Optional
import repositories.reservation_repository as reservation_repo
import repositories.equipment_repository as equipment_repo


class ReservationService:

    @staticmethod
    def create_reservation(user_id: int, equipment_id: int, date_val):
        # Ověření existence vybavení
        eq = equipment_repo.get_equipment_by_id(equipment_id)
        if not eq:
            raise ValueError("Equipment not found")

        # Voláme repo bez komentáře
        return reservation_repo.create_reservation(user_id, equipment_id, str(date_val))

    @staticmethod
    def get_my_reservations(user_id: int, status: Optional[str] = None) -> List[Dict]:
        return reservation_repo.get_reservations(user_id=user_id, status=status)

    @staticmethod
    def get_all_reservations(acting_user: Dict, status: Optional[str] = None) -> List[Dict]:
        # Kontrola práv (admin nebo approver)
        if not acting_user or (acting_user["is_admin"] != 1 and acting_user["is_approver"] != 1):
            raise PermissionError("Access denied")

        return reservation_repo.get_reservations(status=status)

    @staticmethod
    def update_status(reservation_id: int, new_status: str, comment: Optional[str], acting_user: Dict):
        # Jen admin nebo schvalovatel může měnit stav
        if not acting_user or (acting_user["is_admin"] != 1 and acting_user["is_approver"] != 1):
            raise PermissionError("Only approvers can change status")

        valid_statuses = {'PENDING', 'APPROVED', 'REJECTED', 'RETURNED'}
        if new_status not in valid_statuses:
            raise ValueError("Invalid status")

        # Předáváme status i nový komentář
        reservation_repo.update_reservation_status(reservation_id, new_status, comment)

    @staticmethod
    def get_available_on_date(target_date: date) -> List[Dict]:
        # Převedeme date na string (YYYY-MM-DD), protože tak to ukládáme v DB
        date_str = str(target_date)

        items = equipment_repo.get_equipment_availability(date_str)

        # Pojistka: Kdyby náhodou v DB byla chyba a rezervací bylo více než kusů,
        # nepustíme ven záporné číslo, ale zobrazíme 0.
        for item in items:
            if item["quantity_available"] < 0:
                item["quantity_available"] = 0

        return items


