from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
import glob
import random
import json
from . import MobileClound
import requests, base64
import wave
import difflib
from pydub import AudioSegment
from MouleOne.models import *
from django.forms.models import model_to_dict


def read_wav_bytes(filename: str) -> tuple:
    '''
    读取一个wav文件，返回声音信号的时域谱矩阵和播放时间
    '''
    wav = wave.open(filename, "rb")  # 打开一个wav格式的声音文件流
    num_frame = wav.getnframes()  # 获取帧数
    num_channel = wav.getnchannels()  # 获取声道数
    framerate = wav.getframerate()  # 获取帧速率
    num_sample_width = wav.getsampwidth()  # 获取实例的比特宽度，即每一帧的字节数
    str_data = wav.readframes(num_frame)  # 读取全部的帧
    wav.close()  # 关闭流
    return str_data, framerate, num_channel, num_sample_width


def GetSpecifiedClassNews(request):
    ClassesName = request.GET.get('ClassesName')
    articles = list(Article.objects.filter(classes=ClassesName))
    res = []
    for i in range(10):
        index = random.randint(1, len(articles) - 10)
        t = model_to_dict(articles[index])
        t["content"] = ""
        res.append(t)
    return HttpResponse(json.dumps(res, ensure_ascii=False))


from MouleOne.chatService import push


def GetSpecifiedNews(request):
    ID = request.GET.get('ID')
    id = int(ID)
    article = Article.objects.get(id=id)
    article = model_to_dict(article)
    return HttpResponse(json.dumps(article, ensure_ascii=False))


def GetNewsById(request):
    id = int(request.GET.get('id'))
    article = Article.objects.get(id=id)
    article = model_to_dict(article)
    return HttpResponse(json.dumps(article, ensure_ascii=False))


def GetIndexNews(request):
    num=request.GET.get("num")
    if num==None:
        num=10
    else:
        num=int(num)
    res = []
    for i in range(num):
        id = random.randint(1, 836074)
        article = Article.objects.get(id=id)
        article = model_to_dict(article)
        article['content'] = ''
        res.append(article)
    article = model_to_dict(Article.objects.get(id=2))
    res[0]=article
    return HttpResponse(json.dumps(res, ensure_ascii=False))


def TxtToMp3(request):
    text = request.GET.get("text")
    mp3 = MobileClound.TxtToMp3(text)
    return HttpResponse(mp3)


def GetTiku(request):
    with open("毛泽东思想和中国特色社会主义理论体系概论题库.json", 'r', encoding='utf-8') as f:
        tiku = json.loads(f.read())
        return HttpResponse(json.dumps(tiku))


def IdentifyText(request):
    myFile = request.FILES.get('img')
    path = "static/" + myFile.name
    destination = open(path, 'wb')
    for chunk in myFile.chunks():
        destination.write(chunk)
    destination.close()
    res = MobileClound.mobileCloudText(path)
    return HttpResponse(res)


import pydub
import io


def mp3_to_wav(mp3_path, wav_path):
    with open(mp3_path, 'rb') as fh:
        data = fh.read()

    aud = io.BytesIO(data)
    sound = pydub.AudioSegment.from_file(aud, format='mp3')
    raw_data = sound._data

    size = len(raw_data)
    f = wave.open(wav_path, 'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(16000)
    f.setnframes(size)
    f.writeframes(raw_data)
    f.close()
    return wav_path


def IdentifyAudio(request):
    myFile = request.FILES.get('audio')
    path = "static/" + myFile.name
    destination = open(path, 'wb')
    for chunk in myFile.chunks():
        destination.write(chunk)
    destination.close()
    os.system(f"ffmpeg -y -i  {path} -f wav output.wav")
    os.system(f"ffmpeg -y -i output.wav -f s16le -ac 2 -ar 16000 -acodec pcm_s16le 12.ok.pcm")
    os.system(f"ffmpeg -y -f s16le -ac 2 -ar 16000 -acodec pcm_s16le -i 12.ok.pcm test.wav")
    URL = 'http://127.0.0.1:20001/all'
    wav_bytes, sample_rate, channels, sample_width = read_wav_bytes("test.wav")
    print(sample_rate, channels, sample_width)
    datas = {
        'channels': channels,
        'sample_rate': sample_rate,
        'byte_width': sample_width,
        'samples': str(base64.urlsafe_b64encode(wav_bytes), encoding='utf-8')
    }
    headers = {'Content-Type': 'application/json'}
    r = requests.post(URL, headers=headers, data=json.dumps(datas))
    r.encoding = 'utf-8'
    result = json.loads(r.text)
    print(result)
    return HttpResponse(result["result"])


def AddNews():
    FilePath = r"D:\数据集\THUCNews\data\THUCNews"
    classes = os.listdir(FilePath)
    ans = 0
    for i in classes:
        name = os.path.join(FilePath, i)
        files = os.listdir(name)
        for j in files:
            filepath = os.path.join(name, j)
            with open(filepath, 'r', encoding='utf-8') as f:
                TxtContent = f.read()
                Title = TxtContent.split('\n')[0]
                Content = TxtContent.replace(Title, "")
            article = Article(title=Title, content=Content, classes=i, click=0)
            article.save()
            ans += 1
            print(ans)


def Search(request):
    keyword = request.GET.get("keyword")
    articles = Article.objects.filter(title__contains=keyword)
    res = []
    for i in articles:
        t = model_to_dict(i)
        t["content"] = ""
        res.append(t)
    return HttpResponse(json.dumps(res, ensure_ascii=False))
