from ...forms.base_form import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional


class ProjUpdateForm(BaseForm):
    proj_id = IntegerField('proj_id', validators=[Optional()], default=0)
    company_id = IntegerField('company_id', validators=[DataRequired()])
    proj_name = StringField('proj_name', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    crew_num = IntegerField('crew_num', validators=[DataRequired()])
    category = IntegerField('category', validators=[DataRequired()])
    pic_url_list = StringField('pic_url_list', validators=[Optional()])


class ProjStatusChangeForm(BaseForm):
    proj_id = IntegerField('proj_id', validators=[DataRequired()])
    proj_status = IntegerField('proj_status', validators=[DataRequired()])