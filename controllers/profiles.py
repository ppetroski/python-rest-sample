from components.framework.baseController import BaseController
from models.profile import Profile


class Profile(BaseController):
    # At this time all we need to do is define the model to enable CRUD endpoints for it
    _model = Profile
