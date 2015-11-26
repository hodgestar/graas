""" GRaaS API. """

from klein import Klein

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.static import File


class GraasApi(object):

    app = Klein()

    @app.route('/')
    def home(self, request):
        return File("./static/index.html")

    @app.route('/static/', branch=True)
    def static(self, request):
        return File("./static")

    @app.route('/action/press', methods=['POST'])
    def action_press(self, request):
        return "Button pressed"
