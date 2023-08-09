from flask import Flask
import secrets

app_secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = app_secret_key