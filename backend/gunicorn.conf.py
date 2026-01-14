import os
import gc

# 1. Port & Binding
port = os.getenv("PORT", "10000")
bind = f"0.0.0.0:{port}"

# 2. Worker Configuration (Keep at 1 for 512MB limit)
workers = 1 
worker_class = "uvicorn.workers.UvicornWorker"

# 3. MEMORY OPTIMIZATIONS
# Preload loads the app once in the parent process before forking.
# This ensures workers share the same memory space for the initial app load.
preload_app = True

# Max requests restarts the worker after 1000 requests to clear memory leaks.
# Max requests jitter prevents all workers from restarting at the exact same time.
max_requests = 100
max_requests_jitter = 20

# 4. Force Garbage Collection
# Freezes the generational GC to improve memory sharing between processes.
def on_starting(server):
    gc.freeze()

# 5. Standard Configs
timeout = 120
loglevel = "info"
accesslog = "-"
errorlog = "-"