import socket
import time
import sys
import struct
import os
import threading

class Server(object):
  def __init__(self, port=12345):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind(('', port))
    self.store = os.path.join(os.getcwd(), 'store')

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
      # self.send_msg(c, str.encode(toSend))
    else:
      message = 'VALUE ' + key + ' 0\r\n' + '\r\n' + 'END\r\n' 
      self.send_msg(c, str.encode(message))


  def set(self, c, key, value):
    outPath = os.path.join(self.store, key)
    # print(os.listdir(self.store))
    try:
      out = open(outPath, 'w+')
      out.write(value)
      out.close()
      self.send_msg(c, b'STORED\r\n')
    except:
      self.send_msg(c, b'NOT-STORED\r\n')

    # print('key:', key, 'value:', value)

  def parseMessage(self, message):
    # print('message', message)
    parsedMessage = message.decode('ascii')
    parsedMessage = parsedMessage.split(' ')
    # print('parsedMessage', parsedMessage)
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
        print('DEBUG:', rawMessage)
        if rawMessage is None:
          if connection:
            connection.close()
            break 
        parsedMessage = self.parseMessage(rawMessage)
        if self.validateMessage(parsedMessage):
          if parsedMessage[0] == "set":
            # setValue = self.recv_msg(connection).decode('ascii').strip()
            # print(parsedMessage)
            self.set(connection, parsedMessage[1], parsedMessage[4])
          elif parsedMessage[0] == "get":
            self.get(connection, parsedMessage[1])
        # self.send_msg(connection, b'Thank you for connecting')
        # connection.close()
      except KeyboardInterrupt:
        if connection:
          connection.close()
        break
    return

  def run(self):
    self.socket.listen(5)
    print("socket is listening")
    # lock = threading.Lock()
    while True:
      # lock.acquire()
      connection, addr = self.socket.accept()
      print('Got connection from', addr)
      # Start a connection thread here
      t = threading.Thread(target=self.connectionThread, args=(connection,))
      t.start()
      # t.join()
      # lock.release()
    connection.close()
    self.socket.close()
    print('Bye')
  
  def greet(self):
    print('Server')


if __name__ == '__main__':

  server = Server()
  server.run()
