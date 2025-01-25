import unittest
from pathlib import Path

from sensor901.data import Frame


class TestData(unittest.TestCase):

    def test_serialize_deserialize_loopback(self):
        frame = Frame(device_name="Device001",
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
        serialized = frame.serialize()
        self.assertIsInstance(serialized, bytes)

        deserialized_frame = Frame.parse(serialized)
        self.assertEqual(frame, deserialized_frame)

    def test_comparison(self):
        frame_a = Frame(device_name="Device001",
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
        frame_b = Frame(device_name="Device001",
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
        frame_c = Frame(device_name="Device001",
                        time="2020-01-01 00:00:00",
                        acc_x=0.0,
                        acc_y=0.0,
                        acc_z=0.0,
                        as_x=0.0,
                        as_y=0.0,
                        as_z=0.0,
                        gx=1.0,
                        gy=0.0,
                        gz=0.0,
                        angle_x=0.0,
                        angle_y=0.0,
                        angle_z=0.0,
                        temp=25.0,
                        electric_quantity=100,
                        rssi=-50,
                        version=1)

        self.assertEqual(frame_a, frame_b)
        self.assertNotEqual(frame_a, frame_c)
        self.assertNotEqual(frame_b, frame_c)

        # test different types
        self.assertNotEqual(frame_a, 1)
        self.assertNotEqual("aaa", frame_a)

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

        # read file from __dir__ / 'test_frame.bin'
        with open(Path(__file__).parent / 'test_frame.bin', 'rb') as f:
            data = f.read()

        parsed_frame = Frame.parse(data)
        self.assertEqual(frame_data, parsed_frame)

    def test_serialize(self):
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

        # read file from __dir__ / 'test_frame.bin'
        with open(Path(__file__).parent / 'test_frame.bin', 'rb') as f:
            data = f.read()

        serialized_frame = frame_data.serialize()
        self.assertEqual(data, serialized_frame)


if __name__ == '__main__':
    unittest.main()
