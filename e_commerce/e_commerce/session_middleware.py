from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.cache import patch_vary_headers
import logging

# Definindo o logger
logger = logging.getLogger(__name__)

class SeparateAdminSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            logger.debug("Admin session initialized")
            session_key_name = settings.ADMIN_SESSION_COOKIE_NAME
        else:
            logger.debug("Frontend session initialized")
            session_key_name = settings.SESSION_COOKIE_NAME

        session_key = request.COOKIES.get(session_key_name)
        request.session_cookie_name = session_key_name
        request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            return response

        if accessed:
            patch_vary_headers(response, ('Cookie',))

        if modified or settings.SESSION_SAVE_EVERY_REQUEST:
            session_cookie_name = getattr(request, 'session_cookie_name', settings.SESSION_COOKIE_NAME)
            session_key = request.session.session_key

            if session_key:
                response.set_cookie(
                    session_cookie_name,
                    session_key,
                    max_age=request.session.get_expiry_age(),
                    expires=request.session.get_expiry_date(),
                    domain=settings.SESSION_COOKIE_DOMAIN,
                    path=settings.SESSION_COOKIE_PATH,
                    secure=settings.SESSION_COOKIE_SECURE or None,
                    httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )
        return response
