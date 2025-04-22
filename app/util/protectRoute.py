from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.service.adminService import AdminService
from app.service.studentService import StudentService
from app.core.database import get_db
from app.db.schema.admin import UserOutput
from app.db.schema.students import StudentOutput 

AUTH_PREFIX = 'Bearer '

def get_current_user(
        session : Session = Depends(get_db), 
        authorization : Annotated[Union[str, None] , Header()] = None 
) -> UserOutput:
    auth_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Authentication Credentials"
    )
   
    if not authorization:
        raise auth_exception

    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    payload = AuthHandler.decode_jwt(token=authorization[len(AUTH_PREFIX):])

    if not payload or "user_id" not in payload or "role" not in payload:
        raise auth_exception
    try:
        if payload["role"] == "admin":
            admin = AdminService(session=session).get_user_by_id(payload["user_id"])
            return UserOutput(
                id = admin.id,
                first_name=admin.first_name,
                last_name=admin.last_name,
                email=admin.email,
                role= admin.role
            )
        elif payload["role"] == "student":
            student = StudentService(session=session).get_user_by_id(payload["user_id"])
            return StudentOutput(
                id=student.id,
                registration_no=student.registration_no,
                role= student.role,
            )
    except Exception:
        raise auth_exception
    raise auth_exception

    