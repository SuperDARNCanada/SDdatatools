from model import RtiForm, ConvectionForm, FanForm, PlottypeForm
from flask import Flask, render_template, request
from computemaps import compute_maps
from flask_wtf.csrf import CsrfProtect
import sys, os


app = Flask(__name__)
#csrf = CsrfProtect(app)

UPLOAD_DIR = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


# this may need to be read in by file to ensure it is not publicly known form github?
app.config.update(dict(
        SECRET_KEY="W3bApp!1cat1on",
#        WTF_CSRF_SECRET_KEY="s2perD@RN"
))

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
    plot_form = PlottypeForm(request.form) # might not need this form?
    rti_form = RtiForm(request.form)
    convection_form = ConvectionForm(request.form)
    fan_form = FanForm(request.form)

    if request.method == 'POST' and rti_form.validate():
        print("compute rti")
    elif request.method == 'POST' and convection_form.validate():
        print("compute convection")
    elif request.method == 'POST' and fan_form.validate():
        print ("compute fan")


    return render_template("plotting_tools.html",
                           plot_form=plot_form,
                           rti_form=rti_form,
                           convection_form=convection_form,
                           fan_form=fan_form)





if __name__ == '__main__':
    app.run(debug=True)
