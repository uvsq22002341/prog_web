DROP TABLE IF EXISTS avancements;
DROP TABLE IF EXISTS assignations;
DROP TABLE IF EXISTS taches;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
email VARCHAR(128) NOT NULL,
password_hash VARCHAR(128) NOT NULL,
totp CHAR(32),
unique (email)
);

CREATE TABLE taches (
id INT PRIMARY KEY AUTO_INCREMENT,
nom_tache VARCHAR(255) NOT NULL,
date_creation DATE NOT NULL,
createur_id INT,
FOREIGN KEY (createur_id) REFERENCES users(id)
);

CREATE TABLE assignations (
id INT PRIMARY KEY AUTO_INCREMENT,
tache_id INT,
assigneur_id INT,
assigne_id INT,
FOREIGN KEY (tache_id) REFERENCES taches(id),
FOREIGN KEY (assigneur_id) REFERENCES users(id),
FOREIGN KEY (assigne_id) REFERENCES users(id)
);

CREATE TABLE avancements (
id INT PRIMARY KEY AUTO_INCREMENT,
tache_id INT,
assigne_id INT,
pourcentage_avancement INT,
FOREIGN KEY (tache_id) REFERENCES taches(id),
FOREIGN KEY (assigne_id) REFERENCES users(id)
);