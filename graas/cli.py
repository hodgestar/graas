""" Command for launching GRaaS. """

import sys

import click

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site

from .api import GraasApi
from .devserver import GraasServerFactory


@click.command("graas")
@click.version_option()
@click.option(
    '--host', '-h',
    default='localhost',
    help='Host to listen on')
@click.option(
    '--web-port', '-p',
    type=int, default=8080,
    help='Port for web server to listen on')
@click.option(
    '--device-port', '-d',
    type=int, default=8081,
    help='Port for device server to listen on')
@click.option(
    '--log-file', '-l',
    type=str, default=None,
    help='File to log to')
def main(host, web_port, device_port, log_file):
    """ Vumi Go Opt Out API. """
    if log_file is None:
        log_file = sys.stdout
    log.startLogging(log_file)

    site = Site(GraasApi().app.resource())
    reactor.listenTCP(web_port, site, interface=host)
    factory = GraasServerFactory()
    reactor.listenTCP(device_port, factory, interface=host)

    log.msg("Web API listening on %s:%s" % (host, web_port))
    log.msg("Device server listening on %s:%s" % (host, device_port))

    reactor.run()
