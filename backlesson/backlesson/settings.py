
from pathlib import Path
import psycopg2
from datetime import datetime
import json, string, random
import smtplib
from email.mime.text import MIMEText

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^w9@%n$paih!=69#ndjqq^^_&k11j^-z$yc6c#mir*450vrk2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backlesson.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backlesson.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

def sendResponse(request, resultCode, data, action="no action"):
    response = {}
    response["resultCode"] = resultCode
    response["resultMessage"] = resultMessages[resultCode]
    response["data"] = data
    response["size"] = len(data)
    response["action"] = action
    response["curdate"] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')


    return json.dumps(response, indent=4, sort_keys=True, default=str)
#   sendResponse

#Messages
resultMessages = {
    200:"Success",
    404:"Not found",
    1000 : "Burtgeh bolomjgui. Mail hayag umnu burtgeltei baina",
    1001 : "Hereglegch Amjilttai burtgegdlee. Batalgaajuulah mail ilgeegdlee. 24 tsagiin dotor batalgaajuulna.",
    1002 : "Login Successful",
    1003 : "Amjilttai batalgaajlaa",
    1004 : "Hereglegchiin ner, nuuts ug buruu baina.",
    3001 : "ACTION BURUU",
    3002 : "METHOD BURUU",
    3003 : "JSON BURUU",
    3004 : "Token-ii hugatsaa duussan. Idevhgui token baina.",
}

# db connection
def connectDB():
    con = psycopg2.connect (
        host = '192.168.0.15',
        # host = '59.153.86.251',
        dbname = 'qrlesson',
        user = 'userlesson',
        password = '123',
        port = '5938',
    )
    return con
# connectDB

# DB disconnect hiij baina
def disconnectDB(con):
    con.close()
# disconnectDB

#random string generating
def generateStr(length):
    characters = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password
# generateStr

def sendMail(recipient, subj, bodyHtml):
    sender_email = "is21d005@mandakh.edu.mn"
    sender_password = "05060109"
    recipient_email = recipient
    subject = subj
    body = bodyHtml
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subject
    html_message['From'] = sender_email
    html_message['To'] = recipient_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, html_message.as_string())
#sendMail

# def sendMail(recipientMail, subj, bodyMessage):
#     sender_email = "sw21d025@mandakh.edu.mn"
#     sender_password = "03212456"
#     recipient_email = recipientMail
#     subject = subj
#     body = bodyMessage
#     # body = """
#     # <html>
#     # <body>
#     #     <p>This is an <b>HTML</b> email sent from Python using the Gmail SMTP server.</p>
#     # </body>
#     # </html>
#     # """
#     html_message = MIMEText(body, 'html')
#     html_message['Subject'] = subject
#     html_message['From'] = sender_email
#     html_message['To'] = recipient_email
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, recipient_email, html_message.as_string())
# #sendMail