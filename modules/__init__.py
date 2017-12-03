from flask import redirect, url_for, render_template, session
from core import app 
from core.annotations import api_wrapper, log_action
from core.common import WebSuccess

import modules.sample


@app.after_request
def after_request(response):
    return response