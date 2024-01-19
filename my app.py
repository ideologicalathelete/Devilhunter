import tkinter as tk
from tkinter import messagebox
import mysql.connector as mycon

def delete_record():
    ttnum_str = ttnum_entry.get()
    if not ttnum_str.isdigit():
        messagebox.showerror("Error", "Invalid TTNumber. Please enter a valid number.")
        return

    ttnum = int(ttnum_str)

    # Check if the record with the specified TTNumber exists
    cur.execute(f"SELECT * FROM octimetable WHERE ttnum = {ttnum}")
    existing_record = cur.fetchone()

    if not existing_record:
        messagebox.showinfo("Info", f"No record found with TTNumber: {ttnum}")
        return

    # Confirm deletion with the user
    confirm_message = f"Do you want to delete the record with TTNumber {ttnum}?"
    confirmed = messagebox.askyesno("Confirm Deletion", confirm_message)

    if confirmed:
        # Delete the record
        delete_qry = f"DELETE FROM octimetable WHERE ttnum = {ttnum}"

        try:
            cur.execute(delete_qry)
            con.commit()
            messagebox.showinfo("Success", f"Record with TTNumber {ttnum} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting record: {str(e)}")

def clear_fields():
    ttnum_entry.delete(0, tk.END)
    clss_entry.delete(0, tk.END)
    section_entry.delete(0, tk.END)
    day1_entry.delete(0, tk.END)
    time1_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)

def insert_record():
    # Validate input fields
    ttnum_str = ttnum_entry.get()
    if not ttnum_str.isdigit():
        messagebox.showerror("Error", "Invalid TTNumber. Please enter a valid number.")
        return

    ttnum = int(ttnum_str)
    clss = clss_entry.get()
    section = section_entry.get()
    day1 = day1_entry.get()
    time1 = time1_entry.get()
    subject = subject_entry.get()

    if not all([clss, section, day1, time1, subject]):
        messagebox.showerror("Error", "All fields must be filled.")
        return

    # Find the maximum ttnum value in the current records
    cur.execute("SELECT MAX(ttnum) FROM octimetable")
    max_ttnum = cur.fetchone()[0]

    # If no records exist, set max_ttnum to 0
    max_ttnum = max_ttnum if max_ttnum is not None else 0

    # Increment the value to generate a new unique ttnum
    ttnum = max_ttnum + 1

    qry = "INSERT INTO octimetable (ttnum, clss, section, day1, time1, subject) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (ttnum, clss, section, day1, time1, subject)

    try:
        cur.execute(qry, values)
        con.commit()
        messagebox.showinfo("Success", f"Record inserted successfully with TTNumber: {ttnum}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inserting record: {str(e)}")

def retrieve_records():
    qry = "SELECT * FROM octimetable ORDER BY ttnum"
    cur.execute(qry)
    data = cur.fetchall()

    if not data:
        messagebox.showinfo("Info", "No records found.")
        return

    records_window = tk.Toplevel(root)
    records_window.title("Records")

    # Display records in a listbox
    records_listbox = tk.Listbox(records_window, width=70)
    records_listbox.pack(padx=10, pady=10)

    for row in data:
        record_str = f"TTNumber: {row[0]}, Class: {row[1]}, Section: {row[2]}, Day: {row[3]}, Time: {row[4]}, Subject: {row[5]}"
        records_listbox.insert(tk.END, record_str)

def update_record():
    ttnum = int(ttnum_entry.get())

    qry = f"SELECT * FROM octimetable WHERE ttnum = {ttnum} ORDER BY ttnum"
    cur.execute(qry)
    row = cur.fetchone()

    if not row:
        messagebox.showinfo("Info", "No record found for the given TTNumber.")
        return

    update_window = tk.Toplevel(root)
    update_window.title("Update Record")

    # Display the record for updating
    update_label = tk.Label(update_window, text=f"Updating record with TTNumber: {ttnum}")
    update_label.pack(pady=10)

    # Add entry widgets for updating fields
    update_clss_entry = tk.Entry(update_window, width=30)
    update_clss_entry.insert(0, row[1])
    update_clss_entry.pack(pady=5)

    update_section_entry = tk.Entry(update_window, width=30)
    update_section_entry.insert(0, row[2])
    update_section_entry.pack(pady=5)

    update_day1_entry = tk.Entry(update_window, width=30)
    update_day1_entry.insert(0, row[3])
    update_day1_entry.pack(pady=5)

    update_time1_entry = tk.Entry(update_window, width=30)
    update_time1_entry.insert(0, row[4])
    update_time1_entry.pack(pady=5)

    update_subject_entry = tk.Entry(update_window, width=30)
    update_subject_entry.insert(0, row[5])
    update_subject_entry.pack(pady=5)

    def perform_update():
        new_clss = update_clss_entry.get()
        new_section = update_section_entry.get()
        new_day1 = update_day1_entry.get()
        new_time1 = update_time1_entry.get()
        new_subject = update_subject_entry.get()

        update_qry = f"UPDATE octimetable SET clss = '{new_clss}', section = '{new_section}', day1 = '{new_day1}', "\
                     f"time1 = '{new_time1}', subject = '{new_subject}' WHERE ttnum = {ttnum}"

        try:
            cur.execute(update_qry)
            con.commit()
            messagebox.showinfo("Success", "Record updated successfully.")
            update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating record: {str(e)}")

    update_button = tk.Button(update_window, text="Update", command=perform_update)
    update_button.pack(pady=10)

# Connect to MySQL
con = mycon.connect(host='localhost', port='3306', user='root', passwd='1234')
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS onlineclass")
cur.execute("USE onlineclass")
cur.execute("CREATE TABLE IF NOT EXISTS octimetable(ttnum INT(5) PRIMARY KEY, clss CHAR(5), "\
            "section CHAR(5), day1 CHAR(15), time1 CHAR(10), subject CHAR(25))")

# Create the main window
root = tk.Tk()
root.title("MySQL CRUD App")
root.configure(bg="#F0F0F0")  # Set background color

# User Manual Frame
user_manual_frame = tk.Frame(root, bg="#F0F0F0")
user_manual_frame.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="nsew")

# User Manual Text
user_manual_text = """Welcome to the MySQL CRUD App!

Operations:
- Insert Record: Click 'Insert Record' to add a new timetable entry.
- Retrieve Records: Click 'Retrieve Records' to view all timetable entries.
- Update Record: Click 'Update Record' to modify an existing timetable entry.
- Delete Record: Click 'Delete Record' to remove a timetable entry.
- Clear Fields: Click 'Clear Fields' to reset input fields.
- Exit: Click 'Exit' to close the application.

Ensure all fields are filled before performing any operation.

Enjoy using the MySQL CRUD App!
"""

user_manual_label = tk.Label(user_manual_frame, text=user_manual_text, font=("Helvetica", 12), justify=tk.LEFT, bg="#F0F0F0")
user_manual_label.pack()

# Add a separator line
separator_line = tk.Frame(root, height=2, width=400, bd=1, relief=tk.SUNKEN)
separator_line.grid(row=1, column=0, columnspan=2, pady=10)

# Buttons Frame
buttons_frame = tk.Frame(root, bg="#F0F0F0")
buttons_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))



# Add entry widgets for inserting fields
ttnum_label = tk.Label(root, text="TTNumber:")
ttnum_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
ttnum_entry = tk.Entry(root, width=30)
ttnum_entry.grid(row=0, column=1, padx=10, pady=5)

clss_label = tk.Label(root, text="Class:")
clss_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
clss_entry = tk.Entry(root, width=30)
clss_entry.grid(row=1, column=1, padx=10, pady=5)

section_label = tk.Label(root, text="Section:")
section_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
section_entry = tk.Entry(root, width=30)
section_entry.grid(row=2, column=1, padx=10, pady=5)

day1_label = tk.Label(root, text="Day:")
day1_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
day1_entry = tk.Entry(root, width=30)
day1_entry.grid(row=3, column=1, padx=10, pady=5)

time1_label = tk.Label(root, text="Time:")
time1_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
time1_entry = tk.Entry(root, width=30)
time1_entry.grid(row=4, column=1, padx=10, pady=5)

subject_label = tk.Label(root, text="Subject:")
subject_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
subject_entry = tk.Entry(root, width=30)
subject_entry.grid(row=5, column=1, padx=10, pady=5)

# Create buttons for different operations
insert_button = tk.Button(buttons_frame, text="Insert Record", command=insert_record, bg="#4CAF50", fg="white", font=("Helvetica", 12))
insert_button.grid(row=0, column=0, pady=10, padx=5)

retrieve_button = tk.Button(buttons_frame, text="Retrieve Records", command=retrieve_records, bg="#008CBA", fg="white", font=("Helvetica", 12))
retrieve_button.grid(row=0, column=1, pady=10, padx=5)

update_button = tk.Button(buttons_frame, text="Update Record", command=update_record, bg="#FFA500", fg="white", font=("Helvetica", 12))
update_button.grid(row=0, column=2, pady=10, padx=5)

delete_button = tk.Button(buttons_frame, text="Delete Record", command=delete_record, bg="#FF6347", fg="white", font=("Helvetica", 12))
delete_button.grid(row=0, column=3, pady=10, padx=5)

clear_button = tk.Button(buttons_frame, text="Clear Fields", command=clear_fields, bg="#808080", fg="white", font=("Helvetica", 12))
clear_button.grid(row=0, column=4, pady=10, padx=5)

exit_button = tk.Button(buttons_frame, text="Exit", command=root.destroy, bg="#D9534F", fg="white", font=("Helvetica", 12))
exit_button.grid(row=0, column=5, pady=10, padx=5)


# Run the Tkinter main loop
root.mainloop()

