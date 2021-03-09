import enum

class STATE(enum.Enum):
    FREE = 1
    RESERVED = 2
    SOLD = 3

class SeatReservations:

    def __init__(self, eventName):
        self.seatStates = dict()
        self.eventName = eventName

    def reserve(self, seat):
        # A free seat should never be in self.seatStates but the or is in there just in case implementation changes
        r = False
        if (seat not in self.seatStates or self.seatStates[seat] == STATE.FREE):
            self.seatStates[seat] = STATE.RESERVED
            r = True
        return r, None

    def buy(self, seat):
        r = False
        if (seat in self.seatStates and self.seatStates[seat] == STATE.RESERVED):
            self.seatStates[seat] = STATE.SOLD
            r = True
        return r, None

    def query(self, seat):
        if (seat not in self.seatStates):
            return True, STATE.FREE.name
        return True, self.seatStates[seat].name
