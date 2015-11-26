""" GRaaS API. """

import pkg_resources

from klein import Klein

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python.filepath import FilePath
from twisted.web.static import File


class GraasApi(object):

    app = Klein()
    static_path = pkg_resources.resource_filename(__name__, "static")

    @app.route('/')
    def home(self, request):
        p = FilePath(self.static_path).child("index.html")
        return p.open().read()

    @app.route('/static/', branch=True)
    def static(self, request):
        return File(self.static_path)

    @app.route('/action/press', methods=['POST'])
    def action_press(self, request):
        return "Button pressed"
