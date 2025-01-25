import math
import socket
import threading
import time
from dataclasses import dataclass

from .data import Frame


class Simulator:

    def __init__(self, name: str):
        self.name = name
        self.running = False

        self.interval = 0.1

        self.thread: threading.Thread | None = None

    def generate_frame(self, timestamp: str, index: int) -> Frame:
        # Simulate sine wave for sensor data
        sine_value = math.sin(index * 0.1)
        return Frame(device_name=self.name,
                     time=timestamp,
                     acc_x=sine_value,
                     acc_y=sine_value,
                     acc_z=sine_value,
                     as_x=sine_value,
                     as_y=sine_value,
                     as_z=sine_value,
                     gx=sine_value,
                     gy=sine_value,
                     gz=sine_value,
                     angle_x=sine_value,
                     angle_y=sine_value,
                     angle_z=sine_value,
                     temp=25.0 + sine_value,
                     electric_quantity=100,
                     rssi=-50,
                     version=1)

    def mainloop(self, endpoint: tuple[str, int]):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        index = 0
        while self.running:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            frame = self.generate_frame(timestamp, index)
            data = b'\x57\x54' + frame.serialize()
            sock.sendto(data, endpoint)
            index += 1
            time.sleep(self.interval)

        sock.close()

    def start(self, endpoint: tuple[str, int]):
        self.running = True
        self.thread = threading.Thread(target=self.mainloop,
                                       args=(endpoint, ),
                                       daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False


# Example usage
if __name__ == "__main__":
    simulator = Simulator("Device001")
    simulator.start(("localhost", 12345))
    time.sleep(10)  # Run the simulator for 10 seconds
    simulator.stop()
