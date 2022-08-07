# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Libs.SpotiFucker import SpotiFucker
from Libs.Population  import get_people

from CLI     import konsol
from os.path import isfile
from random  import choice

def dosya_2_set(dosya:str) -> set[str] | None:
    try:
        return {satir.strip().replace("\n", "") for satir in open(dosya, "r", encoding="utf-8") if satir.strip()} if isfile(dosya) else None
    except Exception:
        return None

Proxy_File = list(dosya_2_set("Settings/PROXY.txt")) if dosya_2_set("Settings/PROXY.txt") else None

if not Proxy_File:
    konsol.log("[bold red] PROXY.txt Bulunamadı!\n")

def ProxyVer(selenium:bool=False) -> dict[str, str] | None:
    if not Proxy_File:
        return None

    if selenium:
        return choice(Proxy_File)

    proxi_part = choice(Proxy_File).split(":")

    match len(proxi_part):
        case 4:
            p_ip, p_port, p_user, p_pass = proxi_part
            proxi = {
                'http'   : f'http://{p_user}:{p_pass}@{p_ip}:{p_port}',
                'https'  : f'http://{p_user}:{p_pass}@{p_ip}:{p_port}',
                # 'socks5' : f'socks5://{p_user}:{p_pass}@{p_ip}:{p_port}',
            }
        case 2:
            p_ip, p_port = proxi_part
            proxi = {
                'http'  : f'http://{p_ip}:{p_port}',
                'https' : f'http://{p_ip}:{p_port}',
                # 'socks5' : f'socks5://{p_ip}:{p_port}',
            }
        case _:
            return None

    return proxi