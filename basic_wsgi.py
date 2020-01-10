from werkzeug.serving
import run_simple


def wsgi(environ, start_response):
    print(environ)
    environ["HTTP_REFERER"]

    start_response('200 Ok', [('Content-Type', 'text/html'), ("Acces-Control-Allow-Origin", "Lloc segur")])
    return [b "Hello, world!"]


if __name__ == "__main__":
    run_simple("127.0.0.1", 8080, wsgi)


# {
#     'wsgi.version': (1, 0),
#     'wsgi.url_scheme': 'http',
#     'wsgi.input': < _io.BufferedReader name = 4 > ,
#     'wsgi.errors': < _io.TextIOWrapper name = '<stderr>'
#     mode = 'w'
#     encoding = 'UTF-8' > ,
#     'wsgi.multithread': False,
#     'wsgi.multiprocess': False,
#     'wsgi.run_once': False,
#     'werkzeug.server.shutdown': < function WSGIRequestHandler.make_environ. < locals > .shutdown_server at 0x7fe6d1aa7ea0 > ,
#     'SERVER_SOFTWARE': 'Werkzeug/0.16.0',
#     'REQUEST_METHOD': 'GET',
#     'SCRIPT_NAME': '',
#     'PATH_INFO': '/favicon.ico',
#     'QUERY_STRING': '',
#     'REQUEST_URI': '/favicon.ico',
#     'RAW_URI': '/favicon.ico',
#     'REMOTE_ADDR': '127.0.0.1',
#     'REMOTE_PORT': 57176,
#     'SERVER_NAME': '127.0.0.1',
#     'SERVER_PORT': '8080',
#     'SERVER_PROTOCOL': 'HTTP/1.1',
#     'HTTP_HOST': 'localhost:8080',
#     'HTTP_CONNECTION': 'keep-alive',
#     'HTTP_PRAGMA': 'no-cache',
#     'HTTP_CACHE_CONTROL': 'no-cache',
#     'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
#     'HTTP_ACCEPT': 'image/webp,image/apng,image/*,*/*;q=0.8',
#     'HTTP_SEC_FETCH_SITE': 'same-origin',
#     'HTTP_SEC_FETCH_MODE': 'no-cors',
#     'HTTP_REFERER': 'http://localhost:8080/',
#     'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br',
#     'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.9,es;q=0.8,ca;q=0.7,pl;q=0.6'
# }