from typing import Optional
from django.conf import settings
from django.urls import is_valid_path, get_script_prefix
from django.utils import translation
from django.http import HttpRequest, HttpResponse
from django.middleware.locale import LocaleMiddleware as _LocaleMiddleware
from django.utils.cache import patch_vary_headers


class LocaleMiddleware(_LocaleMiddleware):
    def process_request(self, request: HttpRequest):
        language = translation.get_language()
        request_language = self.language_from_request(request)
        if language != request_language and self.validate(request, request_language):
            translation.activate(request_language)
            return
        super().process_request(request)

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        language = translation.get_language()
        if response.status_code == 404:
            if redirect := self.redirect(request, language):
                return redirect

        language = self.language_from_request(request)
        response.headers.setdefault("Content-Language", language)
        return response

    def language_from_request(self, request: HttpRequest) -> str:
        return translation.get_language_from_request(request, check_path=True)

    def language_from_path(self, path: str) -> Optional[str]:
        return translation.get_language_from_path(path)

    def language_path(self, request: HttpRequest, language: str) -> str:
        return f"/{language}{request.path_info}"

    def validate(self, request: HttpRequest, language: str):
        path = self.language_path(request, language)
        if not is_valid_path(path, getattr(request, "urlconf", settings.ROOT_URLCONF)):
            return False
        return True

    def language_url(self, request: HttpRequest, language: str) -> str:
        if language == settings.LANGUAGE_CODE or self.language_from_path(request.path_info):
            return request.path

        # Maybe the language code is missing in the URL? Try adding the language
        # prefix and redirecting to that URL.
        language_path = self.language_path(request, language)
        path_valid = self.validate(request, language)
        path_needs_slash = not path_valid and (
            settings.APPEND_SLASH
            and not language_path.endswith("/")
            and self.resolve_path(request, f"{language_path}/")
        )

        if path_valid or path_needs_slash:
            script_prefix = get_script_prefix()
            # Insert language after the script prefix and before the rest of the URL
            return request.get_full_path(force_append_slash=path_needs_slash).replace(
                script_prefix, "%s%s/" % (script_prefix, language), 1
            )
        return request.path

    def redirect(self, request: HttpRequest, language: str) -> Optional[HttpResponse]:
        url = self.language_url(request, language)
        if url == request.path:
            return
        redirect = self.response_redirect_class(url)
        patch_vary_headers(redirect, ("Accept-Language", "Cookie"))
        return redirect




