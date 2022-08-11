# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from CLI        import konsol, hata_yakala, cikis_yap
from threading  import Thread, active_count
from threading  import enumerate as threads
from Kekik      import proxy_ver, kisi_ver
from Libs       import SpotiFucker
from random     import choices
from string     import ascii_letters, digits

basarili = 0
def basla(profile_link:str):
    global basarili

    kisi = kisi_ver("tr")
    # rastgele = "".join(choices(ascii_letters + digits, k=4))

    spoti = SpotiFucker(proxy_ver("Settings/PROXY.txt", "requests"))

    try:
        if not spoti.kayit_ol(f"{kisi['kullanici_adi']}@gmail.com", f"{kisi['isim']} {kisi['soyisim']}", "KekikAkademi"):
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
        profile_link  = konsol.input("[yellow]Profil Linki : ")
        thread_sayisi = int(konsol.input("[magenta]Thread Sayısı : "))
        print()

        while True:
            if active_count() <= thread_sayisi:
                Thread(target=basla, args=(profile_link,), daemon=True).start()

        # while len(threads()) - 1:
        #     pass

        cikis_yap()
    except Exception as hata:
        hata_yakala(hata)