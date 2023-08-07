from tkinter import Tk, StringVar, Label, OptionMenu, Entry, Button
from ..components import Capacitor, Inductor


class CptDialog:

    def __init__(self, cpt, update=None):

        self.cpt = cpt
        self.update = update

        self.window = Tk()
        self.window.title(cpt.name)

        row = 0

        self.kind_var = None
        if cpt.kind is not None:
            self.kind_var = StringVar(self.window)
            self.kind_var.set(cpt.kind)

            kind_label = Label(self.window, text='Kind: ')
            kind_option = OptionMenu(self.window, self.kind_var,
                                     *cpt.kinds.keys())

            kind_label.grid(row=row)
            kind_option.grid(row=row, column=1)
            row += 1

        self.name_var = StringVar(self.window)
        self.name_var.set(cpt.name)

        name_label = Label(self.window, text='Name: ')
        name_entry = Entry(self.window, textvariable=self.name_var,
                           command=self.on_update)

        name_label.grid(row=row)
        name_entry.grid(row=row, column=1)
        row += 1

        self.value_var = StringVar(self.window)
        value = cpt.value
        if value is None:
            value = cpt.name
        self.value_var.set(value)

        value_label = Label(self.window, text='Value: ')
        value_entry = Entry(self.window, textvariable=self.value_var,
                            command=self.on_update)

        value_label.grid(row=row)
        value_entry.grid(row=row, column=1)
        row += 1

        self.initial_value_var = None
        if isinstance(cpt, (Capacitor, Inductor)):

            ivlabel = 'v0'
            if isinstance(cpt, Inductor):
                ivlabel = 'i0'

            self.initial_value_var = StringVar(self.window)

            initial_value_label = Label(self.window, text=ivlabel + ': ')
            initial_value_entry = Entry(
                self.window, textvariable=self.initial_value_var,
                command=self.on_update)
            initial_value_label.grid(row=row)
            initial_value_entry.grid(row=row, column=1)
            row += 1

        button = Button(self.window, text="OK", command=self.on_ok)
        button.grid(row=row)

    def on_update(self, arg=None):

        if self.kind_var is not None:
            kind = self.kind_var.get()
            if kind == '':
                kind = None
            self.cpt.kind = kind

        self.cpt.name = self.name_var.get()

        value = self.value_var.get()
        if value == '':
            value = None
        self.cpt.value = value

        if self.initial_value_var is not None:
            value = self.initial_value_var.get()
            if value == '':
                value = None
            self.cpt.initial_value = value

        if self.update:
            self.update(self.cpt)

    def on_ok(self):

        self.on_update()

        self.window.destroy()
