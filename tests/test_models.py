from models import db, User, Class, Subject, Student, Performance


def test_create_user(app):
    """Test user model creation and attributes."""
    with app.app_context():
        user = User(
            username="teacher_test",
            password="securepassword",
            role="subject_teacher",
            name="Test Teacher"
        )
        db.session.add(user)
        db.session.commit()

        retrieved = User.query.filter_by(username="teacher_test").first()
        assert retrieved is not None
        assert retrieved.role == "subject_teacher"
        assert retrieved.name == "Test Teacher"


def test_class_and_relationships(app):
    """Test Class model, teacher linking, and relationships."""
    with app.app_context():
        ct = User(
            username="class_teacher_1",
            password="password",
            role="class_teacher",
            name="Class Teacher"
        )
        db.session.add(ct)
        db.session.commit()

        classroom = Class(name="CS-A", class_teacher_id=ct.id)
        db.session.add(classroom)
        db.session.commit()

        st = User(
            username="sub_teacher_1",
            password="password",
            role="subject_teacher",
            name="Sub Teacher"
        )
        db.session.add(st)
        db.session.commit()

        subject = Subject(name="Operating Systems", class_id=classroom.id, teacher_id=st.id)
        student = Student(roll_no="ROLL101", name="Alice", class_id=classroom.id)
        db.session.add_all([subject, student])
        db.session.commit()

        # Verify relationships
        assert len(classroom.students) == 1
        assert classroom.students[0].name == "Alice"
        assert len(classroom.subjects) == 1
        assert classroom.subjects[0].name == "Operating Systems"
        assert subject.classroom.name == "CS-A"
        assert subject.teacher.name == "Sub Teacher"


def test_performance_model(app):
    """Test Student and Performance records."""
    with app.app_context():
        teacher = User(username="t1", password="p", role="subject_teacher", name="T1")
        classroom = Class(name="DS-B")
        db.session.add_all([teacher, classroom])
        db.session.commit()

        subject = Subject(name="Data Science", class_id=classroom.id, teacher_id=teacher.id)
        student = Student(roll_no="DS01", name="Bob", class_id=classroom.id)
        db.session.add_all([subject, student])
        db.session.commit()

        record = Performance(
            student_id=student.id,
            subject_id=subject.id,
            attendance=85,
            ut1_marks=18.5,
            ut2_marks=19.0,
            sem_marks=78.5
        )
        db.session.add(record)
        db.session.commit()

        saved_student = Student.query.filter_by(roll_no="DS01").first()
        assert len(saved_student.performance_records) == 1
        perf = saved_student.performance_records[0]
        assert perf.attendance == 85
        assert perf.ut1_marks == 18.5
        assert perf.sem_marks == 78.5
