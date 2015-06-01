from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.protocols import policies
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet import reactor, interfaces, protocol, error, defer
from twisted.python import log, failure, filepath
'''
S:Server
C:Client

S->C    PUSH filename size\r\n
C->S    ACK\r\n
S->C    file contents

C->S    LIST
S->C    LIST contents

C->S    PUSH filename size\r\n
S->C    ACK\r\n
C->S    file contents
'''
class SyncProtocol(object, LineReceiver, policies.TimeoutMixin):
    
    def __init__(self, factory):
        self.factory = factory
        
    def lineReceived(self, line):
        print "lineReceived"
        #self.resetTimeout()
        #self.pauseProducing()
        
        def processSucceeded(result):
            print "processSucceeded"
            pass
            
        def processFailed(err):
            print "processFailed"
            pass
        
        def allDone(ignored):
            print "allDone"
            pass
        spaceIndex = line.find(' ')
        if spaceIndex != -1:
            cmd = line[:spaceIndex]
            args = (line[spaceIndex + 1:],)
        else:
            cmd = line
            args = ()
        
        d = defer.maybeDeferred(self.processCommand, cmd, *args)
        d.addCallbacks(processSucceeded, processFailed)
        d.addErrback(log.err)
        reactor.callLater(0, d.addBoth, allDone)
        pass
        
    def processCommand(self, cmd, *params):        
        cmd = cmd.upper()
        print "cmd = %s" %(cmd,)
        def call_sync_command(command):
            print "call_sync_command"
            method = getattr(self, "sync_" + command,None)
            print method
            if method is not None:
                print "1111"
                return method(*params)
                print "2222"
            return defer.fail("Cmd not implemented error")
        
        
        return call_sync_command(cmd)
        
        
    
    def sync_LIST(self,u):
        print "sync list cmd"
    
    def sync_PUSH(self):
        print "sync PUSH cmd"
        
    def connectionMade(self):
        pass
    
    def connectionLost(self, reason):
        pass
        
    def pauseProducing(self):
        self.transport.pauseProducing()
######################################################    
class SyncFactory(Factory):
    
    def buildProtocol(self, addr):
        return SyncProtocol(self)
        


endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(SyncFactory())
reactor.run()