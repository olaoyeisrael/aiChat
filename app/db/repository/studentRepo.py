from .base import BaseRepository
from app.db.models.students import Student
from app.db.schema.students import StudentCreate

class StudentRepository(BaseRepository):
    def create_student(self, student_data : StudentCreate):
        newStudent = Student(**student_data.model_dump(exclude_none=True))

        self.session.add(instance=newStudent)
        self.session.commit()
        self.session.refresh(instance=newStudent)

        return newStudent

    def user_exist_by_regn(self, registration_no : str) -> bool:
        student = self.session.query(Student).filter_by(registration_no=registration_no).first()
        return bool(student)

    def get_user_by_regn(self, registration_no : str) -> Student:
        user = self.session.query(Student).filter_by(registration_no=registration_no).first()
        return user
    def get_user_by_id(self, student_id : int) -> Student:
        user = self.session.query(Student).filter_by(id=student_id).first()
        return user
   
    def update_password(self, student_id: int, new_hashed_password: str) -> Student:
        student = self.get_user_by_id(student_id)
        student.password = new_hashed_password
        self.session.commit()
        self.session.refresh(student)
        return student