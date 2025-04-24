from pydantic import BaseModel

class StudentCreate(BaseModel):
    registration_no: str
    password: str

class StudentInLogin(BaseModel):
    registration_no: str
    password: str


# class UserInCreate(BaseModel):
#     registration_no: str
#     role: str

class StudentOutput(BaseModel):
    id: int
    registration_no: str
    role: str




class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
