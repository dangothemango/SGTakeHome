import unittest

from main.event.seats import *

#these operations are very so going to test them all more or less at the same time
class TestSeatsSimple(unittest.TestCase):
    def setUp(self):
        self.sr = SeatReservations("test_event_simple")

    def test_queryReturnsFreeForArbitrarySeats(self):
        r,d = self.sr.query("B1")
        self.assertEqual(d, STATE.FREE.name)
        r,d = self.sr.query("A1")
        self.assertEqual(d, STATE.FREE.name)
        r,d = self.sr.query("C2")
        self.assertEqual(d, STATE.FREE.name)
        r,d = self.sr.query("B1")
        self.assertEqual(d, STATE.FREE.name)
        r,d = self.sr.query("A1")
        self.assertEqual(d, STATE.FREE.name)
        r,d = self.sr.query("C2")
        self.assertEqual(d, STATE.FREE.name)

    def test_reserveReturnsTrueForArbitrarySeats_thenbuyingworks(self):
        r,d = self.sr.buy("B1")
        self.assertFalse(r)
        r,d = self.sr.buy("A1")
        self.assertFalse(r)
        r,d = self.sr.buy("C2")
        self.assertFalse(r)

        r,d = self.sr.reserve("B1")
        self.assertTrue(r)
        r,d = self.sr.reserve("A1")
        self.assertTrue(r)
        r,d = self.sr.reserve("C2")
        self.assertTrue(r)

        r,d = self.sr.buy("B1")
        self.assertTrue(r)
        r,d = self.sr.buy("A1")
        self.assertTrue(r)
        r,d = self.sr.buy("C2")
        self.assertTrue(r)

class TestSeatsComplex(unittest.TestCase):
    def setUp(self):
        self.sr = SeatReservations("test_event_complex")

    def test_buyReturnsFalseForArbitrarySeats(self):
        r,d = self.sr.buy("B1")
        self.assertFalse(r)
        r,d = self.sr.buy("A1")
        self.assertFalse(r)
        r,d = self.sr.buy("C2")
        self.assertFalse(r)

    def test_doubledActionsReturnFalse_queryUpdatesBasedOnOtherActions(self):
        r,d = self.sr.reserve("B1")
        self.assertTrue(r)
        r,d = self.sr.query("B1")
        self.assertEqual(d, STATE.RESERVED.name)

        r,d = self.sr.reserve("B1")
        self.assertFalse(r)
        r,d = self.sr.query("B1")
        self.assertEqual(d, STATE.RESERVED.name)

        r,d = self.sr.buy("B1")
        self.assertTrue(r)
        r,d = self.sr.query("B1")
        self.assertEqual(d, STATE.SOLD.name)

        r,d = self.sr.buy("B1")
        self.assertFalse(r)
        r,d = self.sr.query("B1")
        self.assertEqual(d, STATE.SOLD.name)

if __name__ == '__main__':
    unittest.main()
