### Board

# enum
from enum import Enum, unique

@unique
class FieldType(Enum):
    simple = 0
    safe = 1
    finish = 2

class Player:

    def __init__( self, number ):
       self.number = number
       print("New player: ", number)

    def getNumber( self ):
        return self.number

class BoardField:

    def __init__( self ):
        self.field_type = FieldType.simple
        self.pawn = 0

    def getFieldType( self ):
        return self.field_type

class Board:
    def __init__( self ):
        print("yay")
        self.field = [[BoardField() for j in range(10)] for i in range(4)]
        self.finish = [[BoardField() for j in range(4)] for i in range(4)]

    def printBoard( self ):
#        print("Raw data: ")
#        for x in self.field:
#            print(x)
        print("bb  XXX  bb")
        print("bb  XBX  bb")
        print("    XBX    ")
        print("    XBX    ")
        print("XXXXXBXXXXX")
        print("XRRRR GGGGX")
        print("XXXXXYXXXXX")
        print("    XYX    ")
        print("    XYX    ")
        print("yy  XYX  gg")
        print("yy  XXX  gg")


    def movePawn( self ):
        print("blubb")
