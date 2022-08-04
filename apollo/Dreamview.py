from websocket import create_connection
import json


class Dreamview:
    """
    Class to wrap Dreamview connection
    """

    def __init__(self, ip: str, port: int) -> None:
        """
        Constructs all the attributes for Dreamview object

        Parameters:
            ip: str
                ip address of Dreamview
            port: int
                port of Dreamview
        """
        self.url = f"ws://{ip}:{port}/websocket"
        self.ws = create_connection(self.url)

    def send_data(self, data: dict):
        """
        Helper function to send data to Dreamview

        Parameters:
            data: dict
                data to be sent
        """
        # ws = create_connection(self.url)
        # ws.send(json.dumps(data))
        # ws.close()
        self.ws.send(json.dumps(data))

    def start_sim_control(self):
        """
        Starts SimControl
        """
        self.send_data({
            "type": "StartSimControl"
        })

    def stop_sim_control(self):
        """
        Stops SimControl
        """
        self.send_data({
            "type": "StopSimControl"
        })

    def reset(self):
        """
        Resets Dreamview
        """
        self.send_data({
            "type": "Reset"
        })
