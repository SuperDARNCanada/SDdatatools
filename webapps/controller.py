from model import RtiForm, ConvectionForm, FanForm, PlottypeForm
from flask import Flask, render_template, request
from computemaps import compute_maps
import sys, os

app = Flask(__name__)

UPLOAD_DIR = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.secret_key = 'MySecretKey'

if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

RTI_FAN_EXTENSIONS = set(['fitacf', 'lmfit'])
CONVECTION_EXTENSIONS = set(['map'])

def allowed_rti_fan_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[-1] in RTI_FAN_EXTENSIONS

def allowed_convection_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[-1] in CONVECTION_EXTENSIONS

@app.route('/webapps', methods=['GET', 'POST'])
def index():
    plot_form = PlottypeForm() # might not need this form?
    rti_form = RtiForm()
    convection_form = ConvectionForm()
    fan_form = FanForm()

    filename = None

    if request.method == 'POST':
        file = request.files[plot_file = request.files[plot_form.filename.name]

        if rti_form.validate_on_submit() and file and allowed_rti_fan_file(file.filename):
               filename = secure_filename(file.filename)
               file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        if convection_form.validate_on_submit():
           if file and allowed_convection_file(file.filename):
               filename = secure_filename(file.filename)
               file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        if fan_form.validate_on_submit() and file and allowed_rti_fan_file(file.filename):
               filename = secure_filename(file.filename)
               file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))


    return render_template('plotting_tools.html',
                           form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)
