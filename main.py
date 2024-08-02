import subprocess as sp
import requests

url = "" #webhook

def send_webhook(ip):
    data = {
        "content" : "Sunucuya erişim bulunmuyor.",
        "username" : ip
    }
    result = requests.post(url, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"{result.status_code}.")

def ipcheck():
    for ip in iplist:
        status,result = sp.getstatusoutput("ping -c1 -w2 " + str(ip))
        if status == 0:
            print(str(ip) + " IP adresinden yanıt alabiliyorum.")
        else:
            print(str(ip) + " IP adresinden yanıt alamıyorum.")
            send_webhook(ip)
            print("Gerekli webhook paylaşıldı.")



while True:
    iplist = ['1.1.1.1', '2.2.2.2'] #ip list
    ipcheck()
