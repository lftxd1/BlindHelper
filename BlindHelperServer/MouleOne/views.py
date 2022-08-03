from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
import glob
import random
import json
import requests, base64
from MouleOne.models import *
from django.forms.models import model_to_dict
from MouleOne import MobileClound


def GetSpecifiedClassNews(request):
    # 主要的时间是卡在需要加载所有的类别新闻，所以只需要不加载全部，先随机选再判断选的合不合适即可。
    ClassesName = request.GET.get('ClassesName')
    num = request.GET.get("num")
    if num == None:
        num = 10
    else:
        num = int(num)
    res = []
    while True:
        id = random.randint(1, 836074)
        article = Article.objects.get(id=id)
        article = model_to_dict(article)
        article['content'] = ''
        if article['classes'] == ClassesName or ClassesName=="推荐":
            res.append(article)
        if len(res) == num:
            break
    return HttpResponse(json.dumps(res, ensure_ascii=False))
def Index(request):
    return render(request,"index.html")

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
    num = request.GET.get("num")
    if num == None:
        num = 10
    else:
        num = int(num)
    res = []
    for i in range(num):
        id = random.randint(1, 836074)
        article = Article.objects.get(id=id)
        article = model_to_dict(article)
        article['content'] = ''
        res.append(article)

    return HttpResponse(json.dumps(res, ensure_ascii=False))


def IdentifyText(request):
    myFile = request.FILES.get('img')
    path = "static/" + myFile.name
    destination = open(path, 'wb')
    for chunk in myFile.chunks():
        destination.write(chunk)
    destination.close()
    res = MobileClound.mobileCloudText(path)
    return HttpResponse(res)


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
