
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class StudentSubject(Base):
    __tablename__ = 'student_subject'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    student = relationship('Student', backref='student_subjects')
    subject = relationship('Subject', backref='subject_students')

DATABASE_URL = 'postgresql://liliakasirina:lilia0909@localhost/prjctr_lessons_students'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.query(StudentSubject).delete()
session.query(Subject).delete()
session.query(Student).delete()
session.commit()

students = [Student(name="Alice", age=19), Student(name="Jon", age=21), Student(name="Lilia", age=23)]
subjects = [Subject(name="Mathematics"), Subject(name="English"), Subject(name="English")]
session.add_all(students + subjects)
session.commit()

student_subjects = [
    StudentSubject(student_id=students[0].id, subject_id=subjects[0].id),
    StudentSubject(student_id=students[1].id, subject_id=subjects[1].id),
    StudentSubject(student_id=students[2].id, subject_id=subjects[2].id)
]
session.add_all(student_subjects)
session.commit()

all_students = session.query(Student).all()
for student in all_students:
    subject_names = [ss.subject.name for ss in student.student_subjects]
    print(f"Student Name: {student.name}, Age: {student.age}, Subjects: {subject_names}")

english_students = session.query(Student).\
    join(StudentSubject).\
    join(Subject).\
    filter(Subject.name == 'English').\
    distinct().all()

print("\nStudents who attended English classes:")
for student in english_students:
    print(f"Student Name: {student.name}, Age: {student.age}")

session.close()
