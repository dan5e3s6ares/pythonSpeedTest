import json
import time
from datetime import datetime

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SpeedTest:
    def __init__(self):
        self.results = {}

    def run_test(self):
        # Teste de latência
        start_time = datetime.now()
        response = requests.get(
            "https://www.google.com", stream=True, verify=False
        )
        end_time = datetime.now()
        latency = (end_time - start_time).total_seconds()
        self.results["latency"] = {
            "latency": latency,
            "status_code": response.status_code,
            "url": response.url,
            "timestamp": datetime.now().isoformat(),
        }

        # Teste de download
        file_url = "https://drive.usercontent.google.com/download?id=1FLCjBmrR-qe6x9Ugu1dFaLhtzoKusAzU&export=download&confirm=t&uuid=2aba5ca8-70d7-4329-a7a4-d7886c325fb0"
        # https://drive.google.com/file/d/1FLCjBmrR-qe6x9Ugu1dFaLhtzoKusAzU/view?usp=drive_link
        # URL de um arquivo grande para teste de download
        start_time = datetime.now()
        response = requests.get(file_url, stream=True, verify=False)
        end_time = datetime.now()
        download_time = (end_time - start_time).total_seconds()
        file_size = int(response.headers.get("content-length", 0))
        download_speed = file_size * 8 / download_time / 1024 / 1024  # Mbps
        self.results["download"] = {
            "speed_mbps": download_speed,
            "time_seconds": download_time,
            "file_size_bytes": file_size,
            "url": file_url,
            "status_code": response.status_code,
            "timestamp": datetime.now().isoformat(),
        }

        # Teste de upload
        upload_url = "https://httpbin.org/post"
        data = b"a" * 10 * 1024 * 1024  # 10MB de dados para upload
        start_time = datetime.now()
        response = requests.post(upload_url, data=data, verify=False)
        end_time = datetime.now()
        upload_time = (end_time - start_time).total_seconds()
        upload_speed = len(data) * 8 / upload_time / 1024 / 1024  # Mbps
        self.results["upload"] = {
            "speed_mbps": upload_speed,
            "time_seconds": upload_time,
            "file_size_bytes": len(data),
            "url": upload_url,
            "status_code": response.status_code,
            "response_headers": response.json()["headers"],
            "response_origin": response.json()["origin"],
            "timestamp": datetime.now().isoformat(),
        }

    def save_results(self, filename):
        print(self.results)
        with open(filename, "a") as file:
            json.dump(self.results, file)
            file.write("\n")

    def start(self):
        start_time = time.time()
        while time.time() - start_time < 86400:
            self.run_test()
            self.save_results("speedtest_results.json")


if __name__ == "__main__":
    tester = SpeedTest()
    tester.start()
