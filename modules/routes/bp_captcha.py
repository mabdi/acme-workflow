from flask import request, make_response,render_template
from flask import Blueprint
import core
from core.common import WebSuccess, flat_multi
from core.annotations import api_wrapper, require_login, require_admin

from modules import captcha

blueprint = Blueprint("captcha", __name__, static_folder="/static")

@blueprint.route('/refresh', methods=['GET'])
def refresh_hook():
    imgIO = captcha.refresh()
    response = make_response(imgIO.read())
    response.content_type = 'image/png'
    return response

