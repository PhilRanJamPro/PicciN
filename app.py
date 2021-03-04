from flask import *
import sqlite3
from PIL import Image
import PIL
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
cat = ["Funny", "NSFW", "Animals", "Auto", "Games", "Cinema", "Conspiracy", "Fashion", "Food", "Politics", "Technology", "Sports"]
DATABASE = 'app.db'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


@app.route('/')
def index():
    db = get_db()
    pictures = db.execute("SELECT path FROM posts")
    return render_template('index.html', all_pictures=pictures, title="HOT")


@app.route("/upload_page", methods=['GET', 'POST'])
def upload_page():
    return render_template('upload.html', title="Upload")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect('/')
        file = request.files['file']
        data = request.form.to_dict(flat=True)
        category = data['categories']
        title = data['title']
        description = data['description']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            db = get_db()
            db.execute("INSERT INTO posts (path, description, category, title)\
                        VALUES (?, ?, ?, ?)", [filename, description, category, title])
            db.commit()
    return redirect(url_for('index'))

@app.route("/<path>", methods=["GET", "POST"])
def show_pic(path):
    if request.method == 'GET':
        db = get_db()
        if path in cat:
            cat_pictures = db.execute("SELECT path FROM posts WHERE category=?", [path])
            return render_template('index.html', all_pictures=cat_pictures, title=path)
        else:
            url = path[2:-3]
            pictures = db.execute("SELECT path FROM posts WHERE path=?", [url])
            titre = db.execute("SELECT title FROM posts WHERE path=?", [url])
            a = titre.fetchone()
            return render_template('index.html', all_pictures=pictures, title=a[0], show_comment=1)
    else:
        data = request.form.to_dict(flat=True)
        commentaire = data['comment']
        print(commentaire)
        url = path[2:-3]
        print(url)
        db = get_db()
        pictures = db.execute("SELECT path FROM posts WHERE path=?", [url])
        titre = db.execute("SELECT title FROM posts WHERE path=?", [url])
        a = titre.fetchone()
        db.execute("INSERT INTO commentaries (path, content) VALUES(?, ?)", [url, commentaire])
    return render_template('index.html', all_pictures=pictures, title=a[0], show_comment=1)


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
