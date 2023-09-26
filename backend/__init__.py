import os

from flask import Flask, g
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
app.config.from_mapping(
    SECRET_KEY='dev_SECRETE',
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://new_admin:admin-pass@database-1/studysync_dev_db',
    SQLALCHEMY_ECHO=False
)
# print('__________[[[[[[[[!!--DEBUGGING--!!]]]]]]]]___________')
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)
# print('__________[[[[[[[[!!--DEBUGGING--!!]]]]]]]]___________')

socketio = SocketIO(app)

with app.app_context():
    from backend.routes.api import api_bp
    # from backend.routes.api.chat import socketio
    from backend.routes.auth.auth import auth_bp

# print('[[[###+++DEBUGGING+++###]]]]___init___')
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)


@socketio.on('message')
def handle_message(data):
    print('[[[###+++DEBUGGING+++###]]]]')
    emit('message', data, broadcast=True)
    print('[[[###+++DEBUGGING+++###]]]]')

@app.route('/')
def serve_react_app():
    return app.send_static_file('index.html')





if __name__ == '__main__':
    socketio.run(app, debug=True)