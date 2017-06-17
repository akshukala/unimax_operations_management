DB_WRAPPER_ERROR = "DatabaseWrapper objects created in a thread can only be\
used in that same thread. The object with alias '%s' was created in thread id\
%s and this is thread id %s."

def gevent_django_db_hack():
    '''
    Copied from gunicorn's `run_gevent.py` as a black box.
    '''
    try:
        from django.db.backends import BaseDatabaseWrapper, DatabaseError

        if "validate_thread_sharing" in BaseDatabaseWrapper.__dict__:
            import thread
            _get_ident = thread.get_ident

            __old__init__ = BaseDatabaseWrapper.__init__

            def _init(self, *args, **kwargs):
                __old__init__(self, *args, **kwargs)
                self._thread_ident = _get_ident()

            def _validate_thread_sharing(self):
                if (not self.allow_thread_sharing
                    and self._thread_ident != _get_ident()):
                    raise DatabaseError(
                        DB_WRAPPER_ERROR
                        % (self.alias, self._thread_ident, _get_ident())
                    )

            BaseDatabaseWrapper.__init__ = _init
            BaseDatabaseWrapper.validate_thread_sharing \
                = _validate_thread_sharing
    except ImportError:
        pass
