from app.db.repository.studentRepo import StudentRepository
from app.db.schema.admin import UserWithToken
from app.db.schema.students import StudentOutput, StudentCreate, StudentInLogin
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException


class StudentService:
    def __init__(self, session : Session):
        self.__studentRepository = StudentRepository(session=session)
    
    def signup(self, user_details : StudentCreate) -> StudentOutput:
        if self.__studentRepository.user_exist_by_regn(registration_no=user_details.registration_no):
            raise HTTPException(status_code=400, detail="Student already exists")
        
        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password
        return self.__studentRepository.create_student(student_data=user_details)
    
    # Student should login in registration no
    
    def login(self, login_details : StudentInLogin) -> UserWithToken:
        if not self.__studentRepository.user_exist_by_regn(registration_no=login_details.registration_no):
            raise HTTPException(status_code=400, detail="Please seek help from the admin")
        student = self.__studentRepository.get_user_by_regn(registration_no=login_details.registration_no)
        if HashHelper.verify_password(plain_password=login_details.password, hashed_password=student.password):
            token = AuthHandler.sign_jwt(user_id=student.id, role=student.role)
            if token:
                return UserWithToken(token=token)
            raise HTTPException(status_code=500, detail="Unable to process request")
        raise HTTPException(status_code=400, detail="Please check your Credentials")
    
     
       
    
    def get_user_by_id(self, student_id : int):
        student = self.__studentRepository.get_user_by_id(student_id=student_id)
        if student:
            return student
        raise HTTPException(status_code=400, detail="Student is not available")