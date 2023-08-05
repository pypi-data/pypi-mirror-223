import os
import base64
from werkzeug.wrappers import Request, Response, request
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.debug import DebuggedApplication
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from ..components.sessions import session_manager
from ..components.blueprint import Blueprint
from werkzeug.urls import url_encode
from itsdangerous import URLSafeTimedSerializer
import json
import mimetypes
from urllib.parse import quote as url_quote, quote_plus as url_quote_plus, urlencode as url_encode
from werkzeug.utils import send_from_directory, safe_join
import importlib

class Zylo:
    def __init__(self, __name__=None):
        self.template_folder = 'views'
        self.url_map = Map()
        self.static_folder = "static"
        self.error_handlers = {}
        self.middlewares = []
        self.host = 'localhost'
        self.port = 8000
        self.debug = True
        self.secret_key = os.urandom(24)
        self.serializer = URLSafeTimedSerializer(base64.urlsafe_b64encode(self.secret_key))
        self.blueprints = []
        self.__name__ = __name__
        self.config = {}
        self.template_backend = 'zylo.backends.ZyloTemplates'
        self.template_folder = 'views'
        self.load_settings()

    def load_settings(self):
        try:
            settings_module = importlib.import_module('settings')
            templates_setting = getattr(settings_module, 'TEMPLATES', None)
            self.template_backend = templates_setting[0]['BACKEND'] if templates_setting else self.template_backend
            assert self.template_backend == 'zylo.backends.ZyloTemplates', "This backend isn't supported by Zylo."
            self.template_folder = templates_setting[0]['DIRS'][0] if templates_setting and templates_setting[0]['DIRS'] else self.template_folder
            self.host = getattr(settings_module, 'HOST', self.host)
            self.port = getattr(settings_module, 'PORT', self.port)
            self.debug = getattr(settings_module, 'DEBUG', self.debug)
        except ImportError:
            pass  
        except (IndexError, KeyError, AssertionError, ValueError) as e:
            raise ValueError("Invalid TEMPLATES setting in settings.py.") from e
        self.template_env = Environment(loader=FileSystemLoader(self.template_folder))

    def add_url_rule(self, rule, endpoint, handler, methods=['GET']):
        def view_func(request, **values):
            return handler(request, **values)
        self.url_map.add(Rule(rule, endpoint=endpoint, methods=methods))
        setattr(self, endpoint, view_func)

    def route(self, rule, methods=['GET']):
        def decorator(handler):
            self.add_url_rule(rule, handler.__name__, handler, methods)
            return handler
        return decorator

    def errorhandler(self, code):
        def decorator(handler):
            self.error_handlers[code] = handler
            return handler
        return decorator

    def use(self, middleware):
        self.middlewares.append(middleware)

    def config(self):
        return self.config
    
    def url_for_static(self, filename):
        return f'/static/{filename}'

    def serve_static(self, filename):
        static_path = os.path.join(self.static_folder, filename)
        if os.path.isfile(static_path):
            mimetype, _ = mimetypes.guess_type(static_path)
            if mimetype:
                return Response(open(static_path, 'rb').read(), mimetype=mimetype)
        raise NotFound()

    def register_blueprint(self, blueprint):
        self.blueprints.append(blueprint)

    def handle_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(self, endpoint)
            response = handler(request, **values)
        except NotFound as e:
            response = self.handle_error(404, e, request)
        except HTTPException as e:
            response = e
        return response

    def handle_error(self, code, error, request):
        handler = self.error_handlers.get(code)
        if handler:
            return handler(error, request)
        else:
            return error

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        for blueprint in self.blueprints:
            if request.path.startswith(blueprint.url_prefix):
                request.blueprint = blueprint
                response = blueprint.wsgi_app(environ, start_response)
                return response

        session_id = request.cookies.get('session_id')
        session_data = session_manager.load_session(session_id)
        request.session = session_data
        response = self.handle_request(request)
        session_id = session_manager.save_session(request.session)

        if isinstance(response, Response):
            response.set_cookie('session_id', session_id, secure=True, httponly=True)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        app = self.wsgi_app
        for middleware in reversed(self.middlewares):
            app = middleware(app)
        return app(environ, start_response)

    def run(self, host=None, port=None, debug=None, secret_key=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if debug is not None:
            self.debug = debug
        if secret_key is not None:
            self.secret_key = secret_key

        if self.debug:
            app = DebuggedApplication(self, evalex=True)
        else:
            app = self

        from werkzeug.serving import run_simple
        run_simple(self.host, self.port, app, use_reloader=True)
