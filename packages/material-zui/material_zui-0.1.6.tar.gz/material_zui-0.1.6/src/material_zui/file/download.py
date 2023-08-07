from urllib.request import urlopen


def download(url: str, output_path: str, timeout: float | None = 120) -> None:
    '''
    @output_path: like `path/title.mp4`
    @timeout: in seconds, default `120 seconds`, input `None` for timeout
    '''
    mp4_file = urlopen(url, timeout=timeout)
    with open(output_path, "wb") as output:
        while True:
            data = mp4_file.read(4096)
            if data:
                output.write(data)
            else:
                break


def download_once(urls: list[str], output_path: str, timeout: float | None = 120) -> None:
    """
    Download from list url until have 1 url successfully download
    @output_path: like `path/title.mp4`
    @timeout: in seconds, default 120 seconds
    """
    for url in urls:
        try:
            download(url, output_path, timeout)
            break
        except:
            print('Error downloading:', url)
