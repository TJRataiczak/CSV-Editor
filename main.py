import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import tkinter.messagebox

def select_file(filename, kind):
    if kind == "csv":
        user_file = askopenfilename()
        filename.set(user_file)
    elif kind == "dir":
        user_directory = askdirectory()
        filename.set(user_directory)
        print(user_directory)

def run(old_file, new_file, dump_folder):
    old_data = pd.read_csv(old_file)
    new_data = pd.read_csv(new_file)
    dump_location = dump_folder

    update_records_df = pd.DataFrame()
    add_records_df = pd.DataFrame()

    for record in new_data['0']:
        in_record = old_data[old_data['0'] == record]
        updated_record = new_data[new_data['0'] == record]
        if len(in_record.index) == 1:
            print('Needs Updated')
            update_records_df = update_records_df._append(updated_record)
        elif len(in_record.index) == 0:
            print('Needs Added')
            add_records_df = update_records_df._append(updated_record)

    new_file = new_file.split("/")[-1]

    if update_records_df.empty == False:
        update_records_df.to_csv(dump_location + "/" + new_file[:-4] + "_Update" + new_file[-4:])
    if add_records_df.empty == False:
        add_records_df.to_csv(dump_location + "/" + new_file[:-4] + "_Add" + new_file[-4:])
    
    tkinter.messagebox.showinfo("Finished", "Finished")

root = Tk()
root.title("Updated CSVs")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

old_filename = StringVar()
ttk.Label(mainframe, text="Old File").grid(column=0, row=0)
ttk.Label(mainframe, textvariable=old_filename).grid(column=0, row=1)
ttk.Button(mainframe, text="Choose File", command=lambda: select_file(old_filename, "csv")).grid(column=0, row=2)

new_filename = StringVar()
ttk.Label(mainframe, text="New File").grid(column=0, row=3)
ttk.Label(mainframe, textvariable=new_filename).grid(column=0, row=4)
ttk.Button(mainframe, text="Choose File", command=lambda: select_file(new_filename, "csv")).grid(column=0, row=5)

dump_location = StringVar()
ttk.Label(mainframe, text="Dump Location").grid(column=0, row=6)
ttk.Label(mainframe, textvariable=dump_location).grid(column=0, row=7)
ttk.Button(mainframe, text="Choose File", command=lambda: select_file(dump_location, "dir")).grid(column=0, row=8)

ttk.Button(mainframe, text="Run", command=lambda: run(old_filename.get(), new_filename.get(), dump_location.get())).grid(column=0, row=9, pady= 50, padx=100)

root.mainloop()