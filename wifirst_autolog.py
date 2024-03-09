import requests
import time
import argparse

parser = argparse.ArgumentParser(description='Login to WiFirst network.')
parser.add_argument('-m', '--mail', required=True, help='Email address')
parser.add_argument('-p', '--password', required=True, help='Password')
args = parser.parse_args()

mail = args.mail
password = args.password

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'


def check_internet(url='https://google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except:
        pass
    return False


def connect():
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': useragent,
    }

    response = requests.get('https://wireless.wifirst.net/index.txt', headers=headers, timeout=5)
    indexinfo = response.text

    #print("Step 🚹 1️⃣ ⬆️")


    headers = {
        'User-Agent': useragent,
    }

    response = requests.get('https://portal-front.wifirst.net/connect', headers=headers, timeout=5)
    cookie = response.cookies


    params = {
        'force_production': 'false',
    }

    response = requests.get('https://portal-front.wifirst.net/api/settings', params=params, headers=headers, cookies=cookie, timeout=5)
    if response.cookies:
        cookie = response.cookies
    rjson = response.json()

    #print("Step 🛄 2️⃣ ⬆️")

    print(f"🔆✨ {rjson.get("organism_name","WiFirst")} ✨🔆")
    print(f"💘 {rjson.get("hotspot_name","WiFirst - Unknow")} 💘")

    fragments = rjson["fragments"]
    frid = None
    if len(fragments) > 1:
        for frag in fragments:
            if "email" in str(frag):
                frid = frag["id"]
                
    else:
        frid = fragments[0]
        
    if not frid:
        raise SystemExit("🆘 Could not get Fragment ID 😿")


    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'User-Agent': useragent,
    }

    json_data = {
        'fragment_id': frid,
        'box_token': indexinfo,
        'guest_user': {
            'email': mail,
            'password': password,
            'cgu': True,
        },
    }

    response = requests.post('https://portal-front.wifirst.net/api/guest_users', headers=headers, json=json_data, cookies=cookie, timeout=5)
    if response.cookies:
        cookie = response.cookies
    loginfo = response.json()
    #print("Step 🛂 3️⃣ ⬆️")

    if loginfo.get("properties"):
        print(f"➡️ Nom : 👋 {loginfo["properties"].get("lastname","NoName👻")}💅")
        print(f"➡️ Prenom : 👋 {loginfo["properties"].get("firstname","NoName👻")}🙏")

    if not loginfo.get("radius",""):
        raise SystemExit("🆘 No radius info ‼️⁉")

    wifirstlogin = loginfo["radius"].get("login")
    wifirstpass = loginfo["radius"].get("password")


    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://portal-front.wifirst.net',
        'Referer': 'https://portal-front.wifirst.net/',
        'User-Agent': useragent,
    }

    data = {
        'username': wifirstlogin,
        'password': wifirstpass,
        'success_url': 'https://portal-selfcare.wifirst.net',
        'error_url': 'https://portal-front.wifirst.net/connect-error',
        'update_session': '0',
        'qos_class' : 26
    }

    response = requests.post('https://wireless.wifirst.net/goform/HtmlLoginRequest', headers=headers, data=data, cookies=cookie, timeout=5) # enfin
    if response.status_code < 400:
        print(response.status_code)
        print("🌈😇 Logged in ✈")
    else:
        print("🛑🥲 Error ‼️💥🙇")
        print(f"🚨 Http error code : {response.status_code}")
        print(response.reason)


if __name__ == "__main__":
    print("Starting 🚬🗿 ...")
    
    if check_internet():
        print("🤗 We already have internet, ensuring this stays true 👍")
    
    while True:
        if not check_internet():
            print("🚀 Connecting... 🛜")
            try:
                connect()
            except Exception as e:
                print(e)
                
        time.sleep(10)



print("\n😽 Bye bye 👋")