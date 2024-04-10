from cryptography.fernet import Fernet

# Chemin du fichier où la clé sera enregistrée
KEY_FILE = "encryption_key.key"

# Fonction pour obtenir la clé ou en générer une nouvelle si elle n'existe pas
def get_or_generate_key():
    try:
        # Tenter de charger la clé à partir du fichier
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        # Si le fichier n'existe pas, générer une nouvelle clé et l'enregistrer
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    return key

# Fonction pour chiffrer les lignes de code à partir d'une certaine ligne
def encrypt_lines_from(lines, start_line, cipher_suite):
    encrypted_lines = []
    for i in range(len(lines)):
        if i < start_line - 1:
            encrypted_lines.append(lines[i])  # Laisser les premières lignes en clair
        else:
            encrypted_lines.append(cipher_suite.encrypt(lines[i].encode()).decode())
    return encrypted_lines

# Fonction pour écrire les lignes chiffrées dans un fichier
def write_encrypted_file(encrypted_lines, output_file):
    with open(output_file, 'w') as f:
        for line in encrypted_lines:
            f.write(line + '\n')

# Fonction pour lire les lignes du fichier source
def read_source_file(source_file):
    with open(source_file, 'r') as f:
        return f.readlines()

# Programme principal
def main():
    source_file = "demon.py"  # Remplacez ceci par le nom de votre fichier source
    output_file = "c.py"  # Nom du fichier de sortie chiffré
    key = get_or_generate_key()  # Obtenir ou générer une clé de chiffrement
    cipher_suite = Fernet(key)

    # Lire le contenu du fichier source
    lines = read_source_file(source_file)

    # Chiffrer les lignes de code
    encrypted_lines = encrypt_lines_from(lines, 15, cipher_suite)

    # Écrire les lignes chiffrées dans un fichier de sortie
    write_encrypted_file(encrypted_lines, output_file)

    print(f"Le script a été chiffré avec succès. Clé de chiffrement : {key}")

if __name__ == "__main__":
    main()
