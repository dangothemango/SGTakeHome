import unittest

from main.event.seats import *

#these operations are very so going to test them all more or less at the same time
class TestSeatsSimple(unittest.TestCase):
    def setUp(self):
        self.sr = SeatReservations("test_event_simple")

    def test_queryReturnsFreeForArbitrarySeats(self):
        self.assertEqual(self.sr.query("B1"), STATE.FREE.name)
        self.assertEqual(self.sr.query("A1"), STATE.FREE.name)
        self.assertEqual(self.sr.query("C2"), STATE.FREE.name)
        self.assertEqual(self.sr.query("B1"), STATE.FREE.name)
        self.assertEqual(self.sr.query("A1"), STATE.FREE.name)
        self.assertEqual(self.sr.query("C2"), STATE.FREE.name)

    def test_reserveReturnsTrueForArbitrarySeats_thenbuyingworks(self):
        self.assertFalse(self.sr.buy("B1"))
        self.assertFalse(self.sr.buy("A1"))
        self.assertFalse(self.sr.buy("C2"))

        self.assertTrue(self.sr.reserve("B1"))
        self.assertTrue(self.sr.reserve("A1"))
        self.assertTrue(self.sr.reserve("C2"))

        self.assertTrue(self.sr.buy("B1"))
        self.assertTrue(self.sr.buy("A1"))
        self.assertTrue(self.sr.buy("C2"))

class TestSeatsComplex(unittest.TestCase):
    def setUp(self):
        self.sr = SeatReservations("test_event_complex")

    def test_buyReturnsFalseForArbitrarySeats(self):
        self.assertFalse(self.sr.buy("B1"))
        self.assertFalse(self.sr.buy("A1"))
        self.assertFalse(self.sr.buy("C2"))

    def test_doubledActionsReturnFalse_queryUpdatesBasedOnOtherActions(self):
        self.assertTrue(self.sr.reserve("B1"))
        self.assertEqual(self.sr.query("B1"), STATE.RESERVED.name)

        self.assertFalse(self.sr.reserve("B1"))
        self.assertEqual(self.sr.query("B1"), STATE.RESERVED.name)

        self.assertTrue(self.sr.buy("B1"))
        self.assertEqual(self.sr.query("B1"), STATE.SOLD.name)

        self.assertFalse(self.sr.buy("B1"))
        self.assertEqual(self.sr.query("B1"), STATE.SOLD.name)

if __name__ == '__main__':
    unittest.main()
