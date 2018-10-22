from controller.forms.base_form import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional


class RightsResourceAddForm(BaseForm):
    resource_name = StringField('resource_name', validators=[DataRequired()])
    value = StringField('value', validators=[DataRequired()])
    resource_type = IntegerField('resource_type', validators=[DataRequired()])
    parent_id = IntegerField('parent_id', validators=[Optional()], default=0)
    rank = IntegerField('rank', validators=[Optional()], default=0)


class RightsResourceUpdateForm(RightsResourceAddForm):
    id = IntegerField("id", validators=[DataRequired()])


class RightsRoleAddForm(BaseForm):
    role_name = StringField('role_name', validators=[DataRequired()])


class RightsRoleUpdateForm(RightsRoleAddForm):
    id = IntegerField('id', validators=[DataRequired()])


class RightsRoleResourceAllocateForm(BaseForm):
    role_id = IntegerField('role_id', validators=[DataRequired()])
    rights_ids = StringField('rights_ids', validators=[DataRequired()])


class RightsUserAddForm(BaseForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    phone = IntegerField('phone', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])


class RightsUserUpdateForm(RightsUserAddForm):
    id = IntegerField('id', validators=[DataRequired()])
    user_status = IntegerField('user_status', validators=[DataRequired()])


class ManagerAddForm(BaseForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    phone = IntegerField('phone', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])


class ManagerUpdateForm(BaseForm):
    id = IntegerField('id', validators=[DataRequired()])
    user_status = IntegerField('user_status', validators=[DataRequired()])


class ManagerLoginForm(BaseForm):
    email = StringField('phone', validators=[DataRequired()])
    password = StringField('code', validators=[DataRequired()])


class ManagerRoleAllocateForm(BaseForm):
    manager_id = IntegerField('manager_id', validators=[DataRequired()])
    role_ids = StringField('role_ids', validators=[DataRequired()])


class ManagerProjAllocateForm(BaseForm):
    manager_id = IntegerField('manager_id', validators=[DataRequired()])
    proj_map = StringField('proj_map', validators=[DataRequired()])