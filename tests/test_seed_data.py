from seed_data import seed_database
from models import User, Class, Subject, Student
from app import app


def test_seed_database_execution():
    """Verify seed_database populates HOD, classes, teachers and students."""
    seed_database()

    with app.app_context():
        # Check HOD
        hod = User.query.filter_by(role="hod").first()
        assert hod is not None
        assert hod.username == "hod_admin"

        # Check Classes
        classes = Class.query.all()
        assert len(classes) == 3

        # Check Subject Teachers
        teachers = User.query.filter_by(role="subject_teacher").all()
        assert len(teachers) == 12

        # Check Subjects
        subjects = Subject.query.all()
        assert len(subjects) == 12

        # Check Students
        students = Student.query.all()
        assert len(students) == 5
