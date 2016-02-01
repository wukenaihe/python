#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import urllib2
import urllib
import os,re,sys
import traceback

reload(sys)                         # 2
sys.setdefaultencoding('utf-8')     # 3

os.environ["http_proxy"]="web-proxy.oa.com:8080"
os.environ["https_proxy"]="web-proxy.oa.com:8080"

#proxy_handler = urllib2.ProxyHandler({"http" : 'proxy.tencent.com:8080'})
# proxy_handler = urllib2.ProxyHandler({"http" : 'web-proxyhk.oa.com:8080'})
# opener = urllib2.build_opener(proxy_handler)
# urllib2.install_opener(opener)


_top_url=""



def request_url(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()

    return the_page


def parse_class():
    url="{0}/thread0806.php?fid=16".format(_top_url)
    content=request_url("http://cl.1024s.info/thread0806.php?fid=16")

    daer_pattern=re.compile(r"""<h3><a href="(.*?)" target="_blank" id=""><font color=green>(.*?)</font></a></h3>""")

    result=daer_pattern.findall(content)

    if result:
        for url,name in result:
            print "name:{0}  {1}/{2}".format(name.decode("gbk"),_top_url,url)

    return result

def get_images(url):
    content=request_url(url)
    images=[]

    image_src_pattern=re.compile(r"""<input src='(.*?)' type='image' onclick=(.*?)>""")
    result=image_src_pattern.findall(content)

    if result:
        for url,other in result:
            images.append(url)

    return images

def download_image(_file,url):
    print url
    data = urllib2.urlopen(url).read()
    f = file(_file,"wb")
    f.write(data)
    f.close()

def download_theme(name,theme_url):
    try:
        theme_url="{0}/{1}".format(_top_url,theme_url)
        print "try to download {0},url {1}".format(name.decode("gbk"),theme_url)
        image_urls=get_images(theme_url)
        dir=os.path.join("images",name)
        if os.path.isdir(dir):
            return
        else:
            os.makedirs(dir.decode("gbk"))
        num=0;
        for url in image_urls:
            image_name=os.path.abspath(os.path.join(dir,"{0}.jpg".format(num)))
            download_image(image_name,url)
            num+=1
    except Exception,e:
        traceback.print_exc()


def run():
    theme_urls=parse_class()
    try:
        for theme_url,name in theme_urls:
            download_theme(name,theme_url)
    except Exception,e:
        print e.message

run()