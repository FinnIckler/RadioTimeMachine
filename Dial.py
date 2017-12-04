# -----------------------------------------------------------------------------
# Dial widget that shows a turnable knob for setting an angle.
#
import math
import tkinter


# -----------------------------------------------------------------------------
# Radius is in any Tk-acceptable format.
# Command callback takes an angle argument (degrees).
#


class Dial:
    def __init__(self, parent, radius='.5i', command=None, init_angle=0.0, zero_axis='x', rot_dir='counterclockwise',
                 fill=None, outline='black', line='black', disp_type='month'):
        self.command = command
        self.radius = parent.winfo_pixels(radius)
        self.bump_size = .2 * self.radius
        rpb = self.radius + self.bump_size + 10
        self.center_xy = (rpb, rpb)
        self.drag_from_angle = None

        s = int(2 * (self.radius + self.bump_size))
        c = tkinter.Canvas(parent, width=150, height=150)
        c.bind('<ButtonPress-1>', self.button_press_cb)
        c.bind('<Button1-Motion>', self.pointer_drag_cb)
        c.bind('<ButtonRelease-1>', self.button_release_cb)
        cx, cy = self.center_xy
        r = self.radius
        kw = {}
        if fill is not None:
            kw['fill'] = fill
        if outline is not None:
            kw['outline'] = outline
        c.create_oval(cx - r , cy - r, cx + r , cy + r, **kw)
        bs = self.bump_size
        kw = {'width': bs}
        if line is not None:
            kw['fill'] = line
        id_ = c.create_line(cx, cy, cx + r + bs, cy, **kw)
        self.line_id = id_
        self.canvas = c
        self.widget = c
        self.rotDir = rot_dir
        self.zeroAxis = zero_axis
        self.angle = init_angle
        self.setAngle(init_angle, do_callback=0)

        if disp_type == 'month':
            c.create_text(75, 14, text="Dec", tag="Big")
            c.create_text(105, 22, text="Jan", tag="Small")
            c.create_text(127, 41, text="Feb", tag="Small")
            c.create_text(140, 72, text="Mar", tag="Big")
            c.create_text(131, 100, text="Apr", tag="Small")
            c.create_text(105, 127, text="May", tag="Small")
            c.create_text(75, 138, text="Jun", tag="Big")
            c.create_text(45, 127, text="Jul", tag="Small")
            c.create_text(19, 100, text="Aug", tag="Small")
            c.create_text(15, 72, text="Sep", tag="Big")
            c.create_text(20, 41, text="Oct", tag="Small")
            c.create_text(45, 22, text="Nov", tag="Small")
            c.itemconfig(tagOrId="Big", font=("Fjord One", 12))
            c.itemconfig(tagOrId="Small", font=("Fjord One", 8))
        else:
            c.create_text(75, 14, text="1920", tag="Big")
            c.create_text(105, 22, text="1928", tag="Small")
            c.create_text(127, 41, text="1936", tag="Small")
            c.create_text(140, 72, text="1946", tag="Big")
            c.create_text(131, 100, text="1954", tag="Small")
            c.create_text(105, 127, text="1962", tag="Small")
            c.create_text(75, 138, text="1970", tag="Big")
            c.create_text(45, 127, text="1978", tag="Small")
            c.create_text(19, 100, text="1986", tag="Small")
            c.create_text(15, 72, text="1994", tag="Big")
            c.create_text(20, 41, text="2002", tag="Small")
            c.create_text(45, 22, text="2010", tag="Small")
            c.itemconfig(tagOrId="Big", font=("Fjord One", 12))
            c.itemconfig(tagOrId="Small", font=("Fjord One", 8))

    # ---------------------------------------------------------------------------
    #
    def button_press_cb(self, event):

        try:
            self.drag_from_angle = self.event_angle(event)
        except ValueError:
            pass

    # ---------------------------------------------------------------------------
    #
    def pointer_drag_cb(self, event):

        if self.drag_from_angle is None:
            return

        try:
            a = self.event_angle(event)
        except ValueError:
            pass
        else:
            self.drag_from_angle = a
            self.set_angle(a)

    # ---------------------------------------------------------------------------
    #
    def button_release_cb(self, event):

        if self.drag_from_angle is None:
            return

        try:
            a = self.event_angle(event)
        except ValueError:
            pass
        else:
            self.drag_from_angle = None
            self.set_angle(a)

    # ---------------------------------------------------------------------------
    #
    def event_angle(self, event):
        # math.atan2 may raise ValueError if dx and dy are zero.
        (x, y) = canvas_coordinates(self.canvas, event)
        (dx, dy) = (x - self.center_xy[0], self.center_xy[1] - y)
        rad = math.atan2(dy, dx)
        deg = 180 * rad / math.pi
        if self.zeroAxis == 'y':
            deg = deg + 270
        elif self.zeroAxis == '-x':
            deg = deg + 180
        elif self.zeroAxis == '-y':
            deg = deg + 90

        if self.rotDir == 'clockwise':
            deg = 360 - deg

        while deg > 180.0:
            deg = deg - 360
        while deg <= -180.0:
            deg = deg + 360
        return deg

    # ---------------------------------------------------------------------------
    #
    def set_angle(self, a, do_callback=1):

        #
        # Move dial pointer
        #
        cx, cy = self.center_xy
        d = self.radius + self.bump_size
        cartesian = a
        if self.rotDir == 'clockwise':
            cartesian = 360 - cartesian
        if self.zeroAxis == 'y':
            cartesian = cartesian + 90
        elif self.zeroAxis == '-x':
            cartesian = cartesian + 180
        elif self.zeroAxis == '-y':
            cartesian = cartesian + 270
        while cartesian > 180.0:
            cartesian = cartesian - 360
        while cartesian <= -180.0:
            cartesian = cartesian + 360
        rad = math.pi * cartesian / 180.0
        ox = d * math.cos(rad)
        oy = d * math.sin(rad)
        self.canvas.coords(self.line_id, cx, cy, cx + ox, cy - oy)
        self.angle = a
        #
        # Call callback
        #
        if do_callback:
            self.command(a)

    setAngle = set_angle

# -----------------------------------------------------------------------------
#
def canvas_coordinates(canvas, event):
    return canvas.canvasx(event.x), canvas.canvasy(event.y)
