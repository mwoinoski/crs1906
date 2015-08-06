"""
twisted_tcp_server.py - sample program from the Twisted event-driven
networking engine.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from twisted.internet import protocol, reactor, endpoints

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

endpoints.serverFromString(reactor, "tcp:1234").listen(EchoFactory())
reactor.run()
