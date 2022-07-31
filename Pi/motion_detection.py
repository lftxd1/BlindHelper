# import the necessary packages
from tempimage import TempImage,SendImage
import argparse
import warnings
import datetime
import json
import time
import cv2,os
import requests
import numpy as np

import socket
from threading import Thread

# AF_INET 表示使用IPv4, SOCK_DGRAM 则表明数据将是数据报(datagrams)
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('0.0.0.0', 1777))
liveFlag=False
def UdpReceiver():
    print("Start")
    global liveFlag
    while True:
        rec_msg, addr = udp.recvfrom(1024)
        client_ip, client_port = addr
        order=rec_msg.decode('utf8')
        if order=="open":
            liveFlag=True
        else:
            liveFlag=False
        #print('client_ip:', client_ip, 'client_port:', client_port)
        #print('msg from client:', rec_msg.decode('utf8'))
    #udp.sendto(ack_msg.encode('utf8'), addr)
Thread(target=UdpReceiver).start()

cap = cv2.VideoCapture(0)
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=False,
                help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration 
warnings.filterwarnings("ignore")
conf = json.load(open('conf.json'))
client = None


# 等待摄像头模块启动, 随后初始化平均帧, 
# 时间戳, 以及运动帧计数器
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

def cv2bytes(im):
    return np.array(cv2.imencode('.jpg', im)[1]).tobytes()

def sendImage(frame):
    requests.post("http://192.168.123.110:8080/video",files={"photo":cv2bytes(frame)})

import random
# 从摄像头逐帧捕获数据
while True:
    format="bgr"
    use_video_port=True
    ret, frame = cap.read()
    timestamp = datetime.datetime.now()
    text = "Unoccupied"

    # 调整帧尺寸，转换为灰阶图像并进行模糊
    #frame = imutils.resize(frame, width=500)
    dim = None
    (hh,ww) = frame.shape[:2]
    rr = 500/float(ww)
    dim = (500,int(hh * rr))
    frame = cv2.resize(frame,dim,interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # 如果平均帧是None，初始化它
    if avg is None:
        print("[INFO] starting background model...")
        avg = gray.copy().astype("float")

        continue

#     # accumulate the weighted average between the current frame and
#     # previous frames, then compute the difference between the current
#     # frame and running average
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

#     # threshold the delta image, dilate the thresholded image to fill
#     # in holes, then find contours on thresholded image
    #对变化图像进行阀值化, 膨胀阀值图像来填补孔洞, 在阀值图像上找到轮廓线
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
                           cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)


    if cnts!=None:
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < conf["min_area"]:
                continue
            # 计算轮廓线的外框, 在当前帧上画出外框,并且更新文本
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

    # 在当前帧上标记文本和时间戳
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

    # check to see if the room is occupied
    if text == "Occupied":
        # check to see if enough time has passed between uploads
        #判断上传时间间隔是否已经达到
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
            # increment the motion counter
            #运动检测计数器递增
            motionCounter += 1

            # check to see if the number of frames with consistent motion is high enough
            #判断包含连续运动的帧数是否已经足够多
            if motionCounter >= conf["min_motion_frames"]:
                # check to see if image files sohuld be stored
                if conf["use_imagefile"]:
                    # write the image to temporary file
                    t = TempImage()
                    imagepath = t.path
                    path=str(random.randint(0,10000000))+'.jpg'
                    cv2.imwrite(path, frame)
                    requests.post(url="http://192.168.123.110:8080/intrusion/photo",files={'photo':open(path,"rb")},data={'warehouse':"器材仓库"})
                    os.remove(path)

                    #send file to server via socket
                    # if conf["use_socket"]:
                    #     time.sleep(2)
                    #     sendImage = SendImage(conf["server_address"], conf["server_port"], imagepath)
                    #     sendImage.send()

                    # # upload the image remote server and cleanup the tempory image
                    # print("[UPLOAD] {}".format(ts))

                    #t.cleanup()

                # update the last uploaded timestamp and reset the motion counter
                #更新最近一次上传的时间戳并且重置运动计数器
                lastUploaded = timestamp
                motionCounter = 0

    # otherwise, the room is not occupied
    else:
        motionCounter = 0

    if liveFlag==True:
        Thread(target=sendImage,args=(frame,)).start()
    cv2.imshow("Motion detecting", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

    # clear the stream in preparation for the next frame
