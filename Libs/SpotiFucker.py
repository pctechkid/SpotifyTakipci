# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from rich     import print
from requests import Session
from random   import randint
from re       import search
from Kekik    import satir_ekle

class SpotiFucker:
    def __init__(self, proxi:dict | None):
        self.oturum  = Session()
        if proxi:
            self.oturum.proxies.update(proxi)

        # proxi_ = self.oturum.get("https://httpbin.org/ip")
        # print(proxi_.json())

    def kayit_ol(self, e_posta:str, kullanici_adi:str, sifre:str):
        istek = self.oturum.post(
            url     = "https://spclient.wg.spotify.com/signup/public/v1/account",
            headers = {
                "User-Agent"   : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "Accept"       : "*/*",
                "Content-Type" : "application/x-www-form-urlencoded",
                "Referer"      : "https://www.spotify.com/"
            },
            data   = {
                "birth_day"             : f"{randint(1, 28)}",
                "birth_month"           : f"{randint(1, 12)}",
                "birth_year"            : f"{randint(1970, 2003)}",
                "collect_personal_info" : "undefined",
                "creation_flow"         : "",
                "creation_point"        : "https://www.spotify.com/uk/",
                "displayname"           : kullanici_adi,
                "email"                 : e_posta,
                "gender"                : "neutral",
                "iagree"                : "1",
                "key"                   : "a1e486e2729f46d6bb368d6b2bcda326",
                "password"              : sifre,
                "password_repeat"       : sifre,
                "platform"              : "www",
                "referrer"              : "",
                "send-email"            : "1",
                "thirdpartyemail"       : "0",
                "fb"                    : "0"
            }
        )
        veri = istek.json()

        login_token = veri["login_token"] if "login_token" in veri.keys() else None
        if not login_token:
            if "errors" in veri.keys():
                print(veri["errors"])
            else:
                print(veri)
            return False

        satir_ekle("Settings/HESAPLAR.csv", f"{e_posta},{sifre},{login_token}")

        csrf_token = self.__csrf_token        

        self.__login_auth(login_token, csrf_token)
        return True

    @property
    def __csrf_token(self):
        istek = self.oturum.get(
            url    = "https://www.spotify.com/uk/signup/",
            params = {
                "forward_url" : "https://accounts.spotify.com/en/status&sp_t_counter=1"
            }
        )
        veri = istek.text

        return search('csrfToken":"(.*?)",', veri).group(1)

    def __login_auth(self, login_token, csrf_token):
        self.oturum.post(
            url     = "https://www.spotify.com/api/signup/authenticate",
            headers = {
                "Accept"       : "*/*",
                "X-CSRF-Token" : csrf_token,
                "Content-Type" : "application/x-www-form-urlencoded",
            },
            data = {
                "splot" : login_token
            }
        )
    
        return True

    @property
    def __bearer_token(self):
        istek = self.oturum.get(
            url     = "https://open.spotify.com/get_access_token",
            headers = {
                "spotify-app-version" : "1.1.52.204.ge43bc405",
                "app-platform"        : "WebPlayer"
            },
            params  = {
                "reason"      : "transport",
                "productType" : "web_player"
            }
        )
        veri = istek.json()
    
        return None if veri["isAnonymous"] else veri["accessToken"]

    def takip_et(self, kullanici_adi:str) -> bool:
        if "/user/" in kullanici_adi:
            kullanici_adi = kullanici_adi.split("/user/")[1]

        if "?" in kullanici_adi:
            kullanici_adi = kullanici_adi.split("?")[0]

        self.kullanici_adi = kullanici_adi

        bearer = self.__bearer_token
        if not bearer:
            print("[bold red][!] Not Bearer")
            return False

        istek = self.oturum.put(
            url     = "https://api.spotify.com/v1/me/following",
            headers = {
                "authorization" : f"Bearer {bearer}",
            },
            params  = {
                "type" : "user",
                "ids"  : kullanici_adi
            }
        )

        return istek.status_code == 204
