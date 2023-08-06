import configparser
import json
import os

import yaml
from liveramp_automation.utils.log import Logger


class FileHelper:

    @staticmethod
    def read_json_report(path) -> dict:
        """Read all the content of the json file

        :param path:
        :return:
        """
        with open(path, 'r') as file:
            json_string = file.read()
            data = json.loads(json_string)
        return data

    @staticmethod
    def read_init_file(file_path, file_name, file_mode="r") -> dict:
        """Read all the content of the init file

        :param file_path:
        :param file_name:
        :param file_mode:
        :return: data_dict
        """
        try:
            full_path = os.path.join(file_path, file_name)
            with open(full_path, mode=file_mode) as file:
                data_dict = {}
                current_module = None
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("[") and line.endswith("]"):
                        current_module = line[1:-1].strip()
                        data_dict[current_module] = {}
                    else:
                        if "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()
                            if current_module:
                                data_dict[current_module][key] = value
            return data_dict
        except FileNotFoundError:
            Logger.error(f"File '{file_name}' not found in the specified path: '{file_path}'.")
            return None
        except PermissionError:
            Logger.error(f"Permission denied to read the file '{file_name}' in the specified path: '{file_path}'.")
            return None
        except Exception as e:
            Logger.error(f"An error occurred while reading the file: {e}")
            return None

    @staticmethod
    def load_env_yaml(path, file_prefix, env):
        """read the resources accroding to different envrionments

        :param path:
        :param file_prefix:
        :param env:
        :return:
        """
        file_name = path + "/" + file_prefix + ".{env}.yaml".format(env)
        with open(file_name) as f:
            return yaml.safe_load(f)

    @staticmethod
    def deal_testcase_json(file_path):
        """ read the report.json file and return the testcase object

        :param file_path:
        :return:
        """
        with open(file_path, "r") as file:
            item = json.load(file)
        nodeid = item["nodeid"]
        outcome = item["outcome"]
        groupName = nodeid.split("/")[1]
        testcase = {}
        testcase["groupName"] = groupName
        testcase["className"] = nodeid.split("/")[2].split("::")[0]
        testcase["caseName"] = nodeid.split("/")[-1].split("::")[-1]
        if outcome.upper() == "failed".upper():
            flag = 0
            errorMessage = str(item["call"]["crash"])
        else:
            flag = 1
            errorMessage = None
        testcase["flag"] = flag
        testcase["errorMessage"] = errorMessage
        testcase["duration"] = float(item["call"]["duration"])
        return testcase

    @staticmethod
    def read_junit_xml_report(path):
        """ read the junit.xml and retrun the result_dict

        :param path:
        :return:
        """
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()
        test_cases = int(root.attrib.get('tests', 0))
        failures = int(root.attrib.get('failures', 0))
        errors = int(root.attrib.get('errors', 0))
        skipped = int(root.attrib.get('skipped', 0))
        result_dict = {
            "Cases": test_cases,
            "Failures": failures,
            "Errors": errors,
            "Skipped": skipped
        }
        return result_dict
