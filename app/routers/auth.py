from fastapi import APIRouter, Depends
from app.db.schema.admin import UserInCreate, UserInLogin, UserWithToken, UserOutput
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.service.adminService import AdminService
from app.db.schema.students import StudentCreate, StudentOutput, StudentInLogin, ChangePasswordRequest
from app.service.studentService import StudentService
from app.util.protectRoute import get_current_user
authRouter = APIRouter()

@authRouter.post("/login/admin", status_code=200, response_model=UserWithToken)
def login(loginDetails : UserInLogin, session: Session = Depends(get_db)):
    try:
        return AdminService(session=session).login(login_details=loginDetails)
    except Exception as error:
        print(error)
        raise error
    
@authRouter.post("/login/student", status_code=201, response_model=UserWithToken)
def student_login(
    credentials: StudentInLogin ,
    session : Session = Depends(get_db)
):
    try:
        return StudentService(session=session).login(login_details=credentials)
    except Exception as error:
        print(error)
        raise error
    

@authRouter.post("/signup/admin", status_code=201, response_model=UserOutput)
def signUp(signUpDetails : UserInCreate, session : Session = Depends(get_db)):
    try:
        return AdminService(session=session).signup(user_details=signUpDetails)
    except Exception as error:
        print(error)
        raise error


@authRouter.post("/signup/student", status_code=201, response_model=StudentOutput)
def signUp(signUpDetails : StudentCreate, session : Session = Depends(get_db)):
    try:
        return StudentService(session=session).signup(user_details=signUpDetails)
    except Exception as error:
        print(error)
        raise error 
    
@authRouter.post("/change_password",)
def changePassword(passwordDetails:ChangePasswordRequest , session: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    try:
        studentId = user.id
        return StudentService(session=session).change_password(student_id=studentId,passwords=passwordDetails)
    except Exception as error:
        raise error
    
    
   