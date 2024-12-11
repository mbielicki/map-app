import json
from rtt import file_rtt, rtt
from app import App
import time

def start_rtt(app: App):
    app.rtt_button.disable() # TODO change to stop_rtt button
    app.rtt = rtt()
    # app.rtt = file_rtt('data/test-1.json')

def process_rtt(app: App):
    if not app.rtt: return

    app.rtt_buffer += next(app.rtt)

    try:
        info_str = find_info(app.rtt_buffer)
    except NoStartError:
        app.rtt_buffer = ''
        return

    if info_str:
        info = json.loads(info_str)
        app.rtt_buffer = ''
        on_info_received(app, info)

start_time = time.time()
def now():
    return f'{(time.time() - start_time):.3f}'

def on_info_received(app: App, info: dict):
    info['timestamp'] = now()
    print(info)  # TODO add dist to node, trilaterate
    with open('data/test-3.json', 'a') as f:
        f.write(json.dumps(info) + '\n')
    app.update_nodes(info)


class NoStartError(Exception): pass

def find_info(data: str) -> str:
    start_i = data.find('{')

    if start_i == -1 and len(data) > 2:
        raise NoStartError()

    end_i = data.find('}')

    if end_i == -1:
        return None

    return data[start_i:end_i+1]