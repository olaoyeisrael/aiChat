from .base import BaseRepository
from app.db.models.admin import Admin
from app.db.schema.admin import UserInCreate

class AdminRepository(BaseRepository):
    def create_admin(self, admin_data : UserInCreate):
        newAdmin = Admin(**admin_data.model_dump(exclude_none=True))

        self.session.add(instance=newAdmin)
        self.session.commit()
        self.session.refresh(instance=newAdmin)

        return newAdmin

    def user_exist_by_email(self, email : str) -> bool:
        admin = self.session.query(Admin).filter_by(email=email).first()
        return bool(admin)

    def get_user_by_email(self, email : str) -> Admin:
        admin = self.session.query(Admin).filter_by(email=email).first()
        return admin
    def get_user_by_id(self, admin_id : int) -> Admin:
        user = self.session.query(Admin).filter_by(id=admin_id).first()
        return user
        