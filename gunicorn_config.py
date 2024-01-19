from multiprocessing import cpu_count

bind = "0.0.0.0:8000"
workers = cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
reload_extra_files = ['/app/panels_project']
