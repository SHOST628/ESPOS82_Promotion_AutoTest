from unittest import TestCase


class Assertions(TestCase):
    # def assertAlmostEqual(self, first, second, places=None, msg=None,
    #                       delta=None):
    #     """Fail if the two objects are unequal as determined by their
    #        difference rounded to the given number of decimal places
    #        (default 7) and comparing to zero, or by comparing that the
    #        difference between the two objects is more than the given
    #        delta.
    #
    #        Note that decimal places (from zero) are usually not the same
    #        as significant digits (measured from the most significant digit).
    #
    #        If the two objects compare equal then they will automatically
    #        compare almost equal.
    #     """
    #     if first == second:
    #         # shortcut
    #         return
    #     if delta is not None and places is not None:
    #         raise TypeError("specify delta or places not both")
    #
    #     diff = abs(first - second)
    #     if delta is not None:
    #         if diff <= delta:
    #             return
    #
    #         standardMsg = '%s != %s within %s delta (%s difference)' % (
    #             safe_repr(first),
    #             safe_repr(second),
    #             safe_repr(delta),
    #             safe_repr(diff))
    #     else:
    #         if places is None:
    #             places = 7
    #
    #         if round(diff, places) == 0:
    #             return
    #
    #         standardMsg = '%s != %s within %r places (%s difference)' % (
    #             safe_repr(first),
    #             safe_repr(second),
    #             places,
    #             safe_repr(diff))
    #     msg = self._formatMessage(msg, standardMsg)
    #     raise self.failureException(msg)
    pass