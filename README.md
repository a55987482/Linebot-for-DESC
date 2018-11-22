# Linebot- for-DESC
### Step 1. Clone 專案
##### # Clone 專案到桌面，並確認電腦內的 Python 版本是否為 Python3 。
##### # 安裝 Linebot 所需的套件。
```
 * 安裝 linebot-sdk 模組
> pip install line-bot-sdk
```
```
 * 安裝 Python 3 的 requests 模組
> pip3 install requests
```
```
 * 安裝 Flask 模組
> pip3 install flask
```
```
 * 安裝 Json 模組
> pip3 install simplejson
```
### Step 2. 安裝 Ngrok 並啟動Ngrok

##### # Windows 載點：https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip 。

##### # 下載完後解壓縮到桌面，進入資料夾內直接啟動 ngrok.exe ，並打上 ngrok http 5000 。

### Step 3. 啟動 Linebot 專案

##### # 打開 Linebot 專案資料夾內的 config.py ，修改 url 成樹莓派上的 ngrok url。

##### # 在 Terminal 內 cd 進 Linebot 專案資料夾內，執行
```
> python app.py
```

