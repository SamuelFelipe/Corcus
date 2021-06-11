from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/')

from api.views.auth import *
from api.views.employee import *
from api.views.item import *
from api.views.bonus import *
