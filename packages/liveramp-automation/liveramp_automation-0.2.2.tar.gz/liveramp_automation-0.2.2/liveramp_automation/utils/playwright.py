from urllib.parse import urlparse, urlunsplit

from liveramp_automation.helpers.file import FileHelper
from liveramp_automation.utils.time import MACROS


class PlaywrightUtils:

    def __int__(self, page):
        self.page = page

    def navigate_url(self, scheme=None, host_name=None, path=None, query=None):
        """ navigate_url

        :param scheme:
        :param host_name:
        :param path:
        :param query:
        :return:
        """
        parsed_uri = urlparse(self.page.url)
        self.page.goto(urlunsplit((parsed_uri.scheme if scheme is None else scheme,
                                   parsed_uri.hostname if host_name is None else host_name,
                                   parsed_uri.path if path is None else path,
                                   parsed_uri.query if query is None else query,
                                   '')))

    def savescreenshot(self, name):
        """ to save a screenshot to the destination

                :param name:
                :return:
                """
        data_dict = FileHelper.read_init_file(" /", "pytest.ini", "r")
        file_path = data_dict.get('screenshot', "reports/")
        name = file_path + "/{}_{}.png".format(MACROS["now"], name)
        self.page.screenshot(path=name)
