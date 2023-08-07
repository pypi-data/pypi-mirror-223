import os

workers_location = os.path.dirname(__file__)


# ----------------------------------------------------------------------
def select_worker(worker):
    """"""
    return os.path.join(workers_location, worker)


# ----------------------------------------------------------------------
def list_workers():
    """"""
    workers = []
    for item in os.listdir(workers_location):
        if os.path.isdir(os.path.join(workers_location, item)) and not item.startswith('__'):
            workers.append(item)
    return workers

