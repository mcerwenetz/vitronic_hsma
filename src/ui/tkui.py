import tkinter as tk
from tkinter import ttk
import os
import dotenv
import psycopg2

# Load environment variables from .env file
#load_dotenv()
# Access environment variables
# DATABASE_HOST = os.getenv('DATABASE_HOST')
# DATABASE_PORT = os.getenv('DATABASE_PORT')
# DATABASE_USER = os.getenv('DATABASE_USER')
# DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
# DATABASE = os.getenv('DATABASE')
DATABASE_HOST = "172.19.143.117"
DATABASE_PORT = 5432
DATABASE_USER = "vitronic"
DATABASE_PASSWORD = "vitronicpasswd"
DATABASE = "vitronicdb"
DELAY = 250#millis

conn = psycopg2.connect(host=DATABASE_HOST, database=DATABASE, user=DATABASE_USER, password=DATABASE_PASSWORD, port=DATABASE_PORT)
def fetch_data():
    """Fetches data from the database and returns it."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parceldump')
    rows = cursor.fetchall()
    cursor.close()
    # conn.close()
    #now = datetime.datetime.now()
    #next= datetime.datetime.now()
    #dbentry = [0,17,42,0,now,next,1] #id, len, height, gate, ts1, ts2, status, (features)
    #dbentry2 = [1,42,17,0,now,next,2]
    #rows = [dbentry,dbentry2]
    for row in rows:
        row=list(row)
        row[6] = bin(row[6])[2:].zfill(4)
    return rows

# Create the main application window
root = tk.Tk()
root.title("Parcel Database")

# Configure the main window to adjust with resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a frame for the TreeView
frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Configure the frame to adjust with resizing
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Define columns
columns = ('Id', 'Lenght', 'Height', 'Gate', 'Last Seen TS', 'Expected Next TS', 'Status')

# Create the TreeView widget
tree = ttk.Treeview(frame, columns=columns, show='headings')

# Define headings and column properties
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')

# Add vertical scrollbar to the TreeView
vsb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=vsb.set)
vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))

# Add horizontal scrollbar to the TreeView
hsb = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
tree.configure(xscroll=hsb.set)
hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

# Add the TreeView to the frame
tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

# Function to insert new data into the TreeView
def insert_data():
    tree.delete(*tree.get_children())
    data = fetch_data()
    for item in data:
        tree.insert('', tk.END, values=item)
    root.after(DELAY, insert_data)  # Schedule this function to run again after 1000 milliseconds (1 second)

# Start inserting data
insert_data()
# Start the Tkinter event loop
root.mainloop()
