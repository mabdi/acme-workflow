from flask import request, render_template
from flask import Blueprint, redirect, url_for
import core
from core.common import WebSuccess, flat_multi, WebException
from core.annotations import web_wrapper, require_login, require_admin
from modules import order,models

blueprint = Blueprint("orders", __name__, static_folder="/static")
_get_message = lambda exception: exception.args[0]

@blueprint.route('/list')
@web_wrapper(template='list.html',requires_login=True)
def list_hook():
    return {
        "orders": order.list_orders(),
        "states_str": models.states_str
    }

@blueprint.route('/new')
@web_wrapper(template='neworder.html',requires_login=True)
def new_hook():
    return order.list_products()

@blueprint.route('/new',  methods=["POST"])
def new_add_hook():
    params = flat_multi(request.form)
    try:
        order.new(params)
        return redirect(url_for("orders.list_hook"))
    except WebException as error:
        data = order.list_products()
        return render_template('neworder.html', error = _get_message(error), data=data,params = params)
    
    


@blueprint.route('/edit', methods=['GET', 'POST'])
def edit_hook():
    return render_template('login.html')    


@blueprint.route('/view', methods=['GET', 'POST'])
def view_hook():
    sample.method1(flat_multi(request.values))
    return WebSuccess("method1 done.")


@blueprint.route('/confirm_add', methods=['GET', 'POST'])
def ok_sales_hook():
    params = flat_multi(request.values)
    order.change_state(params['order_id'],  models.states["confirm_add"])
    return redirect(url_for("orders.list_hook"))

@blueprint.route('/set_cost', methods=['GET', 'POST'])
def set_cost_hook():
    params = flat_multi(request.values)
    order.set_cost(params['order_id'],params['cost'])
    order.change_state(params['order_id'], models.states["cost_set"])
    return redirect(url_for("orders.list_hook"))

@blueprint.route('/confirm_cost', methods=['GET', 'POST'])
def confirm_sales_hook():
    params = flat_multi(request.values)
    order.change_state(params['order_id'], models.states["confirm_cost"])
    return redirect(url_for("orders.list_hook"))


@blueprint.route('/pay', methods=['GET', 'POST'])
def pay_hook():
    params = flat_multi(request.values)
    order.change_state(params['order_id'], models.states["payed"])
    return redirect(url_for("orders.list_hook"))

@blueprint.route('/confirm_payment', methods=['GET', 'POST'])
def confirm_payment_hook():
    params = flat_multi(request.values)
    order.change_state(params['order_id'], models.states["confirm_pay"])
    return redirect(url_for("orders.list_hook"))

@blueprint.route('/send_to_qc', methods=['GET', 'POST'])
def send_to_qc_hook():
    params = flat_multi(request.values)
    order.change_state(params['order_id'], models.states["production_done"])
    return redirect(url_for("orders.list_hook"))

@blueprint.route('/test_done', methods=['GET', 'POST'])
def test_done_hook():
    params = flat_multi(request.values)
    order.change_state(params['order_id'], models.states["test_done"])
    return redirect(url_for("orders.list_hook"))

@blueprint.route('/production_done', methods=['GET', 'POST'])
def production_done_hook():
    params = flat_multi(request.values)
    order.change_state(params['order_id'], models.states["production_test_done"])
    return redirect(url_for("orders.list_hook"))

@blueprint.route('/set_as_ready', methods=['GET', 'POST'])
def set_as_ready_hook():
    params = flat_multi(request.values)
    order.change_state(params['order_id'], models.states["confirm_ready"])
    return redirect(url_for("orders.list_hook"))

