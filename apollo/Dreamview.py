from websocket import create_connection
import time
import json
import logging


class Dreamview:
    def __init__(self, ip: str, port: int) -> None:
        self.url = f"ws://{ip}:{port}/websocket"
        # self.ws = create_connection(self.url)
        # self.ws.close()

    # def reconnect(self):
    #     '''
    #     Closes the websocket connection and re-creates it so that data can be received again
    #     '''
    #     self.ws.close()
    #     self.ws = create_connection(self.url)

    def send_data(self, data: dict):
        ws = create_connection(self.url)
        ws.send(json.dumps(data))
        ws.close()

    def start_sim_control(self):
        # self.ws.send(
        #     json.dumps({
        #         "type": "StartSimControl"
        #     })
        # )
        self.send_data({
            "type": "StartSimControl"
        })

    def stop_sim_control(self):
        # self.ws.send(
        #     json.dumps({
        #         "type": "StopSimControl"
        #     })
        # )
        self.send_data({
            "type": "StopSimControl"
        })

    def reset(self):
        # self.ws.send(
        #     json.dumps({
        #         "type": "Reset"
        #     })
        # )
        self.send_data({
            "type": "Reset"
        })
