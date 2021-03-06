from flask import *
import sqlite3
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
cat = ["Funny", "NSFW", "Animals", "Auto", "Games", "Cinema", "Conspiracy", "Fashion", "Food", "Politics", "Technology", "Sports", "Music"]
DATABASE = 'app.db'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = './uploads'
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
    try:
        db = get_db()
        pictures = db.execute("SELECT DISTINCT path FROM posts ORDER BY id DESC")
        return render_template('index.html', all_pictures=pictures, title="HOT")
    except TypeError:
        abort(404)


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

@app.route("/<path>", methods=["GET"])
def show_pic(path):
    try:
        db = get_db()
        if path in cat:
            cat_pictures = db.execute("SELECT DISTINCT path FROM posts WHERE category=?", [path])
            return render_template('index.html', all_pictures=cat_pictures, title=path)
        else:
            if "('" not in path: #trouver un meilleur moyen de g??rer ce cas
                url = path
            else:
                url = path[2:-3]
            comm = db.execute("SELECT content FROM commentaries WHERE path=?", [url]).fetchall()
            foo = []
            for items in comm:
                foo.append(items[0])
            print(foo)
            pictures = db.execute("SELECT DISTINCT path FROM posts WHERE path=?", [url]).fetchall()
            titre = db.execute("SELECT title FROM posts WHERE path=?", [url])
            a = titre.fetchone()
            return render_template('index.html', all_pictures=pictures, title=a[0], commentaires=foo, show_comment=1)
    except TypeError:
        abort(404)

@app.route("/show_comment/<path>", methods=["POST"])
def show_comment(path):
    data = request.form.to_dict(flat=True)
    commentaire = data['comment']
    db = get_db()
    db.execute("INSERT INTO commentaries (path, content) VALUES (?, ?)", [path, commentaire])
    db.commit()
    print("path:",path)
    return redirect("/"+path) #redirection vers l'autre d??corateur




@app.route("/pic_db")
def pic_db():
    db = get_db()
    cur = db.execute("SELECT * FROM posts where path=(?)", ["photo-1506045412240-22980140a405.jpeg"]) #?? remettre comme avant
    posts = []
    for post in cur:
        posts.append({"id": post[0], "path": post[1],
                      "title": post[2], "category": post[3]})
    return jsonify(posts)



@app.route("/comm_db")
def comm_db():
    db = get_db()
    cur = db.execute("SELECT content, path FROM commentaries")
    posts = []
    for post in cur:
        posts.append({"content": post[0], "path": post[1]})
    return jsonify(posts)


if __name__ == '__main__':
    app.run(debug=True)
