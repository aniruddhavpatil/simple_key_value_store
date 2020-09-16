import socket

class Client(object):
  def __init__(self, address='127.0.0.1', port=12345):
    self.socket = socket.socket()
    self.address = address
    self.port = port

  def run(self):
    self.socket.connect((self.address, self.port))
    print(self.socket.recv(1024))
    self.socket.close()

  
  def greet(self):
    print('Client')

if __name__ == '__main__':
  client = Client()
  client.run()
