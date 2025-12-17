from datetime import date
from typing import Dict, List, Optional
import repositories.equipment_repository as equipment_repo


class EquipmentService:

    @staticmethod
    def create_equipment(name: str, description: str, quantity_total: int, image_path: Optional[str],
                         acting_user: Dict) -> int:
        if not acting_user or acting_user["is_admin"] != 1:
            raise PermissionError("Only admin can add equipment")
        return equipment_repo.create_equipment(name, description, quantity_total, image_path)

    @staticmethod
    def get_all() -> List[Dict]:
        return equipment_repo.get_all_equipment()

    @staticmethod
    def get_by_id(equipment_id: int) -> Dict:
        eq = equipment_repo.get_equipment_by_id(equipment_id)
        if not eq:
            raise ValueError("Equipment not found")
        return eq

    @staticmethod
    def update_equipment(
            equipment_id: int,
            acting_user: Dict,
            name: Optional[str] = None,
            description: Optional[str] = None,
            quantity_total: Optional[int] = None,
            image_path: Optional[str] = None
    ) -> None:
        if not acting_user or acting_user["is_admin"] != 1:
            raise PermissionError("Only admin can update equipment")

        EquipmentService.get_by_id(equipment_id)
        equipment_repo.update_equipment(equipment_id, name, description, quantity_total, image_path)

    @staticmethod
    def delete_equipment(equipment_id: int, acting_user: Dict) -> None:
        if not acting_user or acting_user["is_admin"] != 1:
            raise PermissionError("Only admin can delete equipment")
        equipment_repo.delete_equipment(equipment_id)

    @staticmethod
    def get_available_on_date(target_date: date) -> List[Dict]:
        # Převedeme date na string (YYYY-MM-DD), protože tak to ukládáme v DB
        date_str = str(target_date)

        items = equipment_repo.get_equipment_availability(date_str)


        for item in items:
            if item["quantity_available"] < 0:
                item["quantity_available"] = 0

        return items