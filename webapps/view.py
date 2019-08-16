from model import InputForm
from flask import Flask, render_template, request
from computemaps import compute_maps

app = Flask(__name__)


@app.route('/home/marina/superDARN/mapping/mapping/webapps/', methods=['GET','POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = compute_maps(form.date.data,
                              form.integration_time.data,
                              form.start_time.data)
    else:
        result = None

    return render_template('view.html',form=form,result=result)

if __name__ == '__main__':
    app.run(debug=True)

