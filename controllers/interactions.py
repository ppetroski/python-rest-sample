from components.framework.baseController import BaseController
from models.interaction import Interaction


class Interaction(BaseController):
    # At this time all we need to do is define the model to enable CRUD endpoints for it
    _model = Interaction
