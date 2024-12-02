import os
import requests
from dotenv import load_dotenv
from utils import file_extensions

class Filehandler:
  def __init__(self, data: dict[str, str] | None = None, links: list[str] | None = None, download_directory: str | None = None):
    load_dotenv()
    self.data = data or None
    self.links = links or None
    self.download_directory = os.getenv("DOWNLOAD_DIRECTORY") or "download"


  def map_writer(self, links, download_directory) -> None:
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    for link in links:
      try:
        file_name = link.split('/')[-1]
        ext = link.split('.')[-1]
        path = f"{download_directory}/{ext}"
        file_path = os.path.join(path, file_name)

        print(f"Downloading {link}...")
        response = requests.get(link, stream=True)

        if response.status_code == 200:
          with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
              if chunk:
                file.write(chunk)
          print(f"Downloaded: {file_path}")
        else:
          print(f"Failed to download {link}: Status code {response.status_code}")

      except Exception as e:
        print(f"Error downloading {link}: {e}")

  def crawl_writer(self, data, download_directory) -> None:
    if not os.path.exists(download_directory):
      os.makedirs(download_directory)

    for key, value in data.items():
      print(key, "key")
      filename_base = key.split('/')[-2]

      for content_type, extension in file_extensions.items():
        if content_type in value:
          filename = f"{filename_base}{extension}"
          print(filename, "fn")
          path = f"{download_directory}/{content_type}"
          file_path = os.path.join(path, filename)
          content = value.get(content_type, '')
          try:
            with open(file_path, 'w', encoding='utf-8') as file:
              file.write(content)
              print(f"Written to {file_path}")
          except Exception as e:
              print(f"Error writing to {file_path}: {e}")

if __name__ == "__main__":
  fh = Filehandler()
