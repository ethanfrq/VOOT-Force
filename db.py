import sqlite3

# Fonction pour créer la base de données et les tables
def create_database():
    # Connexion à la base de données (si elle n'existe pas, elle sera créée)
    conn = sqlite3.connect('VOO_tracking.db')
    cursor = conn.cursor()

    # Création de la table VOOT_user
    cursor.execute('''CREATE TABLE IF NOT EXISTS VOOT_user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_discord TEXT NOT NULL,
                        pseudo_discord TEXT NOT NULL,
                        mail TEXT NOT NULL,
                        mot_de_passe TEXT NOT NULL,
                        vip BOOLEAN,
                        duree INTEGER
                    )''')

    # Création de la table VOOT_key
    cursor.execute('''CREATE TABLE IF NOT EXISTS VOOT_key (
                        id INTEGER,
                        key TEXT NOT NULL,
                        FOREIGN KEY (id) REFERENCES VOOT_user(id)
                    )''')

    # Création de la table VOOT_admin
    cursor.execute('''CREATE TABLE IF NOT EXISTS VOOT_admin (
                        id_discord TEXT PRIMARY KEY,
                        perm TEXT CHECK (perm IN ('yes', 'no')),
                        FOREIGN KEY (id_discord) REFERENCES VOOT_user(id_discord)
                    )''')

    # Commit des changements et fermeture de la connexion
    conn.commit()
    conn.close()

# Appel de la fonction pour créer la base de données
create_database()
