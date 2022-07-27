from websocket import create_connection
import time
import json
import logging


class Dreamview:
    def __init__(self, ip: str, port: int) -> None:
        self.url = f"ws://{ip}:{port}/websocket"

    def send_data(self, data: dict):
        ws = create_connection(self.url)
        ws.send(json.dumps(data))
        ws.close()

    def start_sim_control(self):
        self.send_data({
            "type": "StartSimControl"
        })

    def stop_sim_control(self):
        self.send_data({
            "type": "StopSimControl"
        })

    def reset(self):
        self.send_data({
            "type": "Reset"
        })
