import os
from CTkMessagebox import CTkMessagebox
from http import HTTPStatus
import requests


class ImageValidationAndProcessing:

    def __init__(self, header: dict, invalid_type: tuple, log):
        self.header = header
        self.invalidType = invalid_type
        self.extensions = ['.png', '.jpeg', '.svg', '.gif', '.jpg']
        self.logger = log

    def download_img(self, *, url: str, name: str, folder_path: str):
        """
        Download the image in the specified folder path and file name
        :param url: The link/URL of the image that user wants to download
        :param name:  The File name of the image
        :param folder_path: The folder where the image will be saved
        :return None:
        """

        # create folder if it does not exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # get and verify if the given link have file extension
        if extension := self.get_extension(url):
            # Create the file name as well as the full folder path of the file where it will be stored/saved
            file_name: str = f'{name}{extension}'
            path: str = os.path.join(folder_path, file_name)

            # check and pop up window will be shown if the file name already exist in the folder
            if os.path.isfile(path):
                CTkMessagebox(message="File name, Already Exist!", title='Invalid file name',
                              icon='warning')
                self.logger.debug('Your input File Name already exist in the path')
                return   # stop the code in continuing

            # Get response from the given URL
            link: str | None = self.verify_link(url)
            response = requests.get(link, headers=self.header)
            status: int = response.status_code

            # get the status name from the link
            if HTTPStatus(status).name == 'OK':
                self.logger.info('Downloading the image...')

                # save the image from the given folder
                with open(path, 'wb+') as downloaded_img:
                    downloaded_img.write(response.content)
                    downloaded_img.flush()
                    os.fsync(downloaded_img.fileno())

                # pop up window will be shown if the image have download successfully
                CTkMessagebox(message=f"Image ({file_name}) has been downloaded successfully",
                              title='Success',
                              icon='check')
                self.logger.info('Images have been successfully downloaded!')

            # else block if the given link is failed or one of the status that is not 'OK'
            else:
                CTkMessagebox(
                    message="Download Failed (Status Code: {} {})".format(status, HTTPStatus(status).phrase),
                    title='Failed',
                    icon='cancel')

    def verify_link(self, url: str) -> str | None:
        """
        check and verify the link if it has https
        :param url: The Url of the image the user wants to download
        :return:
        """
        link: list[str] = url.split(':')

        if 'https' in link or 'http' in link:
            return url

        else:
            CTkMessagebox(message="Invalid, Please double check your URL", title='URL Error',
                          icon='cancel')
            self.logger.debug('Unable to connect to the given URL, PLease double check your url')
            return   # stop the code in continuing

    def get_extension(self, url: str):
        """
        Get and verify file extension from the given link
        :param url: The link/URL of the image that user wants to download
        :return ext: The file extension
        """
        for ext in self.extensions:
            if ext in url:
                return ext