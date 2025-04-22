from app.db.repository.adminRepo import AdminRepository
from app.db.schema.admin import UserOutput, UserInCreate, UserInLogin, UserWithToken
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException

class AdminService:
    def __init__(self, session : Session):
        self.__adminRepository = AdminRepository(session=session)
    
    def signup(self, user_details : UserInCreate) -> UserOutput:
        if self.__adminRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400, detail="Please Login")
        
        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password
        return self.__adminRepository.create_admin(admin_data=user_details)
    
    def login(self, login_details : UserInLogin) -> UserWithToken:
        if not self.__adminRepository.user_exist_by_email(email=login_details.email):
            raise HTTPException(status_code=400, detail="Please create an Account")
        
        admin = self.__adminRepository.get_user_by_email(email=login_details.email)
        if HashHelper.verify_password(plain_password=login_details.password, hashed_password=admin.password):
            token = AuthHandler.sign_jwt(user_id=admin.id, role=admin.role)
            if token:
                return UserWithToken(token=token)
            raise HTTPException(status_code=500, detail="Unable to process request")
        raise HTTPException(status_code=400, detail="Please check your Credentials")
    
    def get_user_by_id(self, admin_id : int):
        admin = self.__adminRepository.get_user_by_id(admin_id=admin_id)
        if admin:
            return admin
        raise HTTPException(status_code=400, detail="Admin is not available")