import struct
import Client

def genSets(n, c):
    total = 0
    sets = []
    for x in range(n):
      D = { "key" + str(i) : "value" + str(i) for i in range(total, c + total)}
      sets.append(D)
      total+=c
    # tests = [
    #     b'get key2 \r\n',
    #     b'set key1 6 \r\n value3 \r\n',
    # ]
    # print(sets)
    # tests = []
    # for i,s in enumerate(sets):
    #     print('Client', i)
    #     print('tests = [', end='\n')
    #     for t, d in enumerate(s):
    #         print('\tb\'get ' + d + ' \\r\\n', end='\',\n')
    #         print('\tb\'set ' + d + ' ' + str(len(s[d])) + ' \\r\\n ' + s[d] + ' \\r\\n', end='\',\n')
    #     print(']')
    return sets
    # print(tests)
    # return tests
def runClient(tests):
    client = Client.Client()
    client.run(tests=tests)

def runTests(n , c):
    S = genSets(n, c)
    tests = []
    for s in S:
        for d in s:
            msg = 'set ' + d + ' ' + str(len(s[d])) + ' \r\n ' + s[d] + ' \r\n'
            ans = 'STORED\r\n'
            tests.append([msg.encode(), bytearray(ans.encode())])
            msg = 'get ' + d + ' \r\n'
            ans = 'VALUE ' + d + ' ' + str(len(s[d])) + ' \r\n' + s[d] + ' \r\nEND\r\n'
            tests.append([msg.encode(), bytearray(ans.encode())])
        runClient(tests)
        tests = []
    # print(tests)
    

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

runTests(5, 5)
