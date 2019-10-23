from config import *


class Post(Form):
    title = StringField(u'Title',validators=[validators.input_required(),
    validators.Length(min=10,max=250)])
    body = TextAreaField(u'Body',validators=[validators.input_required(),
    validators.Length(min=10,max=2500)])

class User(Form):
    username = StringField(u'Username',validators=[validators.input_required(),
    validators.Length(min=3, max=250)])
    email = StringField(u'email',validators=[validators.input_required(),
    validators.Length(min=3,max=50)])
    password = PasswordField('Password',[validators.DataRequired(),
    validators.EqualTo('confirm',message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class Comment(Form):
    body = TextAreaField(u'Body', validators=[validators.input_required(),
    validators.Length(max=2000)])
