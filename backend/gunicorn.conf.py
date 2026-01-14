import os

port = os.getenv("PORT", "10000")
bind = f"0.0.0.0:{port}"  # host:port

workers = 1  # number of worker processes
worker_class = "uvicorn.workers.UvicornWorker"  # tells Gunicorn to use ASGI
timeout = 120  # max request time in seconds
loglevel = "info"  # info/debug/error
accesslog = "-"  # stdout
errorlog = "-"   # stdout