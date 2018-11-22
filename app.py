from flask import Flask
from controller import blueprint

app = Flask("__name__")
app.register_blueprint(blueprint)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
