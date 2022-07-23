import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(user, new):
    addr_from = 'hse.tests@yandex.ru'
    password = os.environ.get('MAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = user.email
    msg['Subject'] = 'Информация смене пароля'

    text = "Здравствуйте"
    if user.first_name != "":
        text += ", " + user.first_name
    text += ". На сайте психологических тестов от высшей школы экономики была активирована функция " \
            "'восстановить пароль' для вашего аккаунта."
    text += "\nВаш новый пароль: " + new + ". Вы сможете заменить его в вашем личном кабинете."
    msg.attach(MIMEText(text, 'plain'))
    try:
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(addr_from, password)
        server.sendmail(addr_from, user.email, msg.as_string())
        server.quit()
    except Exception:
        return 1
    return 0
