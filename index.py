import os

from flask import Flask, render_template, request,send_file, url_for,redirect, session
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename

from apps.image_an import line_intensity

from apps.forms import UploadForm



app = Flask(__name__, static_folder="static")


dropzone = Dropzone(app)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOAD_FOLDER=os.path.join(PROJECT_ROOT, 'uploads'),
    UPLOAD_EXTENSIONS = ['.jpg', 'jpeg', '.png', '.gif'],
    STATIC_FOLDER = 'static/',
    STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static")),
    # # Flask-Dropzone config:
    # DROPZONE_ALLOWED_FILE_TYPE='image',
    # DROPZONE_MAX_FILE_SIZE=3,
    # DROPZONE_MAX_FILES=1,
    # DROPZONE_REDIRECT_VIEW='completed',  # set redirect view
    # DROPZONE_DEFAULT_MESSAGE='Загрузите ваше изображение'
)

# UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# #app.config['UPLOAD_EXTENSIONS'] = ['.jpg', 'jpeg', '.png', '.gif']
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['STATIC_FOLDER'] = 'static/'
#
# app.config['STATICFILES_DIRS'] = (os.path.join(PROJECT_ROOT, "static"))


app.secret_key = b'_5#fwwdss"F4Q8z\n\xec]/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        f = request.files.get('file')
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(path)
        # if session.get('filename'):
        #     try:
        #         os.remove(session.get('filename'))
        #     except:
        #         pass
        session['filename'] = path

    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index_forms():
    forms = [UploadForm(prefix="form%s" %(i)) for i in range(5)]

    if forms[0].validate_on_submit():
        session['datas'] =[]
        for form in forms:
            samplename = form.data['samplename']
            f = form.data['filename']
            if not f: continue
            filename = secure_filename(f.filename)

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(path)
            session['datas'].append({'filename':path, 'samplename':samplename})
        return redirect(url_for('completed'))

    return render_template('index_form.html', forms=forms)



@app.route('/completed')
def completed():
    #file = session.get('filename')
    datas = session.get('datas')
    if datas:
        intensities = {}
        pixels = {}
        I1_I0 = {}
        for data in datas:
            samplename = data['samplename']
            file = data['filename']
            Y, I1_I0[samplename] = line_intensity(file)
            intensities[samplename] = list(Y)

            #pixels[samplename] \
            X = (list(range(len(Y))))

            #filename = 'static/uploads/' + file.split('/')[-1] #change
            #os.path.join(app.config['UPLOADED_PATH'], secure_filename(file))
        return render_template('output.html', X=X, Y=intensities, I1_I0=I1_I0)
    else:
        return redirect (url_for('index_forms'))


if __name__ == '__main__':
    app.run(debug=True)