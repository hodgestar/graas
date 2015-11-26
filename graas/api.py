""" GRaaS API. """

from klein import Klein

from twisted.internet.defer import inlineCallbacks, returnValue


class GraasApi(object):

    app = Klein()

    @app.route('/', methods=['GET'])
    @inlineCallbacks
    def get_main_page(self, request):
        yield
        returnValue("Hello World!")
