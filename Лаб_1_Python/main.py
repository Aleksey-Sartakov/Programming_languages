import urllib3
from time import time
import sys


CHUNK_SIZE = 1024


def convert_to_Mbytes(size: int) -> float:
    """

    :param size: in bytes
    :return: size in MB
    """
    return round(size / 1024 / 1024, 2)


def download_file(url: str):
    url_connection = urllib3.PoolManager()
    response = url_connection.request("GET", url, preload_content=False)

    file_name = url.split("/")[-1]
    file_size = convert_to_Mbytes(int(response.getheader("Content-Length")))
    downloaded_size = 0

    prev_time = time()
    with open(file_name, "wb") as file:
        while chunk := response.read(CHUNK_SIZE):
            file.write(chunk)

            downloaded_size += CHUNK_SIZE

            if (cur_time := time()) - prev_time > 1.0:
                print(f"alredy downloaded.........[{convert_to_Mbytes(downloaded_size)}MB/{file_size}MB]")
                prev_time = cur_time

        print(f"Downloaded successfully...[{file_size}MB/{file_size}MB]")


if __name__ == "__main__":
    download_file(sys.argv[1])
