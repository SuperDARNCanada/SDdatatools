from flask import Flask, render_template, request
from wtforms import FloatField, Form, validators
import numpy as np

app = Flask(__name__)

class InputForm(Form):
    r = FloatField(validators=[validators.InputRequired()])


@app.route('/home/marina/superDARN/mapping/mapping/webapps/', methods=['GET','POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        r = form.r.data
        s = np.sin(r)
        return render_template("view_output.html", form=form, s=s)
    else:
        return render_template("view_input.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
