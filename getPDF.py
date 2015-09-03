from weasyprint import HTML
import getHTML
import requests
import os
import re


link = "http://habrahabr.ru/post/262053/"

filename = str(link).split("/")[-2]+".pdf"

proxies = {'http':'http://proxy.ksu.ru:8080'}
auth = requests.auth.HTTPProxyAuth("nakberov","hemongoo")
headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'}

get_html =  requests.get(link, proxies=proxies, headers=headers, auth=auth)
get_html =  get_html.text

title = re.search("<title>[\s\S]*</title>",get_html)
title = title.group(0)

content = re.search('<div class="content html_format">[\s\S]*<ul class="tags">',get_html)
content = content.group(0)

images = re.findall('"https://[\S]*',content)
images_list = []

for i in range(len(images)):
    images[i]= images[i].split('"')[1]
    image_name = images[i].split("/")[-1]
    if "." in image_name:
        content = re.sub(images[i],"file://"+os.path.abspath(".")+"/"+image_name,content)
        images_list.append(os.path.abspath(".")+"/"+image_name)
        r = requests.get(images[i].replace("https","http"), proxies=proxies, headers=headers, auth=auth)
        link = re.search('<p>Sorry, [\s\S]*you have authenticated yourself.</p>',r.text)

        r = requests.get(link.group(0).split(" ")[8], proxies=proxies, headers=headers, auth=auth)
        with open(image_name, 'wb') as out_file:
            out_file.write(r.content)
            out_file.close()

text = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">' + title  + "</head><body>" + title.replace("title","h1") + content + "</body></html>"

resultFile = open(filename, "wb")

HTML(string=text).write_pdf(filename)
resultFile.close()

for elem in images_list:
    os.remove(elem)
print ("Well done")