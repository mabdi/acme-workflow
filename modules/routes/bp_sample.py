from flask import request, render_template
from flask import Blueprint
import core
from core.common import WebSuccess, flat_multi
from core.annotations import api_wrapper, require_login, require_admin

from modules import sample

blueprint = Blueprint("user_api", __name__, static_folder="/static")

@blueprint.route('/method1', methods=['POST'])
@require_admin
@api_wrapper
def method1_hook():
    sample.method1(flat_multi(request.form))
    return WebSuccess("method1 done.")

@blueprint.route('/', methods=['GET'])
def method2_hook():
    return render_template('login.html')    


@blueprint.route('/<arg1>', methods=['GET'])
@api_wrapper
@require_login
def method3_hook(arg1):
    data = sample.method3(arg1)
    return WebSuccess(message = "last msgs",data = data)