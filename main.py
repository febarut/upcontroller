import subprocess as sp
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import time

url = ""  # dc webhooks

# SMTP Ayarları
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "your_email@gmail.com"
SMTP_PASSWORD = "your_email_password"

LOG_FILE = "server_downtime_log.txt"


def send_webhook(ip):
    data = {
        "content": "Sunucuya erişim bulunmuyor.",
        "username": ip
    }
    result = requests.post(url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"Discord webhook gönderildi: {result.status_code}")


def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = ""

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, SMTP_EMAIL, msg.as_string())
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderimi başarısız: {e}")


def log_downtime(ip):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"{timestamp} - {ip} sunucusuna erişim yok.\n")


def generate_weekly_report():
    try:
        with open(LOG_FILE, "r") as file:
            logs = file.readlines()

        if not logs:
            report = "Bu hafta hiçbir sunucu düşüşü yaşanmadı."
        else:
            report = "Haftalık Sunucu Düşüş Raporu:\n\n" + "".join(logs)

        send_email("Haftalık Sunucu Raporu", report)

        open(LOG_FILE, "w").close()
        print("Haftalık rapor oluşturuldu ve e-posta ile gönderildi.")
    except FileNotFoundError:
        print("Log dosyası bulunamadı. Henüz bir veri yok.")


def ipcheck():
    """Sunucuları kontrol et ve düşenleri bildir."""
    for ip in iplist:
        status, result = sp.getstatusoutput("ping -c1 -w2 " + str(ip))
        if status == 0:
            print(f"{ip} IP adresinden yanıt alabiliyorum.")
        else:
            print(f"{ip} IP adresinden yanıt alamıyorum.")
            send_webhook(ip)
            log_downtime(ip)
            print(f"{ip} için gerekli bilgiler loglandı ve webhook gönderildi.")


last_report_time = datetime.now()

while True:
    iplist = ['1.1.1.1', '2.2.2.2']
    ipcheck()

    # Haftalık raporu kontrol et
    now = datetime.now()
    if now - last_report_time >= timedelta(days=7):
        generate_weekly_report()
        last_report_time = now

    # 60 saniye beklemeden sonra yeniden kontrol et
    time.sleep(60)
