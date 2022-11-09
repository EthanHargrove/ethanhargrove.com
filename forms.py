from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, DecimalField, BooleanField, SelectField, EmailField, TextAreaField, StringField
from wtforms.validators import NumberRange, InputRequired

class DesktopRandomSystemForm(FlaskForm):
    num_planets = RadioField("Number of Planets:", choices=[(8, "Random"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7")], coerce=int)
    star_mass = DecimalField("Star Mass (M☉︎): ", places=8, validators=[NumberRange(0.08, 2.22)])
    terr_only = BooleanField("Only Terrestrial Planets")
    submit = SubmitField("Generate System")

class MobileRandomSystemForm(FlaskForm):
    num_planets = SelectField("Number of Planets:", choices=[(0, "Random"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7")], coerce=int)
    star_mass = DecimalField("Star Mass (M☉︎): ", places=8, validators=[NumberRange(0.08, 2.22)])
    terr_only = BooleanField("Only Terrestrial Planets")
    submit = SubmitField("Generate System")

class ContactForm(FlaskForm):
    name = StringField("Name:", validators=[InputRequired()])
    email = EmailField("Email:", validators=[InputRequired()])
    subject = StringField("Subject:", validators=[InputRequired()])
    message = TextAreaField("Message:", validators=[InputRequired()])
    submit = SubmitField("Send")