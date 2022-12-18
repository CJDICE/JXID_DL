from django.shortcuts import render
from django.shortcuts import redirect
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
from urllib.error import URLError
import urllib
from bs4 import BeautifulSoup
import csv
import re
import os
import requests
import sys

fetched_url = ''
fetched_cookie = ''
fetched_agent = ''

# Create your views here.
def show_index(request):
    return render(request, 'hello.html')

def submit(request):
    if request.method == 'POST':
        urlMainPage = request.POST.get('inputField')
        cookie = request.POST.get('cookie')
        agent = request.POST.get('agent')
        print(' ### TEST INPUT' + urlMainPage)

        ### Main process ###
        if 'VIRTUAL_ENV' in os.environ:
            print('Running in virtual environment:', os.environ['VIRTUAL_ENV'])
        else:
            print('Not running in a virtual environment')

        global fetched_url
        fetched_url = urlMainPage

        global fetched_cookie
        fetched_cookie = cookie

        global fetched_agent
        fetched_agent = agent

        return redirect('success')

def success_view(request):

    ModelName, dirName, imgLinks, total = getLinks(fetched_url)

    """
    # Debug output
    for img in imgLinks:
        print(img)
    """

    return render(request, 'hello.html', {'imgLink_list': imgLinks, 'ModelName': ModelName, 'dirName': dirName, 'total': total})

def downloadImg(dirName, imgList):
    downloadDirectory = './' + dirName
    if not os.path.exists(downloadDirectory):
        os.mkdir(downloadDirectory)

    headers = composeHeaders()

    i = 1
    for img in imgList:
        req = urllib.request.Request(img, headers=headers)
        data = urlopen(req).read()
        fileName = '/' + "{0:0>3}".format(i) + '.jpg'
        print('Download:' + img)
        with open(downloadDirectory + fileName, 'wb') as f:
            f.write(data)
            f.close()
            print(downloadDirectory + fileName + ' Done')
        i += 1

def composeHeaders():
    headers = {
        'User-Agent':fetched_agent,
        'Cookie':fetched_cookie
        }

    with open('headers.txt', 'r') as f:
        if headers['User-Agent'] == '':
            headers['User-Agent'] = f.readline().strip('\n')
        if headers['Cookie'] == '':
            headers['Cookie'] = f.readline().strip('\n')
        f.close()

    return headers

def getHtml(url):
    headers = composeHeaders()
    page1 = urllib.request.Request(url, headers=headers)
    page = urlopen(page1)
    html = str(page.read(), 'utf-8')
    return html

def getLinks(pageURL):

    if ('' == pageURL):
        return

    try:
        print('Get URL:', pageURL)
        html = getHtml(pageURL)

        #print(html)

        bs = BeautifulSoup(html, 'html.parser')
        imgTagList = bs.find_all('a', {'rel':'show_group'})

        TagAuthorName = bs.find('a', {'class', 'authorNameImg'})
        AuthorName = TagAuthorName.attrs['href'][1:].strip()
        AuthorName = '[' + AuthorName + ']'

        TagModelName = bs.find('a', {'class', 'modelNameImg'})
        ModelName = TagModelName.attrs['href'][1:].strip()
        print(ModelName)

        TagTitle = bs.find('h3')

        dirName = AuthorName + ' ' + TagTitle.get_text()
        dirName = dirName.replace('/',' ')
        print(dirName)

        i = 0
        imgList = []
        for a in imgTagList:
            i = i+1
            try:
                #print(a.attrs['href'])
                highResolution = a.attrs['href'].replace('/1600/', '/2560/')
                imgList.append(highResolution)
            except Exception as e:
                print('Tag no attrs[href], maybe contain video?')

        print('total:' + str(i))

        #downloadImg(request, imgList)

        return ModelName, dirName, imgList, i

    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')
    #except Exception as e:
        #print('Other:',e)