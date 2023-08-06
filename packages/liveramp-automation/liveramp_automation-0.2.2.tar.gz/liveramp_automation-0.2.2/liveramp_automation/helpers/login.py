import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from liveramp_automation.utils.log import Logger
from liveramp_automation.utils.time import fixed_wait


class LoginHepler:

    @staticmethod
    def liveramp_okta_login_page(page, config, username, password):
        """
        This function, "liveramp_okta_login_page," facilitates Okta login using Playwright.
        Both the username and password are mandatory.
        Please invoke this API with the username and password provided in os.environ[].
        :param page:
        :param config:
        :param username:
        :param password:
        :return:
        """
        Logger.info("Going to login to OKTA...")
        url = config['login_url']
        Logger.info("The login url is {}".format(url))
        page.goto(url)
        fixed_wait()
        url_new = page.url
        Logger.info("The current url is {}.".format(url_new))
        if url_new.__contains__(url):
            Logger.info("Login to OKTA succefully.")
        else:
            page.fill('#idp-discovery-username', username)
            page.get_by_role("button", name="Next").click()
            page.get_by_role("textbox", name="Password").fill(password)
            page.get_by_role("button", name="Sign In").click()
            Logger.info("We could login to OKTA successfully.")
            # wait for the login process to complete
            fixed_wait(20)

    #
    @staticmethod
    def liveramp_okta_login_driver(driver, config, username, password):
        """
         "liveramp_okta_login_driver," is to facilitate Okta login using Selenium.
         Both the username and password are mandatory.
         Please utilize this API by providing the username and password from os.environ[].
        :param driver:
        :param config:
        :param username:
        :param password:
        :return:
        """
        Logger.info("Going to login to OKTA...")
        url = config['login_url']
        Logger.info("The login url is {}.".format(url))
        driver.get(url)
        fixed_wait()
        if driver.current_url.__contains__(url):
            Logger.info("Login to OKTA succefully.")
        else:
            username_box = driver.find_element(by=By.ID, value='idp-discovery-username')
            username_box.send_keys(username)
            username_box.send_keys(Keys.ENTER)
            fixed_wait()
            password_box = driver.find_element(by=By.ID, value='okta-signin-password')
            password_box.send_keys(password)
            submit_button = driver.find_element(by=By.ID, value='okta-signin-submit')
            submit_button.click()
            Logger.info("We could login to OKTA successfully.")
            fixed_wait(10)

    #
    @staticmethod
    def call_oauth2_get_token(username, password) -> str:
        """
        The purpose of the method `call_oauth2_get_token` is to initiate an OAuth2 login.
        Both the API username and password (sensitive) are mandatory for this process.
        Please ensure that you provide the required username and password from os.environ[] when calling this API.
        :param username:
        :param password:
        :return:
        """
        data = {
            "grant_type": "password",
            "scope": "openid",
            "client_id": "liveramp-api"
        }
        Logger.info("The default params are the {}".format(data))
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data.update(username=username)
        data.update(password=password)
        response = requests.post(
            "https://serviceaccounts.liveramp.com/authn/v1/oauth2/token", data=data, headers=headers)
        assert 200 == response.status_code
        access_token = response.json()['access_token']
        token_type = response.json()['token_type']
        return "{} {}".format(token_type, access_token)
