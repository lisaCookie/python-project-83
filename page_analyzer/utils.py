from urllib.parse import urlparse, urlunparse

import validators


def validate_url(url_input):
    if not url_input:
        return 'Заполните это поле'
    if len(url_input) > 255:
        return 'URL не должен превышать 255 символов'
    if not validators.url(url_input):
        return 'Некорректный URL'
    return None


def normalize_url(url_input):
    parsed = urlparse(url_input)
    return urlunparse((parsed.scheme, parsed.netloc, '', '', '', ''))
