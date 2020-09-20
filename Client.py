import socket
import struct
import time
import sys

class Client(object):
  def __init__(self, address='127.0.0.1', port=12345, tests=None, debug=False, name="Client"):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.address = address
    self.port = port
    self.tests = tests
    self.debug = debug
    self.name = name
  
  # START REFERENCE: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
  def send_msg(self, sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

  def recv_msg(self, sock):
      # Read message length and unpack it into an integer
      raw_msglen = self.recvall(sock, 4)
      if not raw_msglen:
          return None
      msglen = struct.unpack('>I', raw_msglen)[0]
      # Read the message data
      return self.recvall(sock, msglen)

  def recvall(self, sock, n):
      # Helper function to recv n bytes or return None if EOF is hit
      data = bytearray()
      while len(data) < n:
          packet = sock.recv(n - len(data))
          if not packet:
              return None
          data.extend(packet)
      return data
# END REFERENCE: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

  def run(self):
    self.socket.connect((self.address, self.port))
    clientTests = self.tests
    totalTests = len(clientTests)
    passedTests = 0
    for msg, ans in clientTests:

      self.send_msg(self.socket, msg)
      response = self.recv_msg(self.socket)
      if response == ans:
        passedTests+=1
      if self.debug:
        print(self.name, 'result:', 'SUCCESS' if response == ans else 'FAIL')
    
    print(self.name, 'Tests passed:', passedTests, 'of', totalTests)

    self.socket.close()
    sys.exit()

  
  def greet(self):
    print('Client')

if __name__ == '__main__':
  client = Client()
  client.run()
