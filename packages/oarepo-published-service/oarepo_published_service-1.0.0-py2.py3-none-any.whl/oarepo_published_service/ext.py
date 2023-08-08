class OARepoPublishedService(object):
    """OARepo extension of published service."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.service = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["oarepo-published-service"] = self

    def init_config(self, app):
        """Initialize configuration."""