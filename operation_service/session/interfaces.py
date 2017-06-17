try:
    import cPicle as pickle
except ImportError:
    import pickle
from datetime import datetime, timedelta
import uuid

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session as DjangoSession
from django.db import close_old_connections
from flask.sessions import SessionInterface, SecureCookieSession


class DBInterface(SessionInterface):

    pickle_based = True
    session_class = SecureCookieSession

    def open_session(self, app, request):
        key = request.headers.get(app.auth_header_name, None)
        session = None
        try:
            session_obj = DjangoSession.objects.get(
                session_key=key,
                expire_date__gte=datetime.now()
            )
            dump = str(session_obj.session_data)
            session = self.session_class(pickle.loads(dump))
            if session.get('user_id'):
                user = User.objects.get(id=session['user_id'])
                if user.password != session.get('password_hash'):
                    session = None
                    session_obj.delete()
        except DjangoSession.DoesNotExist:
            pass

        if not session:
            session = self.session_class()
            session['key'] = key = str(uuid.uuid4())

        return session

    def save_session(self, app, session, response):
        try:
            domain = self.get_cookie_domain(app)
            path = self.get_cookie_path(app)
            httponly = self.get_cookie_secure(app)
            secure = self.get_cookie_secure(app)
            expires = self.get_expiration_time(app, session)

            response.set_cookie(app.session_cookie_name, session['key'],
                                expires=expires, httponly=httponly,
                                domain=domain, path=path, secure=secure)

            try:
                obj = DjangoSession.objects.get(session_key=session['key'])
            except DjangoSession.DoesNotExist:
                obj = DjangoSession(session_key=session['key'])

            obj.session_data = pickle.dumps(dict(session))
            obj.expire_date = expires or (datetime.now() + timedelta(days=30))
            obj.save()
        finally:
            close_old_connections()
