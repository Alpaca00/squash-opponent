import os


class DataLogin:
    class CorrectLogin:
        email = os.environ["USER_EMAIL"]
        pw = os.environ["USER_PASSWORD"]
        exp_result = 'Hi, Oleg.'
        endpoint = '/account/'

    class SignUp:
        email = 'test00000000@gmail.com'
        name = 'John'
        pw = 'qwerty12345'
        exp_result = 'Thanks for registering'
        endpoint = '/register/unconfirmed'

    class RecoveryPassword:
        email = 'test00000000@gmail.com'
        exp_result = 'Security code has been sent to the mail.'
        endpoint = '/recovery-password/test00000000%gmail.com'