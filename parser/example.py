def login(user):

    token = verify(user)

    if token:

        print("Welcome")

        return True

    return False