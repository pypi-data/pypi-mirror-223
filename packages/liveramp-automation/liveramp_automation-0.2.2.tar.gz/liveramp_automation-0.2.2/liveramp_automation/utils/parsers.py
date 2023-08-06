from pytest_bdd.parsers import StepParser
import parse as base_parse

EXTRA_TYPES = {}


class ParseUtils(StepParser):
    """
    parse step parser.
    This is a Factory method pattern to parse the steps in the BDD scenarios
    :param
    :type
    :return:
    :rtype:
    :raises
    """

    def __init__(self, name, *args):
        """
        Compile parse expression
        :param name:
        :param args:
        """
        super(ParseUtils, self).__init__(name)
        self.parser = base_parse.compile(self.name, *args, extra_types=EXTRA_TYPES)

    def parse_arguments(self, name: str):
        """
        Get step arguments.
        :param name:
        :return:
        """
        return self.parser.parse(name).named

    def is_matching(self, name):
        """
        Match given name with the step name
        :param name:
        :return:
        """
        try:
            return bool(self.parser.parse(name))
        except ValueError:
            return False
