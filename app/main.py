import math
import smtplib
import ssl
from email.header import Header
from email.mime.text import MIMEText
import os
from time import sleep
import requests
from dotenv import load_dotenv
import prometheus_client
from flask import Flask
import threading
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

registry = prometheus_client.CollectorRegistry()

AVAILABLE_STATION = prometheus_client.Gauge('available_station', 'A description for amit metric', "", registry=registry)
TOTAL_STATION = prometheus_client.Gauge('total_station', 'A description for amit metric', "", registry=registry)

load_dotenv()
env_email_from = os.environ['EMAIL_FROM']
env_email_pass = os.environ['EMAIL_PASS']
env_email_to = os.environ['EMAIL_TO']
env_auth = os.environ['AUTH']
env_url_station = os.environ['URL_STATION']


def message(data_station_json, is_full):
    if is_full:
        subject = "אין עמדות טעינה זמינות!"
        body = f"""\
                  היי,
                  כל עמדות הטעינה בכתובת {data_station_json["FriendlyName"]} תפוסות """
    else:
        subject = "עמדת טעינה זמינה!"
        body = f"""\
               היי,
               יש {data_station_json["AvailableEvses"]} מתוך {data_station_json["TotalEvses"]} עמדות טעינה זמינות ברגע זה בכתובת {data_station_json["FriendlyName"]}"""
    return [subject, body]


def send_email(data_station_json, is_full):
    smtp_server = "smtp.gmail.com"
    port = 587
    from_email = env_email_from
    to_email = env_email_to
    password = env_email_pass
    [subject, body] = message(data_station_json, is_full)
    # Create the email message
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_email
    msg['To'] = to_email

    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)  # Secure the connection
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        print("send email.")
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


def get_charging_station():
    # Use a breakpoint in the code line below to debug your script.
    url_station = env_url_station
    data = {
        "headers": {
            "accept": "application/json, text/plain, */*",
            "authorization": env_auth,
        },
        "referrer": "https://user.evedge.co.il/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": "",
        "method": "GET",
        "mode": "cors",
        "credentials": "include"
    }
    response = requests.get(url=url_station, params=data)
    response_json = response.json()
    return response_json


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def run():
    pre_status = -1
    while True:
        data_station_json = get_charging_station()
        availableEvses = data_station_json["AvailableEvses"]
        totalEvses = data_station_json['TotalEvses']
        AVAILABLE_STATION.set(availableEvses)
        TOTAL_STATION.set(totalEvses)
        if availableEvses: is_full = 0
        else: is_full = 1
        if pre_status != is_full:
            pre_status = is_full
            send_email(data_station_json, is_full)
            print(data_station_json)
        print(f"Check position status {availableEvses} / {totalEvses}")
        print("Sleep.")
        sleep(300)  # 5
        print("Wake up.")


def start_flask():
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app(registry)
    })
    app.run(debug=False, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
    run()
