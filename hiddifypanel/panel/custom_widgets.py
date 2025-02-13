from flask_admin.contrib.sqla import ModelView
from wtforms.widgets import TextArea
from wtforms import TextAreaField
from flask_bootstrap import SwitchField
from wtforms.fields import StringField, IntegerField, SelectField
from hiddifypanel.panel.hiddify import flash
from hiddifypanel.panel import hiddify
from flask_babelex import lazy_gettext as _
from flask_babelex import gettext as __
from flask_admin.contrib import sqla
from hiddifypanel.panel.database import db
import datetime
from hiddifypanel.models import *
from flask import Markup, g
from wtforms.validators import Regexp, ValidationError
import re
import uuid

# from gettext import gettext as _


class DaysLeftField(IntegerField):
    def process_data(self, value):
        if value is not None:
            days_left = (value - datetime.date.today()).days
            self.data = days_left
        else:
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            days_left = valuelist[0]
            new_date_value = datetime.date.today() + datetime.timedelta(days=int(days_left))
            self.data = new_date_value
        else:
            self.data = None


class LastResetField(IntegerField):
    def process_data(self, value):
        if value is not None:
            days_left = (datetime.date.today()-value).days
            self.data = days_left
        else:
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            days_left = valuelist[0]
            new_date_value = datetime.date.today() - datetime.timedelta(days=int(days_left))
            self.data = new_date_value
        else:
            self.data = None


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class MessageAdmin(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'body': CKTextAreaField
    }


class EnumSelectField(SelectField):
    def __init__(self, enum, *args, **kwargs):
        choices = [(str(enum_value.value), _(enum_value.name)) for enum_value in enum]
        super().__init__(*args, choices=choices, **kwargs)
