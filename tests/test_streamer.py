import unittest
from pathlib import Path

from sensor901.data import Frame
from sensor901.parser import StreamParser


class TestFrame(unittest.TestCase):

    def test_deserialize(self):
        frame_data = Frame(device_name="Device001",
                           time="2020-01-01 00:00:00",
                           acc_x=0.0,
                           acc_y=0.0,
                           acc_z=0.0,
                           as_x=0.0,
                           as_y=0.0,
                           as_z=0.0,
                           gx=0.0,
                           gy=0.0,
                           gz=0.0,
                           angle_x=0.0,
                           angle_y=0.0,
                           angle_z=0.0,
                           temp=25.0,
                           electric_quantity=100,
                           rssi=-50,
                           version=1)

        stream_parser = StreamParser()

        # read file from __dir__ / 'test_frame.bin'
        with open(Path(__file__).parent / 'test_frame.bin', 'rb') as f:
            data = b'\x57\x54' + f.read()

        # also test with a corrupted frame at first
        buf: bytes = b'\x54\x22' + data[2:] + data * 10

        partial, buf = buf[:len(data) + 10], buf[len(data) + 10:]

        frames = stream_parser.parse(partial)
        self.assertEqual(len(frames), 0)

        partial, buf = buf[:len(data) + 3], buf[len(data) + 3:]

        frames = stream_parser.parse(partial)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0], frame_data)

        # read all
        frames = stream_parser.parse(buf)
        self.assertEqual(len(frames), 9)
        for f in frames:
            self.assertEqual(f, frame_data)


if __name__ == '__main__':
    unittest.main()
