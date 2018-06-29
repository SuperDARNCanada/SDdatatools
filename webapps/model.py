from wtforms import Form, StringField, FloatField, validators

class InputForm(Form):
    integration_time = FloatField(label='Integration time (s)',default=120,
                                  validators=[validators.InputRequired()])
    date = StringField(label='Date YYYYMMDD',
                       validators=[validators.InputRequired()])
    start_time = StringField(label='Start time HH:MM',
                             validators=[validators.InputRequired()])


