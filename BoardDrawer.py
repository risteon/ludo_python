from tkinter import *

class BoardDrawer:

    # DIMENSIONS
    grid_pixel_size = 50
    grid_margin_pixel = 5
    grid_size = 11
    canvas_width = grid_pixel_size*grid_size
    canvas_height = grid_pixel_size*grid_size
    
    def __init__( self ):
        """ Create canvas
        """
        self.master = Tk()
        self.canvas = Canvas(self.master,
                             width = BoardDrawer.canvas_width,
                             height = BoardDrawer.canvas_height)

        self.canvas.pack()

        #y = int(BoardDrawer.canvas_height / 2)
        #self.canvas.create_line(0, y, BoardDrawer.canvas_width, y, fill="#FFEC8B")

        self.drawBoard()

    def drawBoard( self ):
        for field_number in range(40):
            coord = self.getFieldCoordinates(field_number)
            pixel_lower = self.getGridPixel(coord)
            self.canvas.create_oval(pixel_lower[0], pixel_lower[1], pixel_lower[0] + 40, pixel_lower[1] + 40)

    def showBoard( self ):
        mainloop()

    def getFieldCoordinates( self, field_number ):

        # Check Range
        assert field_number >= 0 and field_number < 40, "field_number out of range (0-39)"

        if field_number < 5:
            return (4, field_number)
        elif field_number < 9:
            return (8-field_number, 4)
        elif field_number == 9:
            return (0, 5)
        elif field_number < 15:
            return (field_number - 10, 6)
        elif field_number < 19:
            return (4, field_number - 8)
        elif field_number == 19:
            return (5, 10)
        elif field_number < 25:
            return (6, 30-field_number)
        elif field_number < 29:
            return (field_number-18, 6)
        elif field_number == 29:
            return (10, 5)
        elif field_number < 35:
            return (40-field_number, 4)
        elif field_number < 39:
            return (6, 38-field_number)
        
        return (5, 0)

    def getGridPixel( self, coordinates ):

        return (coordinates[0]*BoardDrawer.grid_pixel_size + BoardDrawer.grid_margin_pixel,
                coordinates[1]*BoardDrawer.grid_pixel_size + BoardDrawer.grid_margin_pixel)

