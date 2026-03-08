"""
A user management GUI implement with Tk.
The GUI sends requests to a user REST service.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# TODO: import the `requests` module


# ----------------------------------------------------------------
# REST FUNCTIONS
# ----------------------------------------------------------------

# TODO: note the base URL that will be used for all REST requests
#       (no code change required)
base_url = 'http://localhost:5001/rest/users'

def get_users():
    print("Getting users...")

    # TODO: create a tuple with the REST service's login credentials.
    #       The username is 'admin' and the password is 'adminpw'
    # HINT: see slide 9-35


    # TODO: set the HTTP Accept header to 'application/json'


    # TODO: send a GET request to the base URL. Store the result in a
    #       variable named 'response'


    # TODO: if the response status code is not 200, raise a RuntimeError


    # TODO: get the JSON body from the response


    # TODO: return the 'users' property of the JSON body instead of
    #       an empty list
    return []


def add_user(user_record):
    print("Adding user:", user_record)
    # TODO: note that the `user_record` parameter is a dict that is populated
    #       with the data from the GUI's form input fields
    #       (no code change required)

    # TODO: use the same login credentials and Accept header values as in
    #       the previous function.


    # TODO: send a POST request to the base URL. Pass the `user_record`
    #       parameter as the JSON data. Store the result in a variable
    #       named `response`.
    # HINT: see slide 9-36


    # TODO: if the response status code is not 201, raise a RuntimeError



def update_user(user_record):
    print("Updating user:", user_record)

    # TODO: build a URL by concatenating the base URL, a forward slash, and
    #       the parameter's `email` value
    # HINT: remember that the parameter is a dict
    # HINT: see slide 9-37


    # TODO: use the same login credentials and Accept header values as in
    #       the previous function


    # TODO: send a PUT request to the base URL. Pass the `user_record`
    #       parameter as the JSON data. Store the result in a variable
    #       named `response`


    # TODO: if the response status code is not 202, raise a RuntimeError



def delete_user(user_email):
    print("Deleting user:", user_email)

    # TODO: build a URL by concatenating the base URL, a forward slash, and
    #       the `user_email` parameter
    # HINT: see slide 9-37


    # TODO: use the same login credentials as in the previous function


    # TODO: send a DELETE request to the base URL


    # TODO: if the response status code is not 204, raise a RuntimeError



# ----------------------------------------------------------------
# GUI APPLICATION
# ----------------------------------------------------------------

class UserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management")
        self.root.geometry("500x750")

        self.setup_global_font()

        # Layout rows
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.setup_display_list_section()
        self.setup_record_form()
        self.setup_status_bar()

        self.load_users()

    # ------------------------------------------------------------
    # GLOBAL FONT + THEME
    # ------------------------------------------------------------
    def setup_global_font(self):
        style = ttk.Style()
        style.theme_use("clam")
        default_font = ("Helvetica", 12)
        self.root.option_add("*Font", default_font)
        style.configure(".", font=default_font)

    # ------------------------------------------------------------
    # SCROLLING LIST OF RECORDS
    # ------------------------------------------------------------
    def setup_display_list_section(self):
        self.display_frame = ttk.Frame(self.root, padding="10")
        self.display_frame.grid(row=0, column=0, sticky="nsew")
        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.rowconfigure(0, weight=1)

        # Listbox + Scrollbar
        self.listbox = tk.Listbox(self.display_frame, height=12)
        self.listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        # Buttons
        btn_frame = ttk.Frame(self.display_frame)
        btn_frame.grid(row=1, column=0, sticky="ew", pady=5)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        ttk.Button(btn_frame, text="Load Selected", command=self.load_selected_record).grid(row=0, column=0, sticky="w")
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected_record).grid(row=0, column=1, sticky="e")

    # ------------------------------------------------------------
    # FULL RECORD EDITING FORM
    # ------------------------------------------------------------
    def setup_record_form(self):
        self.form_frame = ttk.Frame(self.root, padding="10")
        self.form_frame.grid(row=1, column=0, sticky="nsew")
        self.form_frame.columnconfigure(1, weight=1)

        # StringVars
        self.first_name_var = tk.StringVar()
        self.middles_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.street_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.state_var = tk.StringVar()
        self.post_code_var = tk.StringVar()
        self.country_var = tk.StringVar()

        fields = [
            ("First Name", self.first_name_var),
            ("Middle Name", self.middles_var),
            ("Last Name", self.last_name_var),
            ("Email", self.email_var),
            ("Street", self.street_var),
            ("City", self.city_var),
            ("State", self.state_var),
            ("Post Code", self.post_code_var),
            ("Country", self.country_var),
        ]

        for i, (label, var) in enumerate(fields):
            ttk.Label(self.form_frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=3)
            ttk.Entry(self.form_frame, textvariable=var).grid(row=i, column=1, sticky="ew", padx=5, pady=3)

        # Buttons
        ttk.Button(self.form_frame, text="Add / Update", command=self.save_record).grid(row=20, column=0, pady=10)
        ttk.Button(self.form_frame, text="Clear Form", command=self.clear_form).grid(row=20, column=1, pady=10)

        self.current_index = None

    # ------------------------------------------------------------
    # STATUS BAR
    # ------------------------------------------------------------
    def setup_status_bar(self):
        self.status_var = tk.StringVar(value="Ready.")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            relief="sunken",
            padding=5
        )
        self.status_bar.grid(row=3, column=0, sticky="ew")

    def set_status(self, message):
        self.status_var.set(message)
        self.status_bar.update_idletasks()

    # ------------------------------------------------------------
    # LOAD RECORDS INTO LISTBOX
    # ------------------------------------------------------------
    def load_users(self):
        self.set_status("Loading users...")
        try:
            self.listbox.delete(0, tk.END)
            self.records = get_users()

            for rec in self.records:
                display = f"{rec['first_name']} {rec['last_name']} — {rec['email']}"
                self.listbox.insert(tk.END, display)

            self.set_status(f"Loaded {len(self.records)} users.")
        except Exception as e:
            self.set_status("Failed to load users.")
            messagebox.showerror("Error", f"Failed to retrieve users: {e}")

    # ------------------------------------------------------------
    # LOAD SELECTED RECORD INTO FORM
    # ------------------------------------------------------------
    def load_selected_record(self):
        sel = self.listbox.curselection()
        if not sel:
            return

        idx = sel[0]
        rec = self.records[idx]
        self.current_index = idx

        self.first_name_var.set(rec["first_name"])
        self.middles_var.set(rec["middles"])
        self.last_name_var.set(rec["last_name"])
        self.email_var.set(rec["email"])

        addr = rec["address"]
        self.street_var.set(addr["street"])
        self.city_var.set(addr["city"])
        self.state_var.set(addr["state"])
        self.post_code_var.set(addr["post_code"])
        self.country_var.set(addr["country"])

        self.set_status("Record loaded into form.")

    # ------------------------------------------------------------
    # CLEAR FORM
    # ------------------------------------------------------------
    def clear_form(self):
        self.current_index = None
        for var in [
            self.first_name_var, self.middles_var, self.last_name_var,
            self.email_var, self.street_var, self.city_var,
            self.state_var, self.post_code_var, self.country_var
        ]:
            var.set("")
        self.set_status("Form cleared.")

    # ------------------------------------------------------------
    # SAVE (ADD OR UPDATE)
    # ------------------------------------------------------------
    def save_record(self):
        self.set_status("Saving record...")

        record = {
            "email": self.email_var.get(),
            "first_name": self.first_name_var.get(),
            "middles": self.middles_var.get(),
            "last_name": self.last_name_var.get(),
            "address": {
                "country": self.country_var.get(),
                "street": self.street_var.get(),
                "city": self.city_var.get(),
                "post_code": self.post_code_var.get(),
                "state": self.state_var.get()
            }
        }

        try:
            if self.current_index is None:
                add_user(record)
                self.set_status("Record added.")
            else:
                update_user(record)
                self.set_status("Record updated.")

            self.load_users()
            self.clear_form()

        except Exception as e:
            self.set_status("Save failed.")
            messagebox.showerror("Error", f"Failed to save record: {e}")

    # ------------------------------------------------------------
    # DELETE SELECTED RECORD
    # ------------------------------------------------------------
    def delete_selected_record(self):
        sel = self.listbox.curselection()
        if not sel:
            return

        idx = sel[0]
        rec = self.records[idx]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete {rec['first_name']} {rec['last_name']}?")
        if not confirm:
            return

        self.set_status("Deleting record...")

        try:
            delete_user(rec["email"])  # or rec["id"] if your service uses IDs
            self.set_status("Record deleted.")
            self.load_users()
        except Exception as e:
            self.set_status("Delete failed.")
            messagebox.showerror("Error", f"Failed to delete record: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()
