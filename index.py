import os

from flask import Flask, render_template, request,send_file, url_for,redirect, session
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename

from image_an import line_intensity

import json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


dropzone = Dropzone(app)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'static/uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
    DROPZONE_REDIRECT_VIEW='completed',  # set redirect view
    DROPZONE_DEFAULT_MESSAGE='Загрузите ваше изображение'
)


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
app.secret_key = b'_5#fdss"F4Q8z\n\xec]/'

image_urls=[]

@app.route('/', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        f = request.files.get('file')
        path=os.path.join(app.config['UPLOADED_PATH'], secure_filename(f.filename))
        f.save(path)
        # if session.get('filename'):
        #     try:
        #         os.remove(session.get('filename'))
        #     except:
        #         pass
        session['filename'] = path

    return render_template('index.html')



@app.route('/completed')
def completed():
    file=session.get('filename')
    if file:
        Y, I_1_0 = line_intensity(file)
        X = list(range(len(Y)))
        
        filename = 'static/uploads/' + file.split('/')[-1] #change
        #os.path.join(app.config['UPLOADED_PATH'], secure_filename(file))
        return render_template('js_output.html', X=X, Y=list(Y), I_1_0=I_1_0, image=filename)
    else:
        return redirect (url_for('upload'))


if __name__ == '__main__':
    app.run(debug=True)