from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.cache import patch_vary_headers

class SeparateAdminSessionMiddleware(SessionMiddleware):
    """
    Middleware para separar as sessões do painel administrativo (admin) e do frontend.
    """
    def process_request(self, request):
        # Define a chave de sessão baseada na URL do admin ou frontend
        if request.path.startswith('/admin/'):
            session_key_name = settings.ADMIN_SESSION_COOKIE_NAME
            session_age = getattr(settings, 'ADMIN_SESSION_COOKIE_AGE', settings.SESSION_COOKIE_AGE)
        else:
            session_key_name = settings.SESSION_COOKIE_NAME
            session_age = settings.SESSION_COOKIE_AGE

        # Configura a chave de sessão correta
        request.session_cookie_name = session_key_name
        session_key = request.COOKIES.get(session_key_name)
        request.session = self.SessionStore(session_key)
        request.session.set_expiry(session_age)

    def process_response(self, request, response):
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            return response

        # Salva a sessão apenas se ela foi acessada e/ou modificada
        if accessed:
            patch_vary_headers(response, ('Cookie',))
        if modified or settings.SESSION_SAVE_EVERY_REQUEST:
            if request.session.get_expire_at_browser_close():
                max_age = None
                expires = None
            else:
                max_age = request.session.get_expiry_age()
                expires_time = request.session.get_expiry_date()
                expires = expires_time.strftime('%a, %d-%b-%Y %H:%M:%S GMT')

            # Define o cookie correto para a sessão
            response.set_cookie(
                request.session_cookie_name,
                request.session.session_key,
                max_age=max_age,
                expires=expires,
                domain=settings.SESSION_COOKIE_DOMAIN,
                path=settings.SESSION_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                samesite=settings.SESSION_COOKIE_SAMESITE,
            )

        return response
