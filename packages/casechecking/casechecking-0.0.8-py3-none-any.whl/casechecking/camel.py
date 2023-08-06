from .casechecking import casechecking
from .boundaries import OnDelimeterUppercaseNext, OnUpperPrecededByLowerAppendUpper


class Camel(casechecking):
    def define_boundaries(self):
        self.add_boundary_handler(OnDelimeterUppercaseNext(self.delimiters()))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper())

    def prepare_string(self, s):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


def lowitcase(s, **kwargs):
    """Convert a string to camel case.

    Example

      Hello World => helloWorld

    """
    return Camel(s, **kwargs).convert()
