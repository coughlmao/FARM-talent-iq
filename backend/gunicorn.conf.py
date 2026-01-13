import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1  # number of worker processes
worker_class = "uvicorn.workers.UvicornWorker"  # tells Gunicorn to use ASGI
bind = "0.0.0.0:8000"  # host:port
timeout = 120  # max request time in seconds
loglevel = "info"  # info/debug/error
accesslog = "-"  # stdout
errorlog = "-"   # stdout