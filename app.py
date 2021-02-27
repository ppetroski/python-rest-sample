import logging

from flask import Flask
from flask_restful import Api

from controllers.interactions import Interaction
from controllers.profiles import Profile

# Who doesn't like logging? Let's configure it so it's available
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)

# Endpoint Routes go here
api.add_resource(Profile, '/profile', '/profile/<uuid>')
api.add_resource(Interaction, '/interaction', '/interaction/<uuid>')

# Required if running manually. Not required if run within Docker
if __name__ == '__main__':
    app.run()
