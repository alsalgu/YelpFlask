from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms import SubmitField, ValidationError
from wtforms.validators import InputRequired, NumberRange


class searchYelpForm(FlaskForm):
    longitude = FloatField('Longitude', validators=[InputRequired()])
    latitude = FloatField('Latitude', validators=[InputRequired()])
    radius = IntegerField('Radius in Meters', default=1609,
                          validators=[InputRequired(),
                                      NumberRange(min=0, max=1609,
                                      message="Must be within 1609m(1 Mile)")])
    categories = StringField('Categories')
    search = SubmitField('Search')


class businessIDForm(FlaskForm):
    business_id = StringField('Yelp ID', validators=[InputRequired()])
    viewBusiness = SubmitField('View Business')
