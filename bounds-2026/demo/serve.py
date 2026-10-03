#!/usr/bin/env python3
"""Static server for the demo: listens on $PORT, binds $ISOMUX_APP_HOST (default: all interfaces)."""
import functools, http.server, os
DIR = os.path.dirname(os.path.abspath(__file__))
host, port = os.environ.get('ISOMUX_APP_HOST', ''), int(os.environ.get('PORT', '8000'))
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIR)
http.server.ThreadingHTTPServer((host, port), handler).serve_forever()
