import socket

class Server(object):
  def __init__(self, port=12345):
    self.socket = socket.socket()
    self.socket.bind(('', port))

  def run(self):
    self.socket.listen(5)
    print("socket is listening")
    while True:
      c, addr = self.socket.accept()      
      print('Got connection from', addr)
      c.send(b'Thank you for connecting')
      break
  
  def greet(self):
    print('Server')


if __name__ == '__main__':
  server = Server()
  server.run()
