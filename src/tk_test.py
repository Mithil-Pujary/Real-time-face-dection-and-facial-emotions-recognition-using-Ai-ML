import tkinter as tk

root = tk.Tk()
root.title("Tkinter Test")
root.geometry("400x200")

label = tk.Label(root, text="Tkinter UI Working!", font=("Arial", 16))
label.pack(pady=50)

root.mainloop()
