import random
import tkinter as tk
from tkinter.font import Font
import tkinter.messagebox as msg
import os
import sys

LEDEN = ['Jochem',
         'Bart',
         'Lisanne',
         'Thijs',
         'Anne DJ',
         'Chantal',
         'Djim',
         'Ella',
         'Floor',
         'Hilbrand',
         'Linde',
         'Thomas',
         'Fimke Anna',
         'Erik',
         'Ramon',
         'Dagmar',
         'Marco',
         'Danne',
         'Kars',
         'Anne L']


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class LatronesShuffelerWindow:
    def __init__(self, shuffler):
        self.window = shuffler

        self.group_size = 0
        self.doubters = 0

        self.present = []
        self.host = []

        self.groups = []

        self.present_vars = []
        self.host_vars = []
        for j, i in enumerate(LEDEN):
            tk.Label(self.window, text=i).grid(row=j + 1, column=0, padx=10, sticky='w')

            present_var = tk.BooleanVar(self.window)
            present_var.set(False)
            tk.Checkbutton(self.window, var=present_var).grid(row=j + 1, column=1, padx=10, sticky='w')
            self.present_vars.append(present_var)

            host_var = tk.BooleanVar(self.window)
            host_var.set(False)
            tk.Checkbutton(self.window, var=host_var).grid(row=j + 1, column=2, padx=10, sticky='w')
            self.host_vars.append(host_var)

        tk.Label(self.window, text="Naam").grid(row=0, column=0, padx=10, sticky='w')
        tk.Label(self.window, text="Aanwezig").grid(row=0, column=1, padx=10, sticky='w')
        tk.Label(self.window, text="Host").grid(row=0, column=2, padx=10, sticky='w')

        tk.Label(self.window, text="Aantal mensen per groep").grid(row=len(LEDEN)+1, column=0, padx=10, sticky='w')
        tk.Label(self.window, text="Aantal twijvelaars").grid(row=len(LEDEN)+2, column=0, padx=10, sticky='w')

        self.group_size_entry = tk.Entry(self.window)
        self.group_size_entry.insert(0, "4")
        self.group_size_entry.grid(row=len(LEDEN)+1, column=1, columnspan=2, padx=10, sticky='we')

        self.doubters_entry = tk.Entry(self.window)
        self.doubters_entry.insert(0, "2")
        self.doubters_entry.grid(row=len(LEDEN)+2, column=1, columnspan=2, padx=10, sticky='we')

        tk.Button(self.window, text="Genereer groepen!", command=self.create_lists).grid(row=len(LEDEN)+3, column=0,
                                                                                         columnspan=3, padx=10,
                                                                                         sticky='we')

    def create_lists(self):
        self.present = []
        self.host = []
        self.groups = []

        try:
            self.group_size = int(self.group_size_entry.get())
            if self.group_size < 0:
                msg.showerror('Latrones Groepen Generator', 'Je bent nu gewoon bewust fouten aan het zoeken in mijn '
                                                            'programma, ik heb je wel door! Even zien wat er gebeurt '
                                                            'als je een negatief getal invult. Helaas, '
                                                            'je krijgt gewoon een error bericht. Jammer hé!')
                return
        except ValueError:
            msg.showerror('Latrones Groepen Generator', 'Vul een geldige groepsgrote in')

        try:
            self.doubters = int(self.doubters_entry.get())
            if self.doubters < 0:
                msg.showerror('Latrones Groepen Generator', 'Vul 0 of een positief aantal twijvelaars in')
                return
        except ValueError:
            msg.showerror('Latrones Groepen Generator', 'Vul een geldig aantal twijvelaars in')

        for j, i in enumerate(self.present_vars):
            if i.get():
                self.present.append(LEDEN[j])

        for j, i in enumerate(self.host_vars):
            if i.get():
                if LEDEN[j] not in self.present:
                    msg.showerror('Latrones Groepen Generator', 'Een host moet present zijn')
                    return
                self.host.append(LEDEN[j])

        if not self.present:
            msg.showerror('Latrones Groepen Generator', 'Er moet minimaal 1 persoon aanwezig zijn')
            return

        self.generate_groups()

    def generate_groups(self):
        # Maak aantal groepen
        amount_of_groups = int(len(self.present) / self.group_size)
        if len(self.present) % self.group_size > 0:
            amount_of_groups += 1

        # Check of er genoeg hosts zijn
        if len(self.host) < amount_of_groups:
            msg.showerror('Latrones Groepen Generator', 'Er zijn niet genoeg hosts')
            return

        # Voeg ruimte voor twijfelaars toe
        if (len(self.present)+self.doubters) / amount_of_groups > self.group_size:
            amount_of_groups += 1

        if len(self.host) < amount_of_groups:
            msg.showerror('Latrones Groepen Generator', 'Er zijn niet genoeg hosts, als het aantal twijvelaars '
                                                        'verlaagd wordt wel')
            return

        for i in range(amount_of_groups):
            self.groups.append([])

        self.fill_groups()

    def fill_groups(self):
        for i in range(len(self.groups)):
            host = random.choice(self.host)
            self.groups[i].append(host)
            self.host.remove(host)
            self.present.remove(host)

        while self.present:
            for i in range(len(self.groups)):
                if self.present:
                    person = random.choice(self.present)
                    self.groups[i].append(person)
                    self.present.remove(person)

        self.display_groups()

    def print_groups(self):
        for i in self.groups:
            for j in i:
                print(j)
            print("-----------------")
        print("*****************************")

    def display_groups(self):
        groups_window = tk.Tk()
        groups_window.title("Groepen")
        groups_window.iconbitmap(default=resource_path(datafile))

        bold = Font(size=15, weight="bold")

        for i in range(len(self.groups)):
            tk.Label(groups_window, text=f"Groep {i + 1}", font=bold).grid(row=0, column=i, padx=10, sticky='w')

        for j, i in enumerate(self.groups):
            for l, k in enumerate(i):
                tk.Label(groups_window, text=k).grid(row=l + 1, column=j, padx=10, sticky='w')

        groups_window.mainloop()


datafile = "Latroneslogo.ico"
if not hasattr(sys, "frozen"):
    datafile = os.path.join(os.path.dirname(__file__), datafile)
else:
    datafile = os.path.join(sys.prefix, datafile)



root = tk.Tk()
root.title("Latrones Groepen Generator")
root.iconbitmap(default=resource_path(datafile))
window = LatronesShuffelerWindow(root)
root.mainloop()
