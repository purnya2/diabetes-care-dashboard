def authenticate_user(username, password, login_as_doctor=False):
    """
    Basic authentication function
    TODO: it should check by accessing a database, or more simply, a list of valid users and doctors
    """
    if login_as_doctor:
        if username == "doctor" and password == "password":
            return True
    else:
        if username == "user" and password == "user":
            return True
    return False


def logout_user():
    """
    Handle user logout
    TODO: Clear session data
    """
    # TODO: Implement logout logic
    pass