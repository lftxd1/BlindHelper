# import the necessary packages
import uuid
import os
import socket
import threading

class TempImage:
    def __init__(self, basePath="./tempimage", ext=".jpg"):
        # construct the file path
        self.path = "{base_path}/{rand}{ext}".format(base_path=basePath,
            rand=str(uuid.uuid4()), ext=ext)

    def cleanup(self):
        # remove the file
        os.remove(self.path)


#send image to server via socket

class SendImage:
    def __init__(self, serverAdd="127.0.0.1", serverPort=9000, imageFile=""):
        self.address = (serverAdd,serverPort)
        self.imageFile = imageFile


    def send(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        s.connect(self.address)
        image = os.path.normcase(self.imageFile)

        try:
            f = open(image,  "rb")
            print(f)
            send_file_thread = SendFile(s ,f)
            send_file_thread.start()
        except IOError:
            print(" error!!")


class SendFile(threading.Thread):

    def __init__(self, sock, file):
        threading.Thread.__init__(self)
        self.sock = sock
        self.file = file

    def run(self):
        print("file name is =="+self.file.name)
        BUFFERSIZE = 1024
        count = 0
        #name = self.file.name+'\r'

        # send file name first
        #self.sock.send(name.encode())


        #new method
        #with open(self.file,'rb')  as f:
            #while True:
                #data = f.read(BUFFERSIZE)
                #while (data):
                    #self.sock.send(data)
                    #data = f.read(BUFFERSIZE)
                #if not data:
                    #f.close()
                    #self.sock.close()
                    #break

        while True:
            file_data = self.file.read(BUFFERSIZE)
            if not file_data:
                print("no data find")
                break
            self.sock.send(file_data)

        print("sent file ok")
        self.file.close()
        self.sock.close()