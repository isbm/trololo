"""
Test lalala library.
"""

from trololo.lalala import TrololoObject


class TestLalalaLib(object):
    """
    Test lalala library objects.
    """
    def test_trololo_object_loaded(self):
        """
        Test if TrololoObject loader handles data as per expectations.
        :return:
        """

        struct = {
            "number": 123,
            "some_float": .01,
            "inner": {
                "name": "Fred",
                "hidden": {
                    "array": [1, 2, 3]
                }
            }
        }

        obj = TrololoObject.load(None, struct)
        assert obj.number == 123
        assert obj.some_float == .01
        assert obj.inner.hidden.array[1] == 2
