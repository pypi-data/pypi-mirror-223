import re
from .casechecking import casechecking
from .boundaries import OnDelimeterUppercaseNext, OnUpperPrecededByLowerAppendUpper


class Cobol(casechecking):

    JOIN_CHAR = "-"

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimeterUppercaseNext(self.delimiters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper(self.JOIN_CHAR))

    def convert(self):
        if self.raw().isupper():
            return re.sub(
                "[{}]+".format(re.escape(self.delimiters())),
                self.JOIN_CHAR,
                self.raw(),
            )

        return super(Cobol, self).convert()

    def mutate(self, c):
        return c.upper()


def upitcase(s, **kwargs):
    """Convert a string to cobol case

    Example

      Hello World => HELLO-WORLD

    """
    return Cobol(s, **kwargs).convert()
