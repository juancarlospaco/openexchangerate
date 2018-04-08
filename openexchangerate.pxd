# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
#
# CYTHONIZE: cython -3 --verbose --no-docstrings --annotate python_module.py
# COMPILE: gcc -shared -fPIC -I /usr/include/python3.6 -o python_module.so python_module.c


cdef:
    char* __version__
    char* __license__
    char* __author__
    char* __email__
    char* __contact__
    char* __maintainer__
    char* __url__
    tuple __all__


cdef class OpenExchangeRates:

    cdef public str api_key, base, local_base
    cdef public object tipe

    cdef _parsed_response(self, char response)

    cdef inline _local_conversion(self, dict data, char local_base)
        # pass

    cdef latest(self)
        # pass

    cdef currencies(self)
        # pass

    cdef inline historical(self, object since_date)
        # pass
