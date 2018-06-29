from model import InputForm
from flask import Flask, render_template, request
from computemaps import compute_maps
import sys

app = Flask(__name__)

@app.route('/webapps', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = compute_maps(form.date.data,
                              form.integration_time.data,
                              form.start_time.data)
    else:
        result = None
    print form, dir(form)
    #print form.keys()
    for f in form:
        print f.id
        print f.name
        print f.label

    return render_template('view.html',
                           form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)
