-- Création de la table VOOT_user
CREATE TABLE IF NOT EXISTS VOOT_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discord_id VARCHAR(255) NOT NULL,
    pseudo_discord VARCHAR(255),
    mail VARCHAR(255),
    mot_de_passe VARCHAR(255),
    vip BOOLEAN,
    duree INT
);

-- Création de la table VOOT_key
CREATE TABLE IF NOT EXISTS VOOT_key (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES VOOT_user(id),
    cle VARCHAR(255)
);

-- Création de la table VOOT_admin
CREATE TABLE IF NOT EXISTS VOOT_admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discord_id VARCHAR(255),
    perm BOOLEAN,
    FOREIGN KEY (discord_id) REFERENCES VOOT_user(discord_id)
);
