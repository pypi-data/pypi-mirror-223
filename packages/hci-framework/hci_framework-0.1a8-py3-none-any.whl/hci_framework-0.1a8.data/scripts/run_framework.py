#!python

from hci_framework.utils import Workers
import webbrowser

workers = Workers(swarm_advertise_addr='192.168.1.54')

workers.stop_all_workers()

# Basic services
# workers.swarm.start_jupyter(restart=True)
# workers.swarm.start_kafka(restart=True)
workers.swarm.start_kafka_logs(restart=True)
# workers.swarm.start_timescaledb(restart=True)

# # Basic workers
# port = workers.start_django_worker('timescaledb_api', endpoint='/timescaledbapp/', restart=True)
# webbrowser.open_new_tab(f'http://127.0.0.1:{port}/timescaledbapp/')

# # Example Brython worker
# port = workers.start_brython_worker('fps', restart=True)
# webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')

# port = workers.start_brython_worker('main_app', restart=True)
# webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')

# # Example Django worker
# port = workers.start_django_worker('djangotest', restart=True)
# webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')

# port = workers.start_worker('worker', restart=True)
# webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')

# port = workers.start_worker('main_app', restart=True)
# webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')


# webbrowser.open_new_tab(f'http://127.0.0.1:8888/')
