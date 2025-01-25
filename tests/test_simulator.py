import socket
import time
import unittest
from pathlib import Path

from loguru import logger

from sensor901 import Frame, StreamParser
from sensor901.simulator import Simulator


class TestSimulator(unittest.TestCase):

    def test_simulator(self):
        cnt = 0

        simulator = Simulator("Device001")
        simulator.start(("127.0.0.1", 1399))

        parser = StreamParser()

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('0.0.0.0', 1399))
            s.settimeout(1)
            final_frames = []

            while True:
                try:
                    data, addr = s.recvfrom(1024)
                    frames = parser.parse(data)
                    final_frames.extend(frames)
                    cnt += len(frames)
                except socket.timeout:
                    raise TimeoutError("simulator not sending data")

                if cnt >= 5:
                    break

            simulator.stop()

            self.assertIsNotNone(simulator.thread)
            assert simulator.thread is not None
            simulator.thread.join()

    def test_simulator_with_postprocess(self):
        cnt = 0

        simulator = Simulator("Device001")

        simulator.sine_postprocess = lambda x: 1e-2

        simulator.start(("127.0.0.1", 1399))

        parser = StreamParser()

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('0.0.0.0', 1399))
            s.settimeout(1)
            final_frames: list[Frame] = []

            while True:
                try:
                    data, addr = s.recvfrom(1024)
                    frames = parser.parse(data)
                    final_frames.extend(frames)
                    cnt += len(frames)
                except socket.timeout:
                    raise TimeoutError("simulator not sending data")

                if cnt >= 5:
                    break

            simulator.stop()

            self.assertIsNotNone(simulator.thread)
            assert simulator.thread is not None
            simulator.thread.join()

            self.assertGreaterEqual(final_frames[0].acc_x, (1e-2) * 0.94)
            self.assertLessEqual(final_frames[0].acc_x, (1e-2) * 1.06)


if __name__ == '__main__':
    unittest.main()
