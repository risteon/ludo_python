import random
from common_definitions import MAX_DICE_NUMBER_OF_POINTS


class Die:
    """Simulate a 6-sided die."""
    def roll( self ):
        self.value = random.randint(1, MAX_DICE_NUMBER_OF_POINTS)
        return self.value

    def getValue( self ):
        return self.value
