from Dummy_ERP.app import User, Performance, db


def test_dummy_erp_login_page(dummy_erp_client):
    """Test login page loads successfully."""
    response = dummy_erp_client.get('/')
    assert response.status_code == 200


def test_dummy_erp_login_invalid(dummy_erp_client):
    """Test login with wrong credentials."""
    response = dummy_erp_client.post('/login', data={
        'username': 'unknown_user',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200
    assert b"Invalid Credentials!" in response.data


def test_dummy_erp_login_valid_and_dashboard(dummy_erp_client):
    """Test login with valid teacher credentials and accessing dashboard."""
    # Ensure default user exists
    user = User.query.filter_by(username='omkar').first()
    if not user:
        user = User(username='omkar', password='123', role='Subject Teacher', subject='Data Science')
        db.session.add(user)
        db.session.commit()

    login_resp = dummy_erp_client.post('/login', data={
        'username': 'omkar',
        'password': '123'
    }, follow_redirects=True)

    assert login_resp.status_code == 200

    # Test dashboard route
    dashboard_resp = dummy_erp_client.get('/dashboard')
    assert dashboard_resp.status_code == 200

    # Test view data
    view_resp = dummy_erp_client.get('/view_data')
    assert view_resp.status_code == 200

    # Test logout
    logout_resp = dummy_erp_client.get('/logout', follow_redirects=True)
    assert logout_resp.status_code == 200


def test_dummy_erp_submit_performance(dummy_erp_client):
    """Test submitting student performance record."""
    submit_resp = dummy_erp_client.post('/submit', data={
        'student_name': 'Test Student',
        'attendance': '88',
        'ut1_marks': '18',
        'ut2_marks': '19',
        'sem_marks': '75',
        'subject': 'Data Science'
    }, follow_redirects=False)

    assert submit_resp.status_code == 302
    assert submit_resp.headers['Location'] == '/dashboard'

    perf = Performance.query.filter_by(student_name='Test Student').first()
    assert perf is not None
    assert perf.attendance == 88
