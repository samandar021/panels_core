from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request


class I18nMiddleware(BaseHTTPMiddleware):
    WHITE_LIST = ['en']

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        locale = request.headers.get('locale', None) or \
            request.path_params.get('locale', None) or \
            request.query_params.get('locale', None) or \
            'en'

        if locale not in self.WHITE_LIST:
            locale = 'en'
        request.state.locale = locale

        return await call_next(request)
