from enum import Enum
from typing import List


class LabEnum(str, Enum):
    """Base class for Enum classes with values classmethod."""

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, str):
            return self.value == other
        else:
            return super().__eq__(other)

    def __str__(self):
        return self.value

    @classmethod
    def values(cls) -> List[str]:
        return list(map(str, cls))

    @classmethod
    def map_to_ext(cls, lang) -> str:
        if lang in [cls.python3]:
            return 'py'
        elif lang == cls.nodejs:
            return 'js'
        elif lang == cls.java:
            return 'java'
        elif lang == cls.cpp:
            return 'cpp'
        elif lang == cls.html_css_js:
            return 'html'
        elif lang == cls.eiffel:
            return 'e'
        elif lang == cls.c_lang:
            return 'c'
        elif lang == cls.haskell:
            return 'hs'
        elif lang == cls.go:
            return 'go'
        elif lang == cls.kotlin:
            return 'kt'
        elif lang == cls.unspecified:
            return 'unspecified'
        else:
            return None

    @classmethod
    def map_to_separator(cls, lang) -> str:
        if lang in [cls.python3, cls.eiffel, cls.haskell, cls.java, cls.go, cls.unspecified, cls.kotlin]:
            return '_'
        elif lang in [cls.html_css_js, cls.nodejs]:
            return '-'
        else:
            return '.'

    @classmethod
    def map_to_other(cls, lang) -> str:
        if lang in [cls.cpp, cls.c_lang]:
            return 'h'
        elif lang == cls.html_css_js:
            return 'css'
        elif lang == cls.java:
            return 'main'
        else:
            return 'n'

    @classmethod
    def map_to_extra(cls, lang) -> str:
        if lang == cls.html_css_js:
            return "js"
        else:
            return 'n'
    
    @classmethod
    def map_to_default_root(cls, lang) -> str:
        if lang == cls.eiffel:
            return "application"
        else:
            return 'n'

    @classmethod
    def map_to_test_file(cls, lang) -> str:
        if lang == cls.eiffel:
            return "unittest"
        else:
            return ''


class Language(LabEnum):
    """Allowed languages."""

    python3 = 'python3'
    ruby = 'ruby'
    clojure = 'clojure'
    php = 'php'
    nodejs = 'nodejs'
    nodejs_server = 'nodejs-server'
    scala = 'scala'
    go = 'go'
    cpp = 'cpp'
    java = 'java'
    v_basic = 'v_basic'
    c_sharp = 'c_sharp'
    bash = 'bash'
    objective_c = 'objective_c'
    mysql = 'mysql'
    perl = 'perl'
    rust = 'rust'
    html_css_js = 'html-css-js'
    unspecified = 'unspecified'
    eiffel = 'eiffel'
    c_lang = 'c-lang'
    haskell = 'haskell'
    kotlin = 'kotlin'

    @property
    def ext(self) -> str:
        return self.map_to_ext(self.value)


class TestsType(LabEnum):
    unit = 'unit'
    input = 'input'  # noqa: A003


