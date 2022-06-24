import logging
import os
import time
import requests
import magic
from tqdm import tqdm
from urllib.parse import quote
from urllib.request import urlopen, Request


class ImageDownloader:
    """
    Addapted code from
    https://github.com/RiddlerQ/simple_image_download/blob/master/simple_image_download/simple_image_download.py
    """
    __logger = logging.getLogger(__name__)
    extensions = {'.jpg', '.png', '.jpeg'}

    def __init__(self):
        pass

    def download(self, keywords, limit, extensions=None, save_dir='images'):
        extensions = ImageDownloader.extensions if extensions is None else extensions
        keyword_to_search = [str(item).strip() for item in keywords.split(',')]
        self.__logger.debug(f'Keywords to search: {str(keyword_to_search)}')
        i = 0

        things = len(keyword_to_search) * limit

        pbar = tqdm(total=things)
        while i < len(keyword_to_search):
            self._create_directories(save_dir, keyword_to_search[i])
            url = 'https://www.google.com/search?q=' + quote(
                keyword_to_search[i].encode(
                    'utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770' \
                                '&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ '
            raw_html = self._download_page(url)

            end_object = -1
            google_image_seen = False
            j = 0
            object_raw = None
            while j < limit:
                max_iters = 1000
                while True:
                    try:
                        max_iters -= 1
                        if max_iters < 1:
                            raise Exception(f'max iters reached')
                        new_line = raw_html.find('"https://', end_object + 1)
                        end_object = raw_html.find('"', new_line + 1)

                        buffor = raw_html.find('\\', new_line + 1, end_object)
                        if buffor != -1:
                            object_raw = (raw_html[new_line + 1:buffor])
                        else:
                            object_raw = (raw_html[new_line + 1:end_object])

                        if any(extension in object_raw for extension in extensions):
                            if 'light_thumbnail2.png' in object_raw or 'device_default_thumbnail2.png' in object_raw \
                                    or 'dark_thumbnail2.png' in object_raw:
                                pass
                            else:
                                break
                    except Exception as e:
                        self.__logger.warning(f'Error occurered: {e}')
                        break
                path = os.path.join(save_dir, keyword_to_search[i].replace(" ", "_"))

                try:
                    r = requests.get(object_raw, allow_redirects=True, timeout=1)
                    if 'html' not in str(r.content):
                        mime = magic.Magic(mime=True)
                        file_type = mime.from_buffer(r.content)
                        file_extension = f'.{file_type.split("/")[1]}'
                        if file_extension not in extensions:
                            raise ValueError('File not in extensions')
                        if file_extension == '.png' and not google_image_seen:
                            google_image_seen = True
                            raise ValueError('??')
                        file_name = str(keyword_to_search[i]) + "_" + str(j + 1) + file_extension
                        with open(os.path.join(path, file_name), 'wb') as file:
                            file.write(r.content)
                        j += 1
                        pbar.update(1)
                except Exception as e:
                    self.__logger.warning(f'Error occurered: {e}')

            i += 1

    @staticmethod
    def _create_directories(main_directory, name):
        name = name.replace(" ", "_")
        try:
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)
                time.sleep(0.2)
                path = name
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
            else:
                path = name
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)

        except OSError as e:
            if e.errno != 17:
                raise
            pass
        return

    @staticmethod
    def _download_page(url):

        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/77.0.3865.90 Safari/537.36"}
            req = Request(url, headers=headers)
            resp = urlopen(req)
            resp_data = str(resp.read())
            return resp_data

        except Exception as e:
            print(e)
            exit(0)
            import os
