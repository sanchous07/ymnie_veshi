import argparse
import json
from pathlib import Path
import subprocess
import time
import matplotlib.pyplot as plt

import numpy as np
import spidev


def read_response(spi):
    # Пропускаем нули до начала ответа Pico.
    start = b""
    deadline = time.monotonic() + 40
    while start != b"SND2":
        start = (start + bytes(spi.xfer2([0])))[-4:]
        if time.monotonic() > deadline:
            raise TimeoutError("Pico не отвечает")

    # Первые 4 байта — длина ответа. Следующие 4 (CRC) пропускаем.
    header = bytes(spi.xfer2([0] * 8))
    size = int.from_bytes(header[:4], "little")
    data = bytearray()
    for offset in range(0, size, 64):
        data.extend(spi.xfer2([0] * min(64, size - offset)))
    return bytes(data)


def main():
    parser = argparse.ArgumentParser(description="Запись двух микрофонов на Raspberry Pi")
    parser.add_argument("directory", help="Папка для записи")
    parser.add_argument("--threshold", type=int, default=40, help="Порог запуска, по умолчанию 20")
    args = parser.parse_args()

    spi = spidev.SpiDev()
    spi.open(0, 0)
    try:
        spi.mode = 0
        spi.max_speed_hz = 10000
        spi.bits_per_word = 8
        spi.lsbfirst = False
        spi.no_cs = True

        # Сбрасываем предыдущий обмен, затем выбираем Pico.
        subprocess.run(["raspi-gpio", "set", "8", "op", "dh"], check=True)
        time.sleep(0.06)
        subprocess.run(["raspi-gpio", "set", "8", "op", "dl"], check=True)

        spi.xfer2(list(f"capture {args.threshold} 15000\n".encode()))
        armed = json.loads(read_response(spi))
        if "reason" in armed:
            raise RuntimeError(armed["reason"])
        print("Через секунду хлопните возле микрофона 0. Затем дождитесь передачи.", flush=True)

        header, _, payload = read_response(spi).partition(b"\n")
        settings = json.loads(header)
        if "reason" in settings:
            raise RuntimeError(settings["reason"])
        samples = np.frombuffer(payload, dtype="<u2").reshape(-1, 2)
    finally:
        try:
            spi.no_cs = False
        finally:
            spi.close()
            subprocess.run(["raspi-gpio", "set", "8", "a0"], check=True)

    directory = Path(args.directory)
    directory.mkdir(parents=True)
    np.savetxt(directory / "data_0.txt", samples[:, 0], fmt="%d")
    np.savetxt(directory / "data_1.txt", samples[:, 1], fmt="%d")
    print(f"Сохранено {len(samples)} отсчётов каждого микрофона: {directory}")

    plt.plot(samples[:, 0], label="микрофон 0")
    plt.plot(samples[:, 1], label="микрофон 1")
    plt.xlabel("номер отсчета")
    plt.ylabel("код АЦП")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
