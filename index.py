import os

from flask import Flask, render_template, request,send_file, url_for,redirect
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename

from image_an import line_intensity

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

dropzone = Dropzone(app)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'static/uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
       DROPZONE_REDIRECT_VIEW='completed'  # set redirect view
)


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


image_urls=[]

@app.route('/', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        f = request.files.get('file')
        #path=os.path.join(app.config['UPLOADED_PATH'], f.filename)
        path=os.path.join(app.config['UPLOADED_PATH'], secure_filename(f.filename))
        #path=url_for('static', filename=f.filename)
        #f.save(path)

        filename=secure_filename(f.filename+line_intensity(f,path))
        #filename=line_intensity(path)
        image_urls.append(filename)
        #return send_file(bytes_image,
                     # attachment_filename='plot.png',
        
                     # mimetype='image/png')
        #return render_template('output.html',image=path)
        #return "uploading ..."
    return render_template('index.html')

@app.route('/completed')
def completed():
    try:
        path=url_for('static', filename='uploads/'+image_urls[-1])
        return render_template('output.html', image=path)
    except:
        return redirect (url_for('upload'))



if __name__ == '__main__':
    app.run(debug=True)