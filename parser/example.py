def verify(user):

    print("Checking user")

    return "TOKEN123"


def login(user):

    token = verify(user)

    if token:

        print("Welcome")

        return True

    return False


def main():

    login("Ash")


main()