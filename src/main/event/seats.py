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
        if (seat not in self.seatStates or self.seatStates[seat] == STATE.FREE):
            self.seatStates[seat] = STATE.RESERVED
            return True
        return False

    def buy(self, seat):
        if (seat in self.seatStates and self.seatStates[seat] == STATE.RESERVED):
            self.seatStates[seat] = STATE.SOLD
            return True
        return False

    def query(self, seat):
        if (seat not in self.seatStates):
            return STATE.FREE.name
        return self.seatStates[seat].name
