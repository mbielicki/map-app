import json
from rtt import file_rtt, rtt
from app import App

def start_rtt(app: App):
    app.rtt_button.disable() # TODO change to stop_rtt button
    # app.rtt = rtt()
    app.rtt = file_rtt('data/test-3.json')

def process_rtt(app: App):
    if not app.rtt: return

    try:
        app.rtt_buffer += next(app.rtt)
    except StopIteration:
        app.rtt = None

    try:
        info_str, info_str_rest = find_info(app.rtt_buffer)
    except NoStartError:
        app.rtt_buffer = ''
        return

    if info_str:
        info = json.loads(info_str)
        app.rtt_buffer = info_str_rest
        on_info_received(app, info)



def on_info_received(app: App, info: dict):
    print(info)
    app.update_nodes(info)

def log_info(app: App, info: dict):
    info['timestamp'] = app.now_str()
    with open('data/test-4.json', 'a') as f:
        f.write(json.dumps(info) + '\n')

class NoStartError(Exception): pass

def find_info(data: str) -> tuple[str, str]:
    start_i = data.find('{')

    if start_i == -1 and len(data) > 2:
        raise NoStartError()

    end_i = data.find('}')

    if end_i == -1:
        return None, None

    return data[start_i:end_i+1], data[end_i+1:]