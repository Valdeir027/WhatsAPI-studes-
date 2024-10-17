from decouple import config


class settings:

    TOKEN_ACESS = config('ACESS_TOKEN')

    NUMBER= config('NUMBER')
    NUMBER_ID= config('NUMBER_ID')