from flask import Flask
from LoginAuth import user_auth
from AccountController import account_controller
from flask_cors import CORS
running_app = Flask(__name__)
running_app.register_blueprint(user_auth, url_prefix='/loginService')
running_app.register_blueprint(account_controller, url_prefix='/accountService')
CORS(running_app)
if __name__ == '__main__':
    running_app.run(host='localhost')


