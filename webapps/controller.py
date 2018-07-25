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

ALLOWED_EXTENSIONS = set(['fitacf', 'lmfit', 'rawacf', 'gz', 'bz2', 'map'])

def alloed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[-1] in ALLOWED_EXTENSIONS

@app.route('/webapps', methods=['GET', 'POST'])
def index():
    plot_form = PlottypeForm() # might not need this form?
    rti_form = RtiForm()
    convection_form = ConvectionForm()
    fan_form = FanForm()

    filename = None

    if request.method == 'POST':
        file = request.files[plot_file = request.files[form.filename.name]
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                result = compute_maps(form.filename.data,
                              form.date.data,
                              form.integration_time.data,
                              form.start_time.data)
orm.filename.name]
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                result = compute_maps(form.filename.data,
                              form.date.data,
                              form.integration_time.data,
                              form.start_time.data)

        if rti_form.validate_on_submit():

        if convection_form.validate_on_submit():

        if fan_form.validate_on_submit():
            if request._files:
                    else:
        result = None
    print form, dir(form)
    #print form.keys()
    for f in form:
        print f.id
        print f.name
        print f.label

    return render_template('plotting_tools.html',
                           form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)
