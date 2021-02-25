from flask import *
import sqlite3
from PIL import Image
import PIL
import os



app = Flask(__name__)
DATABASE = 'app.db'
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}






def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/file_upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
