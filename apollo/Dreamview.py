from websocket import create_connection
import time
import json
import logging


class Dreamview:
    def __init__(self, ip: str, port: int) -> None:
        self.url = f"ws://{ip}:{port}/websocket"
        self.ws = create_connection(self.url)

    def reconnect(self):
        '''
        Closes the websocket connection and re-creates it so that data can be received again
        '''
        self.ws.close()
        self.ws = create_connection(self.url)

    def start_sim_control(self):
        self.ws.send(
            json.dumps({
                "type": "StartSimControl"
            })
        )

    def stop_sim_control(self):
        self.ws.send(
            json.dumps({
                "type": "StopSimControl"
            })
        )

    def reset(self):
        self.ws.send(
            json.dumps({
                "type": "Reset"
            })
        )
