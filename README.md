## 📺 Video DownLoad Service
📼 웹에서 보고싶은 영상(영화, 예능, 드라마)을 클릭하면 Transmission 서버를 통해 다운로드를 받고 Plex서버에 영상을 저장하는 서비스

***

## 🚀 개발개요
* 나만의 영상 스트리밍 서버를 만들고자 하는 마음에서 개발을 하게 되었다.
* 기존 토렌트 사이트들은 도박 및 선정적인 광고로 도배 되있어서 사용하기 불편하다.

***

## 🏁 동작흐름
* ### 🚩 Web에서 영화 선택
<img src="https://user-images.githubusercontent.com/50009692/128603497-3009b19b-4a25-4160-bd02-117b13956818.PNG">

* ### 🚩 Transmission server로 파일 piece 다운로드
<img src="https://user-images.githubusercontent.com/50009692/128603625-1f2acece-9531-492a-9439-8fc7475c3d37.PNG">

* ### 🚩 개인 스트리밍 서버(PLEX)에 저장
<img src="https://user-images.githubusercontent.com/50009692/128603646-2cefaeae-da28-47f7-8326-66bc185f48d9.PNG">

***

## ⚒ 기술스택
<img src="https://user-images.githubusercontent.com/50009692/128604988-3dfa36bc-5f59-437e-926c-0e5cad8fe4d4.PNG" height="100">

<img src="https://user-images.githubusercontent.com/50009692/128605016-19ca1e6a-6ff8-4bf9-961d-1be75804ce5d.PNG" height="100">

***

## ⛏ Installation

* ### WEB (Ubuntu 16.04 기준)
```
apt-get update -y
apt-get install python3 -y
apt-get install python3-pip -y
pip3 install beautifulsoup4
pip3 install requests
pip3 install lxml
pip3 install flask
```

* ### Transmission Server
1. Transmission 서버 설치 (<https://transmissionbt.com/download/>)

2. Transmission 서버 환경설정 (transmission_settings.json)
```json
{
    "download-dir": "download될 root 디렉토리 경로",   
    "rpc-authentication-required": true,
    "rpc-bind-address": "0.0.0.0",
    "rpc-enabled": true,
    "rpc-host-whitelist": "",
    "rpc-host-whitelist-enabled": true,
    "rpc-password": "본인 비밀번호",
    "rpc-port": 9091,
    "rpc-url": "/transmission/",
    "rpc-username": "본인 아이디",
    "rpc-whitelist": "127.0.0.1",
    "rpc-whitelist-enabled": false,
    "scrape-paused-torrents-enabled": true,
    "script-torrent-done-enabled": true,
    "script-torrent-done-filename": "/Document/Scripts/transmission-done.sh",
}
```

3. 토렌트 시드 리스트 자동삭제(다운로드 O, 업로드 X) Shell Script

✔transmission_settings.json 설정의 "/Document/Scripts/transmission-done.sh" 작성
```shell
#!/bin/sh
SERVER="9091 -n TID:TPASSWD"
TORRENTLIST=`transmission-remote $SERVER --list | sed -e '1d;$d;s/^ *//' | awk '{print $1}'`
for TORRENTID in $TORRENTLIST
do
    DL_COMPLETED=`transmission-remote $SERVER --torrent $TORRENTID --info | grep "Percent Done: 100%"`
    STATE_STOPPED=`transmission-remote $SERVER --torrent $TORRENTID --info | grep "State: Seeding\|Stopped\|Finished\|Idle"`
    if [ "$DL_COMPLETED" ] && [ "$STATE_STOPPED" ]; then
		echo "Torrent #$TORRENTID is completed."
		echo "Removing torrent from list."
        transmission-remote $SERVER --torrent $TORRENTID --remove
    fi
done
```

* ### Plex

Plex 서버 설치 (https://www.plex.tv/ko/media-server-downloads/)

Plex 서버 URL: https://서버url:32400/web





