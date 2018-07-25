import wtforms as wtf
from wtforms import Form, BooleanField, FileField, StringField, FloatField, validators

class PlottypeForm(Form):
    plot_type = wtf.SelectField(label="Plot type",choices=['RTI','Convection','Fan'])
    filename = FileField(default=None, label='filename', description='filename',validators=[validators.InputRequired()])

class ConvectionForm(Form):
    integration_time = FloatField(label='integration time (s)', default=120, description="seconds",
                                  validators=[validators.InputRequired()])
    date = StringField(label='Date', description="YYYYMMDD",validators=[validators.InputRequired()])
    start_time = StringField(label='Start time', description="HH:MM",validators=[validators.InputRequired()])

class RtiForm(Form):
    duration_time = FloatField(label='duration time (hr)', default=24, description="seconds",
                               validators=[validators.InputRequired()])
    date = DateField(label='Date',format="%Y%m%d" description="YYYYMMDD",validators=[validators.InputRequired()])
    start_time = StringField(label='Start time', description="HH:MM",validators=[validators.InputRequired()])
    ground_scatter = BooleanField(default=True,label="Ground Scatter")
    beam = IntegerField(label='Beam',description="beam #",validators=[validators.InputRequired()])
    Radar = wtf.SelectField(labe='Radar', validators=[validators.InputRequired()], choices=[('Rankin Inlet','rkn'),('Clyde River', 'cly'),('Saskatoon','sas'),('Prince George','pgr'),('Inuvet','inv')])

class FanForm(Form):
    duration_time = FloatField(label='duration time (hr)', default=24, description="seconds",
                               validators=[validators.InputRequired()])
    date = DateField(label='Date',format="%Y%m%d" description="YYYYMMDD",validators=[validators.InputRequired()])
    start_time = StringField(label='Start time', description="HH:MM",validators=[validators.InputRequired()])
    ground_scatter = BooleanField(default=True,label="Ground Scatter")
    Radar = wtf.SelectField(labe='Radar', validators=[validators.InputRequired()], choices=[('Rankin Inlet','rkn'),('Clyde River', 'cly'),('Saskatoon','sas'),('Prince George','pgr'),('Inuvet','inv')])


