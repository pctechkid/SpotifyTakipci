# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from CLI       import konsol, hata_yakala, cikis_yap
from threading import Thread
from threading import enumerate as threads
from Libs      import get_people, SpotiFucker, ProxyVer
from random    import choices
from string    import ascii_letters, digits

basarili = 0

def basla(profile_link:str):
    global basarili

    kisi     = get_people()
    # rastgele = "".join(choices(ascii_letters + digits, k=4))

    spoti = SpotiFucker(ProxyVer())

    try:
        if not spoti.kayit_ol(f"{kisi['username']}@gmail.com", f"{kisi['first_name']} {kisi['last_name']}", "KekikAkademi"):
            return False
    except Exception as hata:
        konsol.log(f"[bold red][!] « {type(hata).__name__} »")
        return False

    if spoti.takip_et(profile_link):
        basarili += 1
        konsol.log(f"[green][{basarili}] » {spoti.kullanici_adi}")    

    return True

if __name__ == "__main__":
    try:
        profile_link  = konsol.input("[yellow]Profile Link : ")
        thread_sayisi = int(konsol.input("[magenta]Thread Count : "))

        for _ in range(thread_sayisi):
            Thread(target=basla, args=(profile_link,), daemon=False).start()

        while len(threads()) - 1:
            pass

        cikis_yap()
    except Exception as hata:
        hata_yakala(hata)