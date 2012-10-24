#! /usr/bin/python2.7
#! -*- coding: utf-8 -*-
import urllib2
import cookielib
import time
from bs4 import BeautifulSoup
from base64 import b64encode
from socket import socket, SOCK_DGRAM, AF_INET

username = '' 
password = ''

HOST = '172.20.1.1'
ROOT_URL = 'http://172.20.1.1/portal/'
INDEX_PAGE = 'index_default.jsp'
LOGIN_PAGE = 'login.jsp'
ONLINE_PAGE = 'online.jsp'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:14.0) Gecko/       20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;  q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Referer': 'http://172.20.1.1/portal/index_default.jsp',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '119',
}

def get_ip():

    s = socket(AF_INET, SOCK_DGRAM)
    s.connect((HOST, 0))
    return s.getsockname()[0]

def get_jsessionid(url):

    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

    response = opener.open(url)

    for item in cookie:
        if item.name == 'JSESSIONID':
            HEADERS['Cookie'] = cookie
            return item.value

def add_cookie_in_headers(username, jsessionid):

    cookie = 'hello1={0};hello2=true;hello3=%CE%CD%CC%CB%CA%C9;hello4=;JSESSIONID={1}' 
    cookie.format(username, jsessionid)


    HEADERS['Cookie'] = cookie


def login(username, password, jsessionid, ip):


    password = b64encode(password)
    
    login_url = ROOT_URL + LOGIN_PAGE
    login_data = 'userName={0}&userPwd={1}&serviceType=&isSavePwd=on&isQuickAuth=false&language=English&browserFinalUrl=&userip={2}'
    login_data = login_data.format(username, password, ip)

    login_request = urllib2.Request(login_url, login_data, HEADERS)
    response = urllib2.urlopen(login_request).read()






    soup = BeautifulSoup(response)
    
    online_info = soup.find_all('input')

    language = online_info[0]['value'].decode()
    heartbeatCyc = online_info[1]['value'].decode()
    heartBeatTimeOutMaxTime = online_info[2]['value'].decode()
    userDevPort = online_info[3]['value'].decode()
    userStatus = online_info[4]['value'].decode()
    userip = ip
    serialNo = online_info[6]['value'].decode()

    online_data = 'language={0}&heartbeatCyc={1}&heartBeatTimeoutMaxTime={2}&userDevPort={3}&userStatus={4}&userip={5}&serialNo={6}'
    online_data = online_data.format(language, heartbeatCyc, heartBeatTimeOutMaxTime, userDevPort, userStatus, userip, serialNo)


    online_url = ROOT_URL + ONLINE_PAGE
    online_request = urllib2.Request(online_url, online_data, HEADERS)
    response = urllib2.urlopen(online_request).read()










    starttime = str(int(time.time() * 1000))
    
    heartBeatSrc ='online_heartBeat.jsp?heartbeatCyc={0}&heartBeatTimeoutMaxTime={1}&language={2}&userDevPort={3}&userStatus={4}&userip={5}&serialNo={6}';
    heartBeatSrc = ROOT_URL + heartBeatSrc.format(heartbeatCyc, heartBeatTimeOutMaxTime, language, userDevPort, userStatus, userip, serialNo)
    response = urllib2.urlopen(heartBeatSrc).read()


    showTimerSrc = 'online_showTimer.jsp?language=English&startTime=' + starttime 
    showTimerSrc = ROOT_URL + showTimerSrc
    response = urllib2.urlopen(showTimerSrc).read()

    funcButtonSrc ='online_funcButton.jsp?language={0}&userip={1}&serialNo={2}'
    funcButtonSrc = ROOT_URL + funcButtonSrc.format(language, userip, serialNo)
    response = urllib2.urlopen(funcButtonSrc).read()

      
    doHeartBeat = 'http://172.20.1.1/portal/doHeartBeat.jsp?heartBeatTimeoutMaxTime={0}&language={1}&userDevPort={2}&userip={3}&serialNo={4}&userStatus={5}'
    doHeartBeat = doHeartBeat.format(heartBeatTimeOutMaxTime, language, userDevPort, userip, serialNo, userStatus)

    while True:
        time.sleep( int(heartbeatCyc) /  1000)
        response = urllib2.urlopen(doHeartBeat).read()
        


if __name__ == '__main__':

    ip = get_ip()

    INDEX_URL = ROOT_URL + INDEX_PAGE
    jsessionid = get_jsessionid(INDEX_URL)

    add_cookie_in_headers(username, jsessionid)

    login(username, password, jsessionid, ip)
