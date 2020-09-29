from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template_string
from flask import render_template
from flask import request
import re

app = Flask(__name__, static_url_path='/static')

def search_magnet(keyword):
    if keyword is None:
        return []
    header = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }

    url = "https://1337x.to/search/{}+720p/1/".format(keyword)
    r = requests.get(url, headers=header)
    bs = BeautifulSoup(r.content,"lxml")

    trs = bs.select("tbody > tr")
    magnets=[]

    for tr in trs:
         alink = tr.select("td.coll-1 > a")[1]
         title = alink.text
         seeders = tr.select("td.coll-2")[0].text
         leechers = tr.select("td.coll-3")[0].text
         href = alink.get("href")
         href_mod = "https://1337x.to" + href

         r = requests.get(href_mod)
         bs = BeautifulSoup(r.content,"lxml")
         all_links = bs.select("a")
         for a in all_links:
            m_link = a.get("href")
            if m_link is None:
                continue
            if m_link.find("magnet:?") >= 0:
                magnet_url_mod = m_link[0:60]
    
         magnets.append({
            "title":title,
            "magnet":magnet_url_mod,
            "seeders":seeders,
            "leechers":leechers,
         })

    return magnets


def search_magnet2(keyword):
    if keyword is None:
        return []
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }

    url = "https://torrentj15.com/bbs/search.php?srows=10&gr_id=orak&sfl=wr_subject||wr_content&stx={}+720p-NEXT".format(keyword)
    r = requests.get(url, headers=header)
    bs = BeautifulSoup(r.content,"lxml")

    divs = bs.select("div.media")
    ent_magnets = []

    for d in divs:
        alink = d.select("div.media-body > div.media-content > a")[0]
        title = alink.select("span.text-muted")[0].text
        href = alink.get("href")
        href_mod = href.replace(".","https://www.torrentj15.com/bbs",1)

        r = requests.get(href_mod)
        bs = BeautifulSoup(r.content,"lxml")
        mlink = bs.select("li.list-group-item > a")[0]
        magnet_url = mlink.get("href")
        ent_magnets.append({
                "title":title,
                "url":href_mod,
                "magnet":magnet_url,
        })

    
    return ent_magnets


def search_magnet3(keyword):
    if keyword is None:
        return []
    header = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/83.0.4103.61 Safari/537.36" }
    
    url = "https://torrentj15.com/bbs/search.php?srows=10&gr_id=&sfl=wr_subject%7C%7Cwr_content&stx={}+720p-NEXT".format(keyword)
    r = requests.get(url, headers=header)
    bs = BeautifulSoup(r.content,"lxml")

    divs = bs.select("div.media")
    soap_magnets = []

    for d in divs:
        alink = d.select("div.media-body > div.media-content > a")[0]
        title = alink.select("span.text-muted")[0].text
        href = alink.get("href")
        href_mod = href.replace(".","https://www.torrentj15.com/bbs",1)

        r = requests.get(href_mod)
        bs = BeautifulSoup(r.content,"lxml")
        mlink = bs.select("li.list-group-item > a")[0]
        magnet_url = mlink.get("href")
        soap_magnets.append({
                "title":title,
                "url":href_mod,
                "magnet":magnet_url,
        })

    return soap_magnets
        


def send_to_transmission():
    f = open("static/magnet_tmp.txt",'r')
    line = f.readline()
    s = requests.get('http://park:1234@192.168.111.100:9091/transmission/rpc')
    payload = {
        'method':'torrent-add',
        'arguments':{
            'paused':'false',
            'download-dir':'/home/torrent/movie',
            'filename':line
         }
    }
    r = requests.post('http://park:1234@192.168.111.100:9091/transmission/rpc',headers=s.headers,json=payload)

    f.close()




@app.route("/", methods=["GET","POST"])
def index():
    return render_template('home.html')


@app.route("/search", methods=["GET", "POST"])    
def search():
    if "keyword" in request.form:
        keyword = request.form["keyword"]
    else:
        keyword = None

    global magnets
    magnets = search_magnet(keyword)[0:5]

    if len(magnets) > 0:
        return render_template('movie_lst.html',**{"magnets":magnets})
    else:
        return render_template('home.html')


        
@app.route("/search2", methods=["GET","POST"])
def search2():
    if "keyword2" in request.form:
        keyword2 = request.form["keyword2"]
    else:
        keyword2 = None

    global ent_magnets
    ent_magnets = search_magnet2(keyword2)[0:5]

    if len(ent_magnets) > 0:
        return render_template('ent_lst.html',**{"ent_magnets":ent_magnets})
    else:
        return render_template('home.html')

@app.route("/search3", methods=["GET","POST"])
def search3():
    if "keyword3" in request.form:
        keyword3 = request.form["keyword3"]
    else:
        keyword3 = None

    global soap_magnets
    soap_magnets = search_magnet3(keyword3)[0:5]

    if len(soap_magnets) > 0:
        return render_template('soap_lst.html',**{"soap_magnets":soap_magnets})
    else:
        return render_template('home.html')

@app.route('/button/<magnet>',methods=['POST','GET'])
def button(magnet):
    f = open("static/magnet_tmp.txt",'w')
    data = magnet
    f.write(magnet)
    f.close()
    send_to_transmission()
    return "downloading.......... you just enter http://192.168.111.100:32400"
    
    
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5678,debug=True)
