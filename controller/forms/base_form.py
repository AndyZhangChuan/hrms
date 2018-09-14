from flask_wtf import FlaskForm


class BaseForm(FlaskForm):

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(BaseForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)
