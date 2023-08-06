import requests
from liveramp_automation.utils.allure import *
from liveramp_automation.utils.log import Logger


# These are 7 types of methods to call the APIs.Each API allows to multiple parameters.
# We also added some log/report_content while calling the APIs which would be helpful to check the errors.

def request_post(url, headers, data=None, json=None, **kwargs):
    """Sends a POST request.

    :param url: URL for the new :class:`Request` object.
    :param headers:
    :param data:
    :param json:
    :param kwargs:
    :return:
    """
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is POST")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is POST", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
        allure_attach_text(data, "The request data infomation is as the following.")
    if json:
        Logger.info("The json in request body is {}".format(json))
        allure_attach_json("The json in request body is:", json)
    try:
        response = requests.post(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("The response infomation is {}".format(response.text))
        allure_attach_text(response.text, "The response infomation is as the following.")
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_get(url, headers, data=None, json=None, **kwargs):
    """Sends a get request.

    :param url:
    :param headers:
    :param data:
    :param json:
    :param kwargs:
    :return:
    """
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is GET")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is GET", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        allure_attach_json("The json in request body is:", json)
    try:
        response = requests.get(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_options(url, headers, **kwargs):
    """Sends an OPTIONS request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    :param headers:
    :param kwargs:
    :return:
    """

    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is OPTIONS")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is OPTIONS", "Method")
    try:
        response = requests.options(url=url, headers=headers, **kwargs)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_delete(url, headers, data=None, json=None, **kwargs):
    """Sends a DELETE request.

    :param url:
    :param headers:
    :param data:
    :param json:
    :param kwargs:
    :return:
    """
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is DELETE")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is DELETE", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.delete(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_head(url, headers, data=None, json=None, **kwargs):
    """Sends a HEAD request.

    :param url:
    :param headers:
    :param data:
    :param json:
    :param kwargs:
    :return:
    """
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is HEAD")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is HEAD", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.head(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_put(url, headers, data=None, json=None, **kwargs):
    """Sends a PUT request.

    :param url:
    :param headers:
    :param data:
    :param json:
    :param kwargs:
    :return:
    """
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is PUT")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is PUT", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.put(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_patch(url, headers, data=None, json=None, **kwargs):
    """Sends a PATCH request.

    :param url:
    :param headers:
    :param data:
    :param json:
    :param kwargs:
    :return:
    """
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is PATCH")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is PATCH", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.patch(url=url, data=data, json=json, headers=headers, **kwargs)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response
