import csv
import time

import matplotlib.pyplot as plt
import speedtest


class SpeedTest24Hrs:
    def __init__(
        self,
        interval=3600,
        duration=86400,
        output_file="speedtest_results.csv",
    ):
        self.interval = interval
        self.duration = duration
        self.output_file = output_file
        self.result = None
        with open(self.output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "download", "upload", "ping"])

    def run_speedtest(self):
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        return st.results.dict()

    def save_results(self):
        with open(self.output_file, "a") as f_object:
            writer = csv.writer(f_object)
            writer.writerow(
                [
                    self.result["timestamp"],
                    self.result["download"],
                    self.result["upload"],
                    self.result["ping"],
                ]
            )
            f_object.close()

    def generate_graph(self):
        timestamps = [result["timestamp"] for result in self.result]
        download_speeds = [
            result["download"] / 1e6 for result in self.result
        ]  # Convert to Mbps
        upload_speeds = [
            result["upload"] / 1e6 for result in self.result
        ]  # Convert to Mbps

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, download_speeds, label="Download Speed (Mbps)")
        plt.plot(timestamps, upload_speeds, label="Upload Speed (Mbps)")
        plt.xlabel("Time")
        plt.ylabel("Speed (Mbps)")
        plt.title("Internet Speed Over 24 Hours")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("speedtest_graph.png")
        plt.show()

    def start(self):
        start_time = time.time()
        while time.time() - start_time < self.duration:
            self.result = self.run_speedtest()
            self.result["timestamp"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime()
            )
            print(f"Speedtest completed at {self.result['timestamp']}")
            print(f"Download Speed: {self.result['download'] / 1e6} Mbps")
            print(f"Upload Speed: {self.result['upload'] / 1e6} Mbps")
            print("############################################")
            self.save_results()
        # self.generate_graph()


if __name__ == "__main__":
    print("############################################")
    speed_test = SpeedTest24Hrs()
    speed_test.start()
