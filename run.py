#!/usr/bin/python3

from core import app
from core.config import run

app.run(debug=run["debug"], threaded=run["threaded"], host=run["host"], port=run["port"])