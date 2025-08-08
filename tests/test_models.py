from app.models import User


def test_password_hashing(app):
    """
    Tests the password setting and checking functionality of the User model.
    """
    with app.app_context():
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')

        assert u.check_password('dog') is False
        assert u.check_password('cat') is True
