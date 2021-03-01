import sqlite3


DATABASE = 'app.db'
db = sqlite3.connect(DATABASE)

cursor = db.cursor()




# Création de la BDD


# Données des uploads
cursor.execute("DROP TABLE IF EXISTS posts")
cursor.execute("""CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   title VARCHAR(500),
                                   description VARCHAR(500),
                                   category VARCHAR(50),
                                   path VARCHAR(500) NOT NULL)""")


cursor.execute("DROP TABLE IF EXISTS commentaries")
cursor.execute("""CREATE TABLE commentaries (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   content VARCHAR(5000) NOT NULL,
                                   username VARCHAR(50) NOT NULL,
                                   post_id INTEGER NOT NULL,
                                   CONSTRAINT fk_posts
                                     FOREIGN KEY (post_id)
                                     REFERENCES posts(post_id))""")



cursor.execute('DROP TABLE IF EXISTS categories')
cursor.execute("""CREATE TABLE categories (id INTEGER PRIMARY KEY \
                AUTOINCREMENT,
                            name VARCHAR(200) NOT NULL)""")

for name in ["Funny", "NSFW", "Anime & Manga", "Cars", "Gaming", "GIF", "Meme"]:
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))

db.commit()


db.close()