# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

db = SQLAlchemy()

# config_name
def create_app():

    app = Flask(__name__)

    # db init
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    sqlalchemy_uri = os.getenv('SQLALCHEMY_DATABASE_URI', None)
    if sqlalchemy_uri is None:
        print('Specify SQLALCHEMY_DATABASE_URI as environment variable.')
        sys.exit(1)

    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_uri

    db.init_app(app)
    register_linebot()

    @app.route("/callback", methods=['POST'])
    def callback():
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']
        print('1')
        
        # get request body as text
        body = request.get_data(as_text=True)
        print('2')
        app.logger.info("Request body: " + body)
        print('3')

        # handle webhook body
        try:
            print(f'body : {body}')
            print(f'signature : {signature}')
            handler.handle(body, signature)
            print('4')
        except InvalidSignatureError:
            abort(400)

        return 'OK'

    @app.route("/cdb", methods=['GET'])
    def cdb():
        db.create_all()
        return 'OK'

    # app = Flask(__name__)

    # # 設定config
    # app.config.from_object(config[config_name])

    # # Initialize Celery
    # celery.conf.update(app.config)

    # register_extensions(app)
    # register_blueprints(app)
    # register_celery_beat(celery)
    # register_errorhandlers(app)
    # register_i18n(app)

    # @app.route("/")
    # def index_redirect():
    #     return redirect(url_for("index.article", lang_code="zh"))

    return app

# app
def register_linebot():
    @handler.add(MessageEvent, message=TextMessage)
    def message_text(event):
        save_text(event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

def save_text(text):
    from .models.MsgText import MsgText
    MsgText.save_message(text)
    return


