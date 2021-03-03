from flask import *
import sqlite3
from PIL import Image
import PIL
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)
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
    return render_template('index.html', all_pictures=pictures)

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
    return redirect(url_for('index'))


@app.route("/<category>")
def show_category(category):
    db = get_db()
    pictures = db.execute("SELECT path FROM posts WHERE category=?", [category])
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
