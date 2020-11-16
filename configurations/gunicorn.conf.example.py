import multiprocessing as mp
bind = "127.0.0.1:<port>"
workers = mp.cpu_count() - 1
accesslog = "<service>-api.log"
