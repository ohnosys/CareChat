from wtforms_tornado import Form
from wtforms_alchemy import ModelForm

from models.user import User


class UserForm(ModelForm, Form):
    class Meta:
        model = User


