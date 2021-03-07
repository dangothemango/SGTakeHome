import selectors, socket, uuid
from event.seats import *

HOST_PORT = ('127.0.0.1', 8099)
FAILURE = b'FAIL'
SUCCESS = b'OK'
seatReservations = SeatReservations(str(uuid.uuid4()))

verbs = {
    b'QUERY': seatReservations.query,
    b'RESERVE': seatReservations.reserve,
    b'BUY': seatReservations.buy
}

def processCommand(command):
    print(command)
    splitCommand = command.split(b': ')
    verb = splitCommand[0]
    if (len(splitCommand) != 2 or verb not in verbs):
        return FAILURE
    print(splitCommand)
    predicate = splitCommand[1]
    result = verbs[verb](predicate)
    print(result)
    if (isinstance(result, bool)):
        return (SUCCESS if result else FAILURE)
    return bytes(result, 'UTF8')
    
def startSyncronousServer():
    selector = selectors.DefaultSelector()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(HOST_PORT)
    listener.listen()
    listener.setblocking(False)
    selector.register(listener, selectors.EVENT_READ, data=None)

    while True:
        events = selector.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                sock = key.fileobj
                conn, addr = sock.accept()
                conn.setblocking(False)
                data = { 'out':b'', 'in':b'', 'addr':addr }
                events = selectors.EVENT_READ | selectors.EVENT_WRITE
                selector.register(conn, events, data=data)
            else:
                sock = key.fileobj
                data = key.data
                if mask & selectors.EVENT_READ:
                    try:
                        recv_data = sock.recv(1024)
                        print(recv_data)
                        if recv_data:
                            data['in'] += recv_data
                            i=data['in'].find(b'\n')
                            while (i != -1):
                                data['out'] += processCommand(data['in'][:i])
                                data['out'] += b'\n'
                                data['in'] = data['in'][i+1:]
                                i=data['in'].find(b'\n')
                        else:
                            print('closing connection', data['addr'])
                            selector.unregister(sock)
                            sock.close()
                    except ConnectionResetError:
                        selector.unregister(sock)
                        sock.close()
                if mask & selectors.EVENT_WRITE:
                    if data['out']:
                        sent = sock.send(data['out'])
                        data['out'] = data['out'][sent:]

if __name__ == '__main__':
    startSyncronousServer()
