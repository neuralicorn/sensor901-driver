# coding: utf-8

import socket

from sensor901 import DataParser


def test():
    import time  # Import the time module

    from loguru import logger

    cnt = 0
    fps_counter = 0
    start_time = time.time()  # Record the starting time for FPS calculation

    def updateData(parser: DataParser, data: bytes):
        nonlocal cnt, fps_counter, start_time

        frames = parser.parse(data)

        for frame in frames:
            # Increment the frame counter
            fps_counter += 1

            # Calculate the elapsed time
            elapsed_time = time.perf_counter_ns() - start_time

            # If at least one second has passed, calculate FPS
            if elapsed_time >= 1e9:
                fps = fps_counter / (elapsed_time / 1e9)
                # logger.info(f"FPS: {fps:.2f}")
                # Reset for the next second
                fps_counter = 0
                start_time = time.perf_counter_ns()

            if cnt % 10 == 0:
                offset = frame.angle_x + 90
                offset = min(max(offset, 0), 180)
                print(f"{frame.acc_z:.2f}".rjust(8),
                      ' ' * round(offset // 2) + '|',
                      flush=True)
                # print(frame.angle_x)
            cnt += 1

    # Simulate test environment
    parser = DataParser()

    # listen on UDP port 1399
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('0.0.0.0', 1399))
            while True:
                data, addr = s.recvfrom(1024)
                updateData(parser, data)
    except KeyboardInterrupt:
        pass


# Example usage
if __name__ == "__main__":
    test()
