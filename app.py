from flask import *
import sqlite3
from PIL import Image
import PIL
import os
from werkzeug.utils import secure_filename
<<<<<<< HEAD
=======


>>>>>>> e51dd730b9b9fd29ad194881ab7026fe0e6b2f9d


app = Flask(__name__)
DATABASE = 'app.db'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
<<<<<<< HEAD
UPLOAD_FOLDER = '../uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
=======
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




>>>>>>> e51dd730b9b9fd29ad194881ab7026fe0e6b2f9d


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)
<<<<<<< HEAD
=======


>>>>>>> e51dd730b9b9fd29ad194881ab7026fe0e6b2f9d


@app.route('/')
def index():
    db = get_db()
    pictures = db.execute("SELECT path FROM posts")
<<<<<<< HEAD
    return render_template('index.html', all_pictures=pictures, title="HOT")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect('/')
        file = request.files['file']
        data = request.form.to_dict(flat=True)
        category = data['categories']
        title = data['title']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            db = get_db()
            db.execute("INSERT INTO posts (path, category, title)\
                        VALUES (?, ?, ?)", [filename, category, title])
            db.commit()
=======
    return render_template('index.html', all_pictures=pictures)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    file = request.files['file']
    data = request.form.to_dict(flat=True)
    category = data['categories']
    title = data['title']
    if file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        db = get_db()
        db.execute("INSERT INTO posts (path, category, title)\
                    VALUES (?, ?, ?)", [filename, category, title])
        db.commit()
>>>>>>> e51dd730b9b9fd29ad194881ab7026fe0e6b2f9d
    return redirect(url_for('index'))

@app.route("/<path>")
def show_pic(path):
    db = get_db()
    url = path[2:-3]
    print(url)
    pictures = db.execute("SELECT path FROM posts WHERE path=?", [url])
    titre = db.execute("SELECT title FROM posts WHERE path=?", [url])
    a = titre.fetchone()
    return render_template('index.html', all_pictures=pictures, title=a[0])


@app.route("/categories/<category>")
def show_category(category):
    db = get_db()
    pictures = db.execute("SELECT path FROM posts WHERE category=?", [category])
    return render_template('index.html', all_pictures=pictures, title=category)

@app.route("/<path>", methods=['GET', 'POST'])
def add_comment(path):
    if request.method == "POST":
        data = request.form.to_dict(flat=True)
        commentaire = data['comment']
        url = path[2:-3]
        db = get_db()
        pic_id = db.execute("SELECT id FROM posts where path=?", [url])
        db.execute("INSERT INTO commentaries (content) VALUES(?) WHERE post_id=?", [commentaire, pic_id])

@app.route("/pic_db")
def pic_db():
    db = get_db()
    cur = db.execute("SELECT id, path, title, category FROM posts")
    posts = []
    for post in cur:
        posts.append({"id": post[0], "path": post[1],
                      "title": post[2], "category": post[3]})
    return jsonify(posts)


@app.route("/<category>", methods=["POST"])
def show_category(category):
    db = get_db()
    pictures = db.execute("SELECT path FROM posts WHERE category=?", category)
    return render_template('index.html', all_pictures=pictures)



@app.route("/pic_db")
def pic_db():
    db = get_db()
    cur = db.execute("SELECT id, path, title, category FROM posts")
    posts = []
    for post in cur:
        posts.append({"id": post[0], "path": post[1],
                      "title": post[2], "category": post[3]})
    return jsonify(posts)


if __name__ == '__main__':
    app.run(debug=True)
