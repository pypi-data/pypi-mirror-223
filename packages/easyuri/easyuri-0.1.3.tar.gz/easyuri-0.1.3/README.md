`easyuri` is a dumb URL parser with a smart interface.

    >>> import easyuri
    >>> uri = easyuri.parse("en.wikipedia.org/wiki/Jabberwocky")
    >>> uri.is_secure, uri.in_hsts
    (True, True)
    >>> uri.scheme, uri.host, uri.port
    ('https', 'en.wikipedia.org', 443)
    >>> uri.subdomain, uri.domain, uri.suffix, uri.path
    ('en', 'wikipedia', 'org', 'wiki/Jabberwocky')
    >>> str(uri)
    'https://en.wikipedia.org/wiki/Jabberwocky'

    >>> uri = easyuri.parse("http://evil.com\\@good.com/")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    DifficultURLError
