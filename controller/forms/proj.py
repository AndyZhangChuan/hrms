from controller.forms.base_form import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional


class ProjUpdateForm(BaseForm):
    id = IntegerField('id', validators=[Optional()], default=0)
    company_id = IntegerField('company_id', validators=[DataRequired()])
    proj_name = StringField('proj_name', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    wage_range = StringField('wage_range', validators=[DataRequired()])
    crew_num = StringField('crew_num', validators=[DataRequired()])
    category = IntegerField('category', validators=[DataRequired()])
    tags = StringField('tags', validators=[Optional()])


class ProjStatusChangeForm(BaseForm):
    proj_id = IntegerField('proj_id', validators=[DataRequired()])
    proj_status = IntegerField('proj_status', validators=[DataRequired()])