

:: Checks if connected to Wi-Fi network; if not, attempts to reconnect.
@echo off
setlocal

:: Set your Wi-Fi name here
set "WIFI_NAME=_WifirstXXXX"

:start
netsh wlan show interfaces | Findstr /c:"%WIFI_NAME%" && echo Online || netsh wlan connect ssid="%WIFI_NAME%" name="%WIFI_NAME%"
TIMEOUT /T 10
goto start
