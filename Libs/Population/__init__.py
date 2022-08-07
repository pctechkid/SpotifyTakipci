# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Libs.Population.first_names import first_names
from Libs.Population.last_names  import last_names
from random                      import choice, randint

def get_people():
    first_name = choice(first_names)
    last_name  = choice(last_names)
    username   = f"{first_name[:4].title()}{randint(0,99)}{last_name[:4].title()}"

    return {
        "first_name" : first_name,
        "last_name"  : last_name,
        "username"   : username
    }