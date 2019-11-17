from tkinter import *
from utils import *


class Tp:

    status = 'up'
    xy = []
    curve = Curva()
    intermediarios = []
    pixel_selected = None
    num_inter = 0
    draw_inter = 0

    # ========== Mouse Functions ==========
    def motion(self, event=None):
        if self.num_inter > 0 or self.status == 'up' or not self.pixel_selected:
            return
        self.drawing_area.delete(self.pixel_selected['point'])
        self.pixel_selected['point'] = self.draw_point(event.x, event.y)

    def left_click(self, event=None):
        if self.draw_inter > 0:
            self.xy.append({'x': event.x, 'y': event.y})
            self.intermediarios.append({
                                        'point': self.draw_point(event.x, event.y),
                                        'pos': self.num_inter - self.draw_inter
                                        })
            self.draw_inter -= 1
            if self.draw_inter == 0:
                curve = Curva()
                curve.intermediarios = self.intermediarios
                bpoints = bezier(500, self.xy)
                for i in bpoints:
                    curve.pixels.append(self.draw_pixel(i['x'], i['y']))
                self.curve = curve

        else:
            self.num_inter = 0
            x = event.x
            y = event.y
            enclosed = self.drawing_area.find_overlapping(x-1, y-1, x+2, y+2)
            if not enclosed:
                self.pixel_selected = None
            for i in enclosed:
                for j in self.curve.intermediarios:
                    if j['point'] == i:
                        self.pixel_selected = j
                        self.status = 'down'
                        break
                    else:
                        self.pixel_selected = None

    def left_release(self, event=None):
        self.status = 'up'
        if self.num_inter > 0 or not self.pixel_selected:
            return
        self.drawing_area.delete(self.pixel_selected['point'])
        for i in self.curve.pixels:
            self.drawing_area.delete(i)
        self.pixel_selected['point'] = self.draw_point(event.x, event.y)
        pos = self.pixel_selected['pos']
        self.xy.pop(pos)
        self.intermediarios.pop(pos)
        self.xy.insert(pos, {'x': event.x, 'y': event.y})
        self.intermediarios.insert(pos, self.pixel_selected)
        curve = Curva()
        curve.intermediarios = self.intermediarios
        bpoints = bezier(500, self.xy)
        for i in bpoints:
            curve.pixels.append(self.draw_pixel(i['x'], i['y']))
        self.curve = curve

    def right_click(self, event=None):
        self.num_inter = 0

    # ========== Get number of control points ==========
    def set_num_inter(self, event=None):
        self.num_inter = int(self.r.get())
        self.draw_inter = self.num_inter
        self.win.destroy()
        self.drawing_area.delete("all")
        self.xy = []
        self.curve = Curva()

    def show_popup(self):
        win = Toplevel()
        win.wm_title("Bezier")
        l = Label(win, text="Nº de pontos de controle: ", pady=15)
        r = Entry(win)
        b1 = Button(win, text="Ok", padx=15, command=self.set_num_inter)
        b2 = Button(win, text="Cancel", command=win.destroy)
        l.grid(row=0, column=0)
        r.grid(row=0, column=1)
        b1.grid(row=1, column=0)
        b2.grid(row=1, column=1)
        self.win = win
        self.r = r

    # ========== Draw control point ==========
    def draw_point(self, x=None, y=None):
        if None not in (x, y):
            return self.drawing_area.create_rectangle(x-5, y-5, x+4, y+4, fill="pink")

    # ========== Draw normal pixel ==========
    def draw_pixel(self, x=None, y=None):
        if None not in (x, y):
            return self.drawing_area.create_rectangle(x, y, x+2, y+2, fill="black")

    def __init__(self, master=None):
        self.root = master
        self.win = None
        self.r = None
        self.option_menu = Frame(self.root, padx=5, pady=5)
        self.option_menu.pack(side=LEFT)
        self.draw_curve_bt = Button(self.option_menu, text="Bezier", font=("Helvetica", 10),
                                    command=self.show_popup)
        self.draw_curve_bt.pack(fill="y")
        self.drawing_area = Canvas(self.root, width=1280, height=720, bg="#ffffff")
        self.drawing_area.pack(fill="both")
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.left_click)
        self.drawing_area.bind("<ButtonRelease-1>", self.left_release)
        self.drawing_area.bind("<ButtonPress-3>", self.right_click)


if __name__ == '__main__':
    master = Tk()
    master.title("Curvas Paralelas")
    app = Tp(master)
    master.mainloop()
