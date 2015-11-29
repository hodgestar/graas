""" GRaaS device registry server.

    Devices connect to this server and register themselves.
"""

import re
import types

from twisted.internet.defer import maybeDeferred
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver


class GraasCommand(object):

    COMMAND = '!'
    REPLY = '?'
    INFORM = '>'

    GTYPES = set([COMMAND, REPLY, INFORM])

    def __init__(self, name, *args, **kw):
        self.gtype = kw.pop('gtype', self.COMMAND)
        self.gid = kw.pop('gid', None)
        self.name = name
        self.args = args
        assert self.gtype in self.GTYPES
        assert not kw

    def __str__(self):
        gid = '' if not self.gid else '[%s]' % self.gid
        args = ' '.join(self.args)
        return '%s%s%s %s' % (self.gtype, self.name, gid, args)


class GraasParser(object):

    NAME_RE = re.compile(
        r'(?P<gtype>[!?>])'
        r'(?P<name>[a-z][a-zA-Z0-9\-]*)'
        r'(\[(?P<gid>[a-zA-Z0-9\-]+)\])?')

    def parse(self, line):
        parts = line.split()
        name, args = parts[0], parts[1:]
        m = self.NAME_RE.match(name)
        if not m:
            return None
        return GraasCommand(
            m.group('name'), *args,
            gtype=m.group('gtype'), gid=m.group('gid'))


class GraasProtocol(LineReceiver):

    MAX_LENGTH = 16384
    delimiter = '\n'

    def __init__(self):
        self.parser = GraasParser()

    def lineReceived(self, line):
        cmd = self.parser.parse(line)
        if cmd is None:
            return
        if cmd.gtype == GraasCommand.COMMAND:
            handler = getattr(
                self, 'command_%s' % cmd.name, 'fallback_command')
        elif cmd.gtype == GraasCommand.INFORM:
            handler = getattr(
                self, 'inform_%s' % cmd.name, 'fallback_inform')
        else:
            handler = getattr(
                self, 'reply_%s' % cmd.name, 'fallback_reply')
        d = maybeDeferred(handler, cmd)
        d.addErrback(self.fallback_error, cmd)
        d.addCallback(self.send_commands, cmd)

    def fallback_command(self, cmd):
        return GraasCommand(
            cmd.name, ['fail', 'unknown-command'], gtype=GraasCommand.REPLY)

    def fallback_inform(self, cmd):
        pass

    def fallback_reply(self, reply):
        pass

    def fallback_error(self, f, orig_cmd):
        if orig_cmd.gtype == GraasCommand.COMMAND:
            return GraasCommand(
                orig_cmd.name, 'fail', 'server-error',
                gtype=GraasCommand.REPLY, gid=orig_cmd.gid)

    def send_commands(self, msgs, orig_cmd):
        if isinstance(msgs, types.NoneType):
            msgs = []
        elif isinstance(msgs, GraasCommand):
            msgs = [msgs]
        if orig_cmd.gtype == GraasCommand.COMMAND:
            for msg in msgs:
                msg.name = orig_cmd.name
                msg.gid = orig_cmd.gid
        for msg in msgs:
            self.sendLine(str(msg))


class GraasServerProtocol(GraasProtocol):
    def command_version(self, cmd):
        return GraasCommand('foo', 'ok', '0.0.1', gtype=GraasCommand.REPLY)


class GraasServerFactory(ServerFactory):
    protocol = GraasServerProtocol
