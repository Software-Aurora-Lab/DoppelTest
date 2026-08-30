from cyber.python.cyber_py3 import cyber
from modules.planning.proto.planning_pb2 import ADCTrajectory
from time import time

# bazel run //modules/custom_nodes:simplified_planning


class SimplifiedPlanning:
    def __init__(self) -> None:
        curr_time = time()
        self.node = cyber.Node(f"SimplifiedPlanning_{curr_time}")

        self.writer = self.node.create_writer(
            "/apollo/planning/simplified", ADCTrajectory)

        def callback(data):
            simplified = ADCTrajectory(
                header=data.header,
                decision=data.decision,
                total_path_length=data.total_path_length,
                total_path_time=data.total_path_time,
            )
            self.writer.write(simplified)

        self.reader = self.node.create_reader(
            "/apollo/planning",
            ADCTrajectory,
            callback
        )

    def spin(self):
        self.node.spin()


if __name__ == '__main__':
    cyber.init()
    SimplifiedPlanning().spin()
