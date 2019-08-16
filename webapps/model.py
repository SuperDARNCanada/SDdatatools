import wtforms as wtf

# Please note that the order of the fields are how they will appear on the page.
class PlottypeForm(wtf.Form):
    plot_type = wtf.SelectField(label="Plot type",
                                choices=['RTI','Convection','Fan'])
    filename = wtf.FileField(default=None,
                             label='filename',
                             description='filename',
                             validators=[wtf.validators.InputRequired()])


class ConvectionForm(wtf.Form):
    integration_time = wtf.FloatField(label='integration time (s)',
                                      default=120, description="seconds",
                                      validators=[wtf.validators.InputRequired()])
    date = wtf.StringField(label='Date',
                           description="YYYYMMDD",
                           validators=[wtf.validators.InputRequired()])
    start_time = wtf.StringField(label='Start time',
                                 description="HH:MM",
                                 validators=[wtf.validators.InputRequired()])
    plot = wtf.SubmitField(label='Plot',validators=[wtf.validators.InputRequired()])


class RtiForm(wtf.Form):
    Radar = wtf.SelectField(label='Radar',
                            validators=[wtf.validators.InputRequired()],
                            choices=[('rkn','Rankin Inlet'),
                                     ('cly','Clyde River'),
                                     ('sas','Saskatoon'),
                                     ('pgr','Prince George'),
                                     ('inv','Inuvet')])

    duration_time = wtf.FloatField(label='duration time (hr)',
                                   default=24,
                                   description="seconds",
                                   validators=[wtf.validators.InputRequired()])
    date = wtf.DateField(label='Date',
                         format="%Y%m%d",
                         description="YYYYMMDD",
                         validators=[wtf.validators.InputRequired()])
    start_time = wtf.StringField(label='Start time',
                                 description="HH:MM",
                                 validators=[wtf.validators.InputRequired()])
    beam = wtf.IntegerField(label='Beam',
                            description="beam #",
                            validators=[wtf.validators.InputRequired()])

    ground_scatter = wtf.BooleanField(default=True,
                                      label="Ground Scatter",
                                      validators=[wtf.validators.InputRequired()])
    plot = wtf.SubmitField(label='Plot')


class FanForm(wtf.Form):

    Radar = wtf.SelectField(label='Radar',
                            validators=[wtf.validators.InputRequired()],
                            choices=[('Rankin Inlet','rkn'),
                                     ('Clyde River', 'cly'),
                                     ('Saskatoon','sas'),
                                     ('Prince George','pgr'),
                                     ('Inuvet','inv')])

    duration_time = wtf.FloatField(label='duration time (hr)',
                                   default=24,
                                   description="seconds",
                                   validators=[wtf.validators.InputRequired()])

    date = wtf.DateField(label='Date',
                         format="%Y%m%d",
                         description="YYYYMMDD",
                         validators=[wtf.validators.InputRequired()])

    start_time = wtf.StringField(label='Start time',
                                 description="HH:MM",
                                 validators=[wtf.validators.InputRequired()])

    ground_scatter = wtf.BooleanField(default=True,
                                      label="Ground Scatter")
    plot = wtf.SubmitField(label='Plot',validators=[wtf.validators.InputRequired()])

