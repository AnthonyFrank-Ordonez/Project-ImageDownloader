import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from fake_useragent import UserAgent
from img_validation_and_processing import ImageValidationAndProcessing
import logging


class ImageDownloader(ImageValidationAndProcessing):
    def __init__(self, header: dict, invalid_type: tuple, log):
        super().__init__(header, invalid_type, log)
        self.window = ctk.CTk()
        self.window.geometry('420x280')
        self.window.title('Image Downloader')
        self.window.resizable(False, False)

        # Set up all the labels, Entry, and Buttons
        self.url_label = ctk.CTkLabel(self.window, text='URL: ', font=('Calibri Bold', 15))
        self.url_entry = ctk.CTkEntry(self.window, placeholder_text='URL', width=250)

        self.fileName_label = ctk.CTkLabel(self.window, text='FIle Name: ', font=('Calibri Bold', 15))
        self.fileName_entry = ctk.CTkEntry(self.window, placeholder_text='File Name', width=250)

        self.folderPath_label = ctk.CTkLabel(self.window, text='Folder Path: ', font=('Calibri Bold', 15))
        self.folderPath_entry = ctk.CTkEntry(self.window, placeholder_text='Folder Path', width=250)

        self.download_btn = ctk.CTkButton(self.window, text='DOWNLOAD', width=250, height=40, command=self.check_inputs)
        self.clear_btn = ctk.CTkButton(self.window, text='CLEAR', width=250, height=40)

        # Set up the grid
        self.url_label.grid(row=0, column=0, padx=25, pady=20, sticky='se')
        self.url_entry.grid(row=0, column=1)
        self.fileName_label.grid(row=1, column=0, padx=25, sticky='se')
        self.fileName_entry.grid(row=1, column=1)
        self.folderPath_label.grid(row=2, column=0, padx=25, pady=20)
        self.folderPath_entry.grid(row=2, column=1)
        self.download_btn.grid(row=3, column=1)
        self.clear_btn.grid(row=4, column=1, pady=15)

    def check_inputs(self):
        """Check if there are any missing inputs from the entry"""

        # input values obtain from the user input from the entries
        input_URL: str = self.url_entry.get()
        input_Name: str = self.fileName_entry.get()
        input_Path: str = self.folderPath_entry.get()

        # Check if there are any missing inputs from entries
        if not input_URL or not input_Name or not input_Path:
            CTkMessagebox(message="Invalid, Please double check your input and try again.", title='Input Error',
                          icon='cancel')
            self.logger.debug('Input Error: There are missing input from the entries')

        else:
            self.download_img(url=input_URL, name=input_Name, folder_path=input_Path)

    def run_app(self):
        """Run the application"""
        self.window.mainloop()


def main():
    logging.basicConfig(filename='Your Path', level=logging.DEBUG,
                        encoding='utf-8',
                        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d: %I:%M %p')
    header: dict = {'user_agent': str(UserAgent.firefox)}
    invalid_type: tuple = ("", " ")
    logger = logging.getLogger(__name__)

    # Disable 3rd party module loggers
    logging.getLogger('requests').setLevel(logging.INFO)
    logging.getLogger('PIL').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)

    # Create the Object and start the app
    Image_Downloader = ImageDownloader(header, invalid_type, logger)
    Image_Downloader.run_app()


if __name__ == '__main__':
    main()