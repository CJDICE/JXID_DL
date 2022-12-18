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
		'User-Agent':'',
		'Cookie':''
		}

	with open('headers.txt', 'r') as f:
		headers['User-Agent'] = f.readline().strip('\n')
		headers['Cookie'] = f.readline().strip('\n')
		f.close()

	return headers



def getHtml(url):
	headers = composeHeaders()
	page1 = urllib.request.Request(url, headers=headers)
	page = urlopen(page1)
	html = str(page.read(), 'utf-8')
	return html



def getLink(pageURL):

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
				print(a.attrs['href'])
				highResolution = a.attrs['href'].replace('/1600/', '/2560/')
				imgList.append(highResolution)
			except Exception as e:
				print('Tag no attrs[href], maybe contain video?')

		print('total:' + str(i))

		#downloadImg(dirName, imgList)

	except HTTPError as e:
		print(e)
	except URLError as e:
		print('The server could not be found!')
	#except Exception as e:
	#	print('Other:',e);
	else:
		print('It Works')



### Main process ###
if 'VIRTUAL_ENV' in os.environ:
    print('Running in virtual environment:', os.environ['VIRTUAL_ENV'])
else:
    print('Not running in a virtual environment')

if len(sys.argv) < 2:
	print('Usage: python3 JXID_DL.py [URL]')
	exit()

strMainPage = sys.argv[1]
getLink(strMainPage)
