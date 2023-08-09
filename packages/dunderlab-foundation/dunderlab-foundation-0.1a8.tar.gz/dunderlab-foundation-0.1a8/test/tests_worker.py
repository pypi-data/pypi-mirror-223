from hci_framework.utils import Workers
import webbrowser

workers = Workers()
# workers.stop_all_workers()

port = workers.start_worker('figurestream_brython_worker', service_name='worker', restart=True)
webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')

# workers.swarm.start_kafka_logs(restart=True)
# port = workers.start_worker('python_logs', service_name='namae2', restart=True)


# port = workers.start_worker('python_logs', service_name='python_logs', restart=True)
# webbrowser.open_new_tab(f'http://127.0.0.1:{port}/')
