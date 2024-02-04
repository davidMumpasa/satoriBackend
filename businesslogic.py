from models.user import User, UserModel, db
from flask import request

# Custom exception for registration errors
class RegistrationError(Exception):
    pass

# Logic for user registration
def storeUser():
    try:
        data = request.get_json()

        # Check if the email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            # Check if all required fields are present in the request
            required_fields = ['email', 'password']
            if not all(field in data for field in required_fields):
                raise RegistrationError('Missing required fields')

            # Move the import of bcrypt here
            from main import bcrypt

            email = data['email']
            password = data["password"]

            existing_user = UserModel.query.filter_by(email=data['email']).first()
            if existing_user:
                raise RecursionError('You have Already Registered')
            password = password.strip() 

            # Check password strength
            if is_strong_password(password):

                # Hash the password before storing it
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                # Create a new user
                new_user = UserModel(password=hashed_password, email=email)
                db.session.add(new_user)
                db.session.commit()

                return "Registered Successfully"
            else:
                raise RegistrationError('Weak password. Password must be strong.')
        else:
            raise RegistrationError('You need to be registered to the Academy')

    except RegistrationError as e:
        raise e

    except Exception as e:
        raise RegistrationError(str(e))

def is_strong_password(password):
    """
    Check if the password meets the strength criteria:
    - At least one uppercase letter
    - At least one special character
    - At least one digit
    - Minimum length (adjust as needed)
    """

    if (
        any(char.isupper() for char in password) and
        any(char.isdigit() for char in password) and
        any(char in '!@#$%^&*()_-+=<>?/[]{}|' for char in password) and
        len(password) >= 8 
    ):
        return True
    else:
        return False
