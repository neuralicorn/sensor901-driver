# coding: utf-8

from dataclasses import dataclass

# coding: utf-8


@dataclass
class Frame:
    device_name: str  # Name of the device sending the data
    time: str  # Timestamp of the data
    acc_x: float  # Acceleration in the X-axis
    acc_y: float  # Acceleration in the Y-axis
    acc_z: float  # Acceleration in the Z-axis
    as_x: float  # Angular speed in the X-axis
    as_y: float  # Angular speed in the Y-axis
    as_z: float  # Angular speed in the Z-axis
    gx: float  # Gyroscope reading in the X-axis
    gy: float  # Gyroscope reading in the Y-axis
    gz: float  # Gyroscope reading in the Z-axis
    angle_x: float  # Angle in the X-axis
    angle_y: float  # Angle in the Y-axis
    angle_z: float  # Angle in the Z-axis
    temp: float  # Temperature reading
    electric_quantity: int  # Battery level or electric quantity
    rssi: int  # Received Signal Strength Indicator
    version: int  # Version of the sensor or firmware


class DataParser:

    @staticmethod
    def _parse_frame(fr: bytes):
        """
        Parse a single frame into a Frame object.

        Args:
            fr (bytes): A single frame as bytes.

        Returns:
            Frame: Parsed Frame object.
        """
        device_name = fr[:12].decode('ascii')
        time_data = "20{}-{}-{} {}:{}:{}.{}".format(fr[12], fr[13], fr[14],
                                                    fr[15], fr[16], fr[17],
                                                    (fr[19] << 8 | fr[18]))
        acc_x = DataParser.getSignInt16(fr[21] << 8 | fr[20]) / 32768 * 16
        acc_y = DataParser.getSignInt16(fr[23] << 8 | fr[22]) / 32768 * 16
        acc_z = DataParser.getSignInt16(fr[25] << 8 | fr[24]) / 32768 * 16
        as_x = DataParser.getSignInt16(fr[27] << 8 | fr[26]) / 32768 * 2000
        as_y = DataParser.getSignInt16(fr[29] << 8 | fr[28]) / 32768 * 2000
        as_z = DataParser.getSignInt16(fr[31] << 8 | fr[30]) / 32768 * 2000
        gx = DataParser.getSignInt16(fr[33] << 8 | fr[32]) * 100 / 1024
        gy = DataParser.getSignInt16(fr[35] << 8 | fr[34]) * 100 / 1024
        gz = DataParser.getSignInt16(fr[37] << 8 | fr[36]) * 100 / 1024
        angle_x = DataParser.getSignInt16(fr[39] << 8 | fr[38]) / 32768 * 180
        angle_y = DataParser.getSignInt16(fr[41] << 8 | fr[40]) / 32768 * 180
        angle_z = DataParser.getSignInt16(fr[43] << 8 | fr[42]) / 32768 * 180
        temp = DataParser.getSignInt16(fr[45] << 8 | fr[44]) / 100
        electric_quantity = fr[47] << 8 | fr[46]
        rssi = DataParser.getSignInt16(fr[49] << 8 | fr[48])
        version = DataParser.getSignInt16(fr[51] << 8 | fr[50])

        return Frame(device_name=device_name,
                     time=time_data,
                     acc_x=acc_x,
                     acc_y=acc_y,
                     acc_z=acc_z,
                     as_x=as_x,
                     as_y=as_y,
                     as_z=as_z,
                     gx=gx,
                     gy=gy,
                     gz=gz,
                     angle_x=angle_x,
                     angle_y=angle_y,
                     angle_z=angle_z,
                     temp=temp,
                     electric_quantity=electric_quantity,
                     rssi=rssi,
                     version=version)

    @staticmethod
    def getSignInt16(num):
        if num >= pow(2, 15):
            num -= pow(2, 16)
        return num

    def __init__(self):
        self.buffer = []

    def parse(self, data: bytes):
        """
        Parses the incoming data and returns a list of complete frames.

        Args:
            data (bytes): Incoming data as bytes.

        Returns:
            list[Frame]: A list of complete frames.
        """
        frames: list[Frame] = []

        # Add incoming data to the buffer
        self.buffer.extend(data)

        # Process buffer to extract complete frames
        while len(self.buffer
                  ) >= 54:  # Check if buffer has enough data for a frame
            if self.buffer[0] == 0x57 and self.buffer[
                    1] == 0x54:  # Check frame header
                # Extract one frame (54 bytes)
                frame = self.buffer[:54]
                frames.append(self._parse_frame(bytes(frame)))
                # Remove the frame from the buffer
                self.buffer = self.buffer[54:]
            else:
                # Discard invalid data at the start of the buffer
                del self.buffer[0]

        # Return the list of complete frames
        return frames


# Example usage
if __name__ == "__main__":
    parser = DataParser()

    # Simulate receiving fragmented data
    data_part1 = bytes([0x57, 0x54] + [0x00] * 52)  # First part of the frame
    data_part2 = bytes([0x57, 0x54] + [0x01] * 52)  # Second frame begins

    # Parse first part
    frames = parser.parse(data_part1)
    print("Frames after first part:", frames)  # Expect []

    # Parse second part
    frames = parser.parse(data_part2)
    print("Frames after second part:", frames)  # Expect two frames
