from functools import wraps
import os

from flask import (
    Blueprint, request
)

from flaskr.instance_manager import InstanceManager

blueprint = Blueprint('routes', __name__)


def require_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != os.environ.get('DISCORD_BOT_TOKEN'):
            raise Exception('Invalid token')
        return func(*args, **kwargs)
    return decorated


@blueprint.route('/start')
def start_instance():
    instanceManager = InstanceManager()
    state = instanceManager.get_instance_state()

    if state == 'running' or state == 'pending':
        return 'already running'

    instanceManager.start_instance()
    instanceManager.kill_session()

    return 'started'


@blueprint.route('/stop')
def stop_instance():
    instanceManager = InstanceManager()
    state = instanceManager.get_instance_state()

    if state == 'stopped' or state == 'stopping':
        return 'already stopped'

    instanceManager.stop_instance()
    instanceManager.kill_session()

    return 'stopped'


@blueprint.route('/state')
def server_state():
    instanceManager = InstanceManager()
    state = instanceManager.get_instance_state()
    instanceManager.kill_session()
    return state


@blueprint.route('/ip')
def server_ip():
    instanceManager = InstanceManager()
    ip = instanceManager.get_instance_ip()
    instanceManager.kill_session()
    return ip
