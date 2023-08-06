import allure


def allure_page_screenshot(page, name):
    """
    Call allure_page_screenshot to show the screenshot while using Playright
    :param page:
    :param name:
    :return:
    """
    allure.attach(page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)


#
def allure_drive_screenshot(driver, name):
    """
    Call allure_drive_screenshot to show the screenshot while using Selenium
    :param page:
    :param name:
    :return:
    """
    allure.attach(driver.save_screenshot(), name=name, attachment_type=allure.attachment_type.PNG)


def allure_attach_video(path, video_name):
    """
    Call allure_drive_screenshot to show the screenshot while using Selenium
    :param page:
    :param name:
    :return:
    """
    allure.attach.file(path, name=video_name, attachment_type=allure.attachment_type.MP4)


def allure_attach_text(content, description):
    """
    Call allure_attach_text to show the content in text format.
    :param page:
    :param name:
    :return:
    """
    allure.attach(content, description, attachment_type=allure.attachment_type.TEXT)


def allure_attach_json(content, description):
    """
    Call allure_attach_json to show the content in json format.
    :param page:
    :param name:
    :return:
    """
    allure.attach(content, description, attachment_type=allure.attachment_type.JSON)
