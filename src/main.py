import tkinter as tk
from tkinter import ttk
from gui.main_gui import MainGUI

def main():
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()