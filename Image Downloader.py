import time
import requests
import os
from fake_useragent import UserAgent
from http import HTTPStatus


def get_extensions(url: str) -> str | None:
    """get and verify the extensions in the link"""
    extensions: list[str] = ['.png', '.jpg', '.jpeg', '.svg', '.gif']

    for extension in extensions:
        if extension in url:
            return extension


def verify_link(url: str) -> str | None:
    """Validate link or URL if it has https"""

    link: list[str] = url.split(":")

    try:
        if 'https' in link or 'http' in link:
            return url

        else:
            raise Exception("Could not download the image please double check you URL...")

    except Exception as e:
        print()
        print(e)


def create_folder(folder: str) -> None:
    """Create the folder if it does not exist"""
    if not os.path.exists(folder):
        os.makedirs(folder)

    else:
        pass


def download_image(url: str, name: str, header: dict, folder_path: str) -> None:
    """"Download the Image based on the user url and file name"""

    # Create Folder if it does not exist
    create_folder(folder_path)

    if extension := get_extensions(url):

        file_name: str = f'{name}{extension}'
        path: str = os.path.join(folder_path, file_name)

        if os.path.isfile(path):
            raise Exception('File Name already Exists..')

        # Get response from the given URL
        link: str = verify_link(url)
        response = requests.get(link, headers=header)
        status: int = response.status_code

        # Check if the status of URL is active or not
        if HTTPStatus(status).name == "OK":
            print("Downloading... Please wait")

            with open(path, "wb") as download_img:
                download_img.write(response.content)
                download_img.flush()
                os.fsync(download_img.fileno())

            print()
            print(f"Image ({file_name}) has been downloaded successfully [path: {path}]")
            print("Exiting the System Please wait...")
            time.sleep(2)

        else:
            print('-' * 75)
            raise Exception("Download Failed (Status Code: {} {})".format(status, HTTPStatus(status).phrase))

    else:
        raise Exception('Image Extension could not be located in the given link')


def main():
    """Initializer"""
    header: dict = {"user_agent": str(UserAgent.firefox)}
    path: str = "images"

    try:
        input_url: str = input("Input your Url >> ")
        input_name: str = input("What would you like to name your file? >> ")

        if input_url in invalid_type:

            if input_name in invalid_type:
                raise Exception('Invalid URL and Name Please Try Again...')

            raise Exception('Invalid URL Please Try Again...')

        elif input_name in invalid_type:
            raise Exception('Invalid Name Please Try Again!...')

        else:
            download_image(input_url, name=input_name, header=header, folder_path=path)

    except Exception as e:
        print(e)
        print("-" * 75)
        time.sleep(1)
        main()


if __name__ == '__main__':
    invalid_type = ("", " ")
    main()