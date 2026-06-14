from server.app import running_app

import os

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', 'localhost')
    port = int(os.environ.get('FLASK_PORT', 5000))
    running_app.run(host=host, port=port)
