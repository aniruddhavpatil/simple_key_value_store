import socket
import time
import sys
import struct

class Server(object):
  def __init__(self, port=12345):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind(('', port))

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

  def get(self, key):
    pass

  def set(self, key, value):
    pass

  def parseMessage(self, message):
    parsedMessage = message.decode('ascii')
    print(parsedMessage)
    return parsedMessage

  def run(self):
    self.socket.listen(5)
    print("socket is listening")
    while True:
      try:
        c, addr = self.socket.accept()      
        print('Got connection from', addr)
        rawMessage = self.recv_msg(c)
        parsedMessage = self.parseMessage(rawMessage)
        c.send(b'Thank you for connecting')
      except KeyboardInterrupt:
        break
        
    self.socket.close()
    print('Bye')
  
  def greet(self):
    print('Server')


if __name__ == '__main__':

  server = Server()
  server.run()
