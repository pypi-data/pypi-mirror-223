"""
A dumb URL parser with a smart interface.

"""

from __future__ import annotations

import base64
import codecs
import hashlib
import inspect
import mimetypes
import unicodedata
import urllib.parse
from dataclasses import dataclass

import hstspreload
import pkg_resources

__all__ = ["parse", "supported_schemes"]


class DifficultURLError(Exception):
    """"""


def parse(uri, secure=True) -> URI:
    """
    Return a `URI` object for given `uri`.

    Various web-related protocols supported.

        >>> webpage = parse("https://wikipedia.org")
        >>> stylesheet = parse("data:text/css,body{font:14px/1.5 Helvetica;}")
        >>> script = parse("javascript:alert('hello world')")

    """
    # TODO
    if "evil" in uri:
        raise DifficultURLError("...")
    uri = str(uri)
    if uri.startswith("//"):
        uri = f"https:{uri}"
    scheme, _, identifier = uri.partition(":")
    if not identifier:
        uri = f"https://{scheme}"
        scheme = "https"
    if "/" in scheme:
        uri = f"https://{scheme}:{identifier}"
        scheme = "https"
    try:
        handler = supported_schemes[scheme]
    except KeyError:
        handler = URI
        # XXX raise ValueError(f"scheme `{scheme}` not supported")
    return handler(uri)

    # XXX uri = handler(identifier)
    # XXX # TODO if scheme == "https":  # TODO cleanup
    # XXX if secure:
    # XXX     uri.is_secure = True
    # XXX     uri.scheme = "https"
    # XXX elif isinstance(uri, HTTPSURI):
    # XXX     uri.is_secure = True
    # XXX     uri.scheme = "https"
    # XXX     if uri.suffix == "onion":
    # XXX         uri.is_secure = False
    # XXX         uri.scheme = "http"
    # XXX return uri


def clean(s):
    # XXX s = str(urllib.parse.unquote(s), "utf-8", "replace")
    s = urllib.parse.unquote(s)
    return unicodedata.normalize("NFC", s).encode("utf-8")


class URI:
    """A Uniform Resource Identifier."""

    def __init__(self, uri):
        self.given = uri

    def __eq__(self, other):
        return str(self) == str(parse(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.normalized)

    def __str__(self):
        return self.normalized

    def __bytes__(self):
        return bytes(self.normalized, "utf-8")

    def __add__(self, suffix):
        new = "".join((self.given, str(suffix)))
        return self.__class__(new)

    def __truediv__(self, path):
        new = "/".join((self.given, str(path)))
        return self.__class__(new)

    def __hash__(self):
        try:
            return self.__hash
        except AttributeError:
            pass
        self.__hash = int(hashlib.sha1(bytes(self.normalized, "utf-8")).hexdigest(), 16)
        return self.__hash

    def __repr__(self):
        return self.normalized

    @property
    def normalized(self):
        return self.given

    @property
    def minimized(self):
        return self.given


class HTTPURI(URI):
    """
    Non-secure web address.

        >>> HTTPURI("example.org")
        http://example.org

    """

    is_secure = False

    def __init__(self, identifier):
        super().__init__(identifier)
        self._normalize()

    @property
    def in_hsts(self):
        return hstspreload.in_hsts_preload(self.host)

    @classmethod
    def from_parts(cls, netloc, path="/", query=None, fragment=""):
        """
        instantiate a URI from parts

        # TODO >>> HTTPURI.from_parts("example.org")
        # TODO http://example.org

        """
        if query is None:
            query = {}
        query_string = urllib.parse.urlencode(query, doseq=True)
        return cls(
            urllib.parse.urlunsplit(
                (cls.__name__.lower(), netloc, path, query_string, fragment)
            )
        )

    @property
    def dict_items(self):
        return dict(scheme=self.scheme, host=self.host, path=self.path)

    @property
    def labels(self):
        return (self.subdomain, self.domain, self.suffix)

    @property
    def minimized(self):
        uri = self.normalized
        uri = uri[len(self.scheme) + 3 :]
        # XXX TODO if uri.startswith("www."):
        # XXX TODO     uri = uri[4:]
        # FIXME strip trail slash on path not fragment
        return uri.rstrip("/").partition("#")[0]

    @property
    def normalized(self):
        query = urllib.parse.urlencode(self.query, doseq=True)
        normalized_parts = (
            "https" if self.is_secure else "http",
            self.netloc,
            self.path,
            query,
            self.fragment,
        )
        normalized = urllib.parse.urlunsplit(normalized_parts)
        # XXX if self.is_relative:
        # XXX     normalized = "/" + normalized
        return normalized

    def _normalize(self):
        uri = self.given
        if uri == "":
            raise ValueError("`uri` must not be blank")
        # if isinstance(uri, unicode):
        #     uri = uri.encode("utf-8", "ignore")

        if uri.startswith("//"):
            self.is_absolute = True
            uri = uri[2:]
        if not uri.startswith(("/", "http://", "https://")):
            uri = "http://" + uri

        uri = uri.replace("#!", "?_escaped_fragment_=", 1)

        parts = urllib.parse.urlsplit(uri.strip())
        self.netloc = ""
        if parts.scheme:
            self.scheme = self._normalize_scheme(parts.scheme)
            self.username = self._normalize_username(parts.username)
            self.password = self._normalize_password(parts.password)
            self.host = self._normalize_host(parts.hostname)
            self.port = self._normalize_port(parts.port)
            if self.username:
                auth = self.username
                if self.password:
                    auth += ":" + self.password
                self.netloc = auth + "@"
            # if not self.host:
            #     raise ValueError("no host in an absolute `uri`")
            self.netloc += self.host
            if self.port not in (80, 443):  # TODO make sure no http on 443, ..
                self.netloc += ":" + str(self.port)
            domain_parts = split_suffix(parts.hostname)
            self.subdomain = domain_parts.subdomain
            self.domain = domain_parts.domain
            self.suffix = domain_parts.suffix
            self.origin = f"{self.scheme}://{self.netloc}"
            self.suffixed_domain = f"{self.domain}.{self.suffix}"
        self.path = self._normalize_path(parts.path).lstrip("/")
        self.raw_query = self._normalize_query(parts.query)
        self.query = urllib.parse.parse_qs(self.raw_query)
        self.fragment = self._normalize_fragment(parts.fragment)

    def _normalize_scheme(self, scheme):
        if scheme not in ("http", "https"):
            error_msg = f"`{scheme}` scheme not supported"
            raise ValueError(error_msg)
        scheme = scheme.lower()
        return scheme

    def _normalize_username(self, username):
        if username is None:
            username = ""
        return username

    def _normalize_password(self, password):
        if password is None:
            password = ""
        return password

    def _normalize_host(self, host):
        if host is None:
            raise ValueError(f"absolute uri `{self.given}` requires a host")
        if " " in host:
            raise ValueError("spaces not allowed in host")
        # host = host.lower().strip(".").decode("utf-8").encode("idna")
        host = host.lower().strip(".")  # .encode("idna")
        return host

    def _normalize_port(self, port):
        # TODO limit to range of possibilities (0 < port < 36???)
        if port is None:
            port = 80 if self.scheme == "http" else 443
        return port

    def _normalize_path(self, path):
        if path == "":
            path = "/"
        path = urllib.parse.unquote(path)
        path = urllib.parse.quote(path, "~:/?#[]@!$&'()*+,;=")
        # path = self._clean(path)
        # XXX if self.is_absolute:
        output = []
        part = None
        for part in path.split("/"):
            if part == "":
                if not output:
                    output.append(part)
            elif part == ".":
                pass
            elif part == "..":
                if len(output) > 1:
                    output.pop()
            else:
                output.append(part)
        if part in ["", ".", ".."]:
            output.append("")
        path = "/".join(output)
        return path

    def _normalize_query(self, query):
        # TODO %3a to %3A
        # TODO %7E to ~
        args = [
            "=".join(
                [
                    urllib.parse.quote(clean(t), "~:/?#[]@!$'()*+,;=")
                    for t in q.split("=", 1)
                ]
            )
            for q in query.split("&")
        ]
        return "&".join(args)

    def _normalize_fragment(self, fragment):
        fragment = urllib.parse.unquote(fragment)
        fragment = urllib.parse.quote(fragment, "~")
        return fragment

    def __getitem__(self, key):
        """get a query parameter"""
        try:
            return self.query[key]
        except KeyError:
            self.query[key] = []
            return self.query[key]

    def __setitem__(self, key, value):
        """set a query parameter"""
        if isinstance(value, list):
            self.query[key] = value
        else:
            self.query[key] = [value]

    def update(self, **args):
        self.query.update(**args)


class HTTPSURI(HTTPURI):

    """
    secure web address

        >>> HTTPSURI("//example.org")
        https://example.org

    """

    is_secure = True

    def __init__(self, identifier):
        super().__init__(identifier)


class WSURI(URI):

    """
    WebSocket service endpoint

    # TODO >>> WSURI("//example.org")
    # TODO ws://example.org

    """

    is_secure = False


class WSSURI(WSURI):

    """
    secure WebSocket service endpoint

    # TODO >>> WSSURI("//example.org")
    # TODO wss://example.org

    """

    is_secure = True

    def __init__(self, identifier):
        super().__init__(identifier)


class DataURI(URI):

    """
    data objects

        >>> DataURI("foo bar")
        data:,foo bar
        >>> data = DataURI("iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAH"
        ...                "ElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAA09O9TXL0Y4O"
        ...                "HwAAAABJRU5ErkJggg==",
        ...                encoded=True, mime_type="image/png")
        >>> data  # doctest: +ELLIPSIS
        data:image/png;base64,iVBORw0K...rkJggg==
        >>> data.mime_type
        'image/png'
        >>> data.save("foo.png")  # doctest: +SKIP

    """

    def __init__(self, data, encoded=False, mime_type="text/plain", charset="US-ASCII"):
        self.given = data
        self.data = data
        self.encoded = encoded
        self.mime_type = mime_type
        self.charset = charset

    @classmethod
    def from_identifier(cls, identifier):
        r"""
        return a data URI for given parsed identifier

            >>> DataURI.from_identifier("text/html,<!doctype html>foo bar")
            data:text/html,<!doctype html>foo bar
            >>> DataURI.from_identifier("text/html;charset=utf-8"
            ...                      ",<!doctype html>fnṏrd")
            data:text/html;charset=utf-8,<!doctype html>fnṏrd

        # TODO >>> DataURI.from_identifier("charset=utf-8,\xe2\x81\x82")
        # TODO data:charset=utf-8,â

        """
        metadata, _, data = identifier.partition(",")
        if not data:
            raise ValueError("unable to parse data URI; bad syntax")
        metadata = metadata.lower().split()
        encoded = "base64" in metadata
        charset = "US-ASCII"
        mime_type = "text/plain"
        for meta in metadata:
            if meta.startswith("charset="):
                charset = meta.partition("=")[2]
            elif meta != "base64":
                mime_type = meta
        return cls(data, encoded, mime_type, charset)

    @classmethod
    def from_file(cls, path, mime_type=None):
        """
        return a data URI for contents of file at given path

        MIME type will be inferred from the file extension if possible. You
        may override this by providing your own with `mime_type`.

            >>> Data.from_file("glider.png")  # doctest: +SKIP
            data:image/png;base64,...

        """
        # TODO infer charset
        with open(path, "rb") as f:
            data = f.read()
        mime_type = mimetypes.guess_type(path)[0]
        encoded = False
        if mime_type.startswith(("image", "audio", "video")):
            data = base64.b64encode(data)
            encoded = True
        return cls(data, mime_type, encoded=encoded)

    @property
    def normalized(self):
        metadata = []
        if self.mime_type != "text/plain":
            metadata.append(self.mime_type)
        if self.charset != "US-ASCII":
            metadata.append(f"charset={self.charset}")
        if self.encoded:
            metadata.append("base64")
        return f"data:{';'.join(metadata)},{self.data}"


class JavascriptURI(URI):

    """
    JavaScript code

        javascript:<javascript to execute>

        >>> JavascriptURI("alert('example');")
        javascript:alert('example');

    """

    @classmethod
    def from_identifier(cls, identifier):
        """"""
        print(identifier)
        return cls()

    @property
    def normalized(self):
        return f"javascript:{self.given}"


class MagnetURI(URI):

    """
    address to a specific piece of content

        magnet:<content-parameters>

        >>> MagnetURI("alert('example');")
        magnet:alert('example');

    """

    def __init__(self, identifier):
        super().__init__(identifier)
        self._normalized = urllib.parse.unquote(identifier)

    @property
    def normalized(self):
        return f"magnet:{self._normalized}"


class TelURI(URI):

    """"""

    def __init__(self, identifier):
        super().__init__(identifier)

    @property
    def normalized(self):
        return self.given
        # XXX return f"tel:{self._normalized}"


class FaxURI(URI):

    """"""

    def __init__(self, identifier):
        super().__init__(identifier)

    @property
    def normalized(self):
        return f"fax:{self._normalized}"


class SMSURI(URI):

    """"""

    def __init__(self, identifier):
        super().__init__(identifier)
        self._normalize()

    def _normalize(self):
        uri = self.given
        parts = urllib.parse.urlsplit(uri.strip())
        self.numbers = parts.path.split(",")
        self.body = urllib.parse.parse_qs(parts.query).get("body", [None])[0]
        self._normalized = ",".join(self.numbers)
        if self.body:
            self._normalized += f"?body={parts.query}"

    @property
    def normalized(self):
        return f"sms:{self._normalized}"


class MailtoURI(URI):

    """"""

    def __init__(self, identifier):
        super().__init__(identifier)
        self._normalize()

    def _normalize(self):
        self._normalized = self.given

    @property
    def normalized(self):
        return f"{self._normalized}"


class WEB_ACTIONURI(URI):

    """"""

    def __init__(self, identifier):
        super().__init__(identifier)
        self._normalize()

    def _normalize(self):
        uri = self.given
        parts = urllib.parse.urlsplit(uri.strip())
        self.action = parts.netloc
        self.query = urllib.parse.parse_qs(parts.query)
        self._normalized = f"{parts.netloc}?{parts.query}"

    @property
    def normalized(self):
        return f"web+action://{self._normalized}"

    def __getitem__(self, key):
        """get a query parameter"""
        return self.query[key]


class MOZ_EXTENSIONURI(URI):

    """"""

    def __init__(self, identifier):
        super().__init__(identifier)
        self._normalize()

    def _normalize(self):
        uri = self.given
        parts = urllib.parse.urlsplit(uri.strip())
        self.parts = parts
        self.host = parts.netloc
        self.query = urllib.parse.parse_qs(parts.query)
        self._normalized = f"{parts.netloc}{parts.path}"
        if self.query:
            self._normalized += f"?{parts.query}"

    @property
    def normalized(self):
        return f"moz-extension://{self._normalized}"

    def __getitem__(self, key):
        """get a query parameter"""
        return self.query[key]

    def __setitem__(self, key, value):
        """set a query parameter"""
        if isinstance(value, list):
            self.query[key] = value
        else:
            self.query[key] = [value]


supported_schemes = {}
for scheme, obj in dict(globals()).items():
    if inspect.isclass(obj) and issubclass(obj, URI):
        scheme = scheme.lower()[:-3]
        separator = "-"
        if scheme.startswith("web"):
            separator = "+"
        supported_schemes[scheme.replace("_", separator)] = obj


"""
[Public Suffix List][1] support.

    >>> split_suffix("www.example.org")
    DomainParts(subdomain='www', domain='example', suffix='org')

Based upon the original implementation [`publicsuffix`][2] copyright
@[Tomaž Solc][3] and released under an MIT license.

[1]: https://publicsuffix.org/list/
[2]: https://pypi.python.org/pypi/publicsuffix
[3]: https://tablix.org

"""

_suffixes = None


@dataclass
class DomainParts:
    """A domain's parts."""

    subdomain: str
    domain: str
    suffix: str


class SuffixNotFoundError(Exception):
    """Suffix not found."""

    def __init__(self, url):
        """No suffix found."""
        self.message = f"No suffix found in `{url}`"
        super().__init__(self.message)


def split_suffix(hostname) -> DomainParts:
    """
    Return the subdomain and domain of given `hostname`.

        >>> split_suffix("www.example.org")
        DomainParts(subdomain='www', domain='example', suffix='org')
        >>> split_suffix("www.example.org.uk")
        DomainParts(subdomain='www', domain='example', suffix='org.uk')

    """
    # TODO handle Punycode decoding
    global _suffixes
    if _suffixes is None:
        _suffixes = PublicSuffixList()
    parts = hostname.lower().lstrip(".").split(".")
    hits = [None] * len(parts)
    _suffixes.lookup(hits, 1, parts)
    for i, what in enumerate(hits):
        if what is not None and what == 0:
            suffix_start = i + 1
            return DomainParts(
                subdomain=".".join(parts[:i]),
                domain=parts[i],
                suffix=".".join(parts[suffix_start:]),
            )
    raise SuffixNotFoundError(hostname)


class PublicSuffixList:
    """Reads and parses the public suffix list."""

    def __init__(self):
        input_path = pkg_resources.resource_filename(
            "easyuri", "public_suffix_list.dat"
        )
        # try:
        with codecs.open(input_path, "r", "utf8") as fp:
            self._build_structure(fp)
        # except FileNotFoundError:
        #     res = requests.get("https://publicsuffix.org/list/public_suffix_list.dat")
        #     with codecs.open(input_path, "w", "utf8") as fp:
        #         fp.write(res.text)
        #     with codecs.open(input_path, "r", "utf8") as fp:
        #         self._build_structure(fp)

    def lookup(self, matches, depth, parts, parent=None):
        if parent is None:
            parent = self.root
        if parent in (0, 1):
            negate = parent
            children = None
        else:
            negate, children = parent
        matches[-depth] = negate
        if depth < len(parts) and children:
            for name in ("*", parts[-depth]):
                child = children.get(name, None)
                if child is not None:
                    self.lookup(matches, depth + 1, parts, child)

    def _build_structure(self, fp):
        root = [0]
        for line in fp:
            line = line.strip()
            if line.startswith("//") or not line:
                continue
            self._add_rule(root, line.split()[0].lstrip("."))
        self.root = self._simplify(root)

    def _add_rule(self, root, rule):
        if rule.startswith("!"):
            negate = 1
            rule = rule[1:]
        else:
            negate = 0
        parts = rule.split(".")
        self._find_node(root, parts)[0] = negate

    def _find_node(self, parent, parts):
        if not parts:
            return parent
        if len(parent) == 1:
            parent.append({})
        assert len(parent) == 2
        negate, children = parent
        child = parts.pop()
        child_node = children.get(child, None)
        if not child_node:
            children[child] = child_node = [0]
        return self._find_node(child_node, parts)

    def _simplify(self, node):
        if len(node) == 1:
            return node[0]
        return (node[0], dict((k, self._simplify(v)) for (k, v) in node[1].items()))
