from flask.views import MethodView

from core.factory.di import BaseComponent


class BaseResource(MethodView, BaseComponent):
    pass
