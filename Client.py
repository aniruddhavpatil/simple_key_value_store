import socket
import struct

class Client(object):
  def __init__(self, address='127.0.0.1', port=12345):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.address = address
    self.port = port
  
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

  def run(self):
    self.socket.connect((self.address, self.port))
    self.send_msg(self.socket, b'message')
    response = self.socket.recv(1024)
    print(response)
    self.socket.close()

  
  def greet(self):
    print('Client')

if __name__ == '__main__':
  client = Client()
  client.run()
