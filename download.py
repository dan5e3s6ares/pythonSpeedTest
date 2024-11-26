import requests


class FileDownloader:
    def __init__(self, url):
        self.url = url

    def download(self, save_path):
        response = requests.get(self.url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {save_path}")


# Example usage:
# downloader = FileDownloader('https://example.com/file.zip')
# downloader.download('/path/to/save/file.zip')# downloader.download('/path/to/save/file.zip')
