import random
import string

def random_string(n):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )


