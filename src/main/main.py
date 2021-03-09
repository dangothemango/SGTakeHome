import selectors, socket, uuid
from .event.seats import *

HOST, PORT = '', 8099
FAILURE = b'FAIL'
SUCCESS = b'OK'

#This probably doesnt need an identifier but in theory this could support multiple events simulaneously
seatReservations = SeatReservations(str(uuid.uuid4()))

#supports constant time lookup of seat actions, not super extensible though and only works with one event
#this could be generated dynamically but it seems like overkill for this assignment
verbs = {
    b'QUERY': seatReservations.query,
    b'RESERVE': seatReservations.reserve,
    b'BUY': seatReservations.buy
}

def parseCommand(command):
    splitCommand = command.split(b': ')
    verb = splitCommand[0]
    if (len(splitCommand) != 2 or verb not in verbs or len(splitCommand[1]) == 0):
        return None, None
    predicate = splitCommand[1]
    return verb, predicate

def processCommand(command):
    verb, predicate = parseCommand(command)
    if (verb == None):
        return FAILURE
    result, data = verbs[verb](predicate)
    if (not result):
        return FAILURE
    return bytes(data, 'UTF8') if data != None else SUCCESS
    
def startSyncronousServer():
    selector = selectors.DefaultSelector()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((HOST,PORT))
    listener.listen()
    listener.setblocking(False)
    selector.register(listener, selectors.EVENT_READ, data=None)
    print("Listening on port:", PORT)
    eventLoop(selector)
    return selector

def loadNewConnection(selector, key):
    sock = key.fileobj
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = { 'out':b'', 'in':b'', 'addr':addr }
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, events, data=data)
    return conn

def getFirstCommandFromData(data):
    i=data.find(b'\n')
    if (i == -1):
        return None, data
    return data[:i], data[i+1:]

def processAllCommands(data):
    command, data['in'] = getFirstCommandFromData(data['in']) 
    while (command):
        data['out'] += processCommand(command)
        data['out'] += b'\n'
        command, data['in'] = getFirstCommandFromData(data['in'])

def processExistingConnection(selector, key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        receivedData = None
        try:
            receivedData = sock.recv(1024)
        except ConnectionResetError:
            receivedData = None
        if receivedData:
            data['in'] += receivedData
            processAllCommands(data)
        else:
            print('closing connection', data['addr'])
            closeConnection(selector, key)
    if mask & selectors.EVENT_WRITE:
        if data['out']:
            sent = sock.send(data['out'])
            data['out'] = data['out'][sent:]

def eventLoop(selector):
    while True:
        events = selector.select(timeout=None)
        for key, mask in events:
            #using a try because one failure shouldnt stop the server
            try:
                if key.data is None:
                        loadNewConnection(selector, key)
                else:
                    processExistingConnection(selector, key, mask)
            except Exception as e:
                print("error while reading from connection", e)
                closeConnection(selector, key)

def closeConnection(selector, key):
    sock = key.fileobj
    selector.unregister(sock)
    sock.close()

if __name__ == '__main__':
    startSyncronousServer()
