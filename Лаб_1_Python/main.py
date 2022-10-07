import urllib3
import time
import sys
from threading import Thread


CHUNK_SIZE = 1024

downloaded_size: int = 0
file_size: float = 0


def convert_to_Mbytes(size: int) -> float:
    """

    :param size: in bytes
    :return: size in MB
    """
    return round(size / 1024 / 1024, 2)


def download_file(url: str):
    global downloaded_size
    global file_size

    url_connection = urllib3.PoolManager()
    response = url_connection.request("GET", url, preload_content=False)

    file_name = url.split("/")[-1]
    file_size = convert_to_Mbytes(int(response.getheader("Content-Length")))

    with open(file_name, "wb") as file:
        while chunk := response.read(CHUNK_SIZE):
            file.write(chunk)

            downloaded_size += CHUNK_SIZE


def print_progress():
    while True:
        time.sleep(1)
        print(f"alredy downloaded.........[{convert_to_Mbytes(downloaded_size)}MB/{file_size}MB]")

        if convert_to_Mbytes(downloaded_size) >= file_size:
            print(f"Downloaded successfully...[{file_size}MB/{file_size}MB]")
            break


if __name__ == "__main__":
    thread = Thread(target=print_progress)
    thread.start()

    download_file(sys.argv[1])
