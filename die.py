import random


class Die:
    """Simulate a 6-sided die."""
    def roll( self ):
        self.value = random.randint(1,6)
        return self.value

    def getValue( self ):
        return self.value
