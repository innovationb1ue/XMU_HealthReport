import os
from flask import Flask, current_app, send_file

from .apis import api_rep

app = Flask(__name__)
app.secret_key = 'My_Ultimate_Secret_Key'
app.register_blueprint(api_rep)
# app.register_blueprint(client_bp)

# from .config import Config
# app.logger.info('>>> {}'.format(Config.FLASK_ENV))

@app.route('/')
def index_client():
    return {'message':'index page'}


