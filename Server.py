import socket
import time
import sys
import struct
import os
import threading

class Server(object):
  def __init__(self, port=12345, debug=False):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind(('', port))
    self.store = os.path.join(os.getcwd(), 'store')
    self.debug = debug

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
  
  def checkKey(self, key):
    dirList = os.listdir(self.store)
    return key in dirList

  def get(self, c, key):
    if self.checkKey(key):
      retrievedFile = open(os.path.join(self.store, key), 'r')
      toSend = retrievedFile.read()
      message = 'VALUE ' + key + ' ' + str(len(toSend)) + ' \r\n'
      message = message + toSend + ' \r\n' + 'END\r\n'
      self.send_msg(c, str.encode(message))
    else:
      message = 'VALUE ' + key + ' 0\r\n' + '\r\n' + 'END\r\n' 
      self.send_msg(c, str.encode(message))


  def set(self, c, key, value, size):
    if len(value) != int(size):
      self.send_msg(c, b'NOT-STORED\r\n')
      return
    try:
      outPath = os.path.join(self.store, key)
      out = open(outPath, 'w+')
      out.write(value)
      out.close()
      self.send_msg(c, b'STORED\r\n')
    except:
      self.send_msg(c, b'NOT-STORED\r\n')


  def parseMessage(self, message):
    parsedMessage = message.decode('ascii')
    parsedMessage = parsedMessage.split(' ')
    return parsedMessage
  
  def validateMessage(self, message):
    if len(message) <= 0:
      return False
    if message[0] == "get":
      if len(message) != 3:
        return False
    if message[0] == "set":
      if len(message) != 6:
        return False
    return True

  def connectionThread(self, connection):
    while True:
      try:
        rawMessage = self.recv_msg(connection)
        if self.debug:
          print('DEBUG:', rawMessage)
        if rawMessage is None:
          if connection:
            connection.close()
            break 
        parsedMessage = self.parseMessage(rawMessage)
        if self.validateMessage(parsedMessage):
          if parsedMessage[0] == "set":
            self.set(connection, parsedMessage[1], parsedMessage[4], parsedMessage[2])
          elif parsedMessage[0] == "get":
            self.get(connection, parsedMessage[1])
      except KeyboardInterrupt:
        if connection:
          connection.close()
        break
    return

  def run(self):
    self.socket.listen(5)
    print("socket is listening")
    while True:
      connection, addr = self.socket.accept()
      print('Got connection from', addr)
      # Start a connection thread here
      t = threading.Thread(target=self.connectionThread, args=(connection,))
      t.start()
    connection.close()
    self.socket.close()
    print('Bye')
  
  def greet(self):
    print('Server')


if __name__ == '__main__':

  server = Server(debug=True)
  server.run()
