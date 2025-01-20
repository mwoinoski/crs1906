r"""

"""
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont  # Import the font module

class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management")
        self.root.geometry("1000x600")
        
        # **Global Font Configuration**
        self.setup_global_font()

        # Configure grid layout for the root window to make it responsive
        self.root.rowconfigure(1, weight=1)  # Display customers section
        self.root.columnconfigure(0, weight=1)
        
        # Add Customer Section
        self.setup_add_customer_section()
        
        # Display Customers Section
        self.setup_display_customers_section()
        
        # Load customers on startup
        self.load_customers()
    
    def setup_global_font(self):
        """Sets up the global default font for all ttk widgets."""
        style = ttk.Style()
        
        # **Choose a theme that better supports style changes**
        style.theme_use('clam')  # Options: 'clam', 'alt', 'default', 'classic'
        
        # **Define a new font as a tuple (font_family, size)**
        default_font = ("Helvetica", 12)  # Change to ("Arial", 12) if preferred
        
        self.root.option_add("*Font", default_font)

        # **Apply the font to all ttk widgets**
        style.configure('.', font=default_font)
        
        # **Specifically ensure that 'TEntry' uses the global font**
        # style.configure('TEntry', font=default_font)
        
        # **Optionally, apply the font to other widget styles if desired**
        # style.configure('TLabel', font=default_font)
        # style.configure('TButton', font=default_font)
    
    def setup_add_customer_section(self):
        """Sets up the 'Add Customer' section with input fields and an Add button."""
        self.add_frame = ttk.Frame(self.root, padding="10")
        self.add_frame.grid(row=0, column=0, sticky="ew")
        
        # Configure grid weights to make input fields expandable
        self.add_frame.columnconfigure(1, weight=1)  # Full Name Entry
        self.add_frame.columnconfigure(3, weight=1)  # Email Address Entry
        self.add_frame.columnconfigure(5, weight=1)  # Mailing Address Entry
        self.add_frame.columnconfigure(6, weight=0)  # Add Button
        
        # Full Name
        ttk.Label(self.add_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Email Address
        ttk.Label(self.add_frame, text="Email Address:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.email_entry = ttk.Entry(self.add_frame)
        self.email_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Mailing Address
        ttk.Label(self.add_frame, text="Mailing Address:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.address_entry = ttk.Entry(self.add_frame)
        self.address_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        
        # Add Button
        self.add_button = ttk.Button(self.add_frame, text="Add", command=self.add_customer_action)
        self.add_button.grid(row=0, column=6, padx=5, pady=5, sticky="w")
    
    def setup_display_customers_section(self):
        """Sets up the 'Display Customers' section with a scrollable table."""
        self.display_frame = ttk.Frame(self.root, padding="10")
        self.display_frame.grid(row=1, column=0, sticky="nsew")
        self.display_frame.rowconfigure(0, weight=1)
        self.display_frame.columnconfigure(0, weight=1)
        
        # Create a canvas and a vertical scrollbar for the customer table
        self.canvas = tk.Canvas(self.display_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas to hold the table
        self.table_frame = ttk.Frame(self.canvas)
        # **Capture the window ID returned by create_window**
        self.table_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        
        # Bind the configure event to update the scrollregion
        self.table_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Table Headers
        headers = ["Full Name", "Email Address", "Mailing Address"]
        for idx, header in enumerate(headers):
            # Remove the explicit font for headers to inherit the global font
            label = ttk.Label(self.table_frame, text=header, font=('Arial', 12, 'bold'))
            label.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")
            if header in ["Full Name", "Email Address", "Mailing Address"]:
                self.table_frame.columnconfigure(idx, weight=1)
            else:
                self.table_frame.columnconfigure(idx, weight=0)
        
        # Dictionary to keep track of customer rows
        self.customer_rows = {}
    
    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Adjust the inner frame's width to match the canvas."""
        canvas_width = event.width
        self.canvas.itemconfig(self.table_window, width=canvas_width)
    
    def load_customers(self):
        """Fetches customers from the API and displays them in the table."""
        # Clear existing rows except headers
        for widget in self.table_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        self.customer_rows.clear()
        
        try:
            # Call your actual get_customers() function here
            customers = get_customers()  # Replace with your actual function
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve customers: {e}")
            customers = []
        
        for idx, customer in enumerate(customers, start=1):
            self.add_customer_row(idx, customer)
    
    def add_customer_row(self, row_num, customer):
        """Adds a single customer row to the table."""
        # Full Name Entry
        name_var = tk.StringVar(value=customer['name'])
        name_entry = ttk.Entry(self.table_frame, textvariable=name_var)
        name_entry.grid(row=row_num, column=0, padx=5, pady=2, sticky="ew")
        
        # Email Address Entry
        email_var = tk.StringVar(value=customer['email'])
        email_entry = ttk.Entry(self.table_frame, textvariable=email_var)
        email_entry.grid(row=row_num, column=1, padx=5, pady=2, sticky="ew")
        
        # Mailing Address Entry
        address_var = tk.StringVar(value=customer['address'])
        address_entry = ttk.Entry(self.table_frame, textvariable=address_var)
        address_entry.grid(row=row_num, column=2, padx=5, pady=2, sticky="ew")
        
        # Update Button
        update_button = ttk.Button(self.table_frame, text="Update", width=10, 
                                   command=lambda c=customer: self.update_customer_action(c))
        update_button.grid(row=row_num, column=3, padx=5, pady=2, sticky="w")
        
        # Delete Button
        delete_button = ttk.Button(self.table_frame, text="Delete", width=10, 
                                   command=lambda c=customer: self.delete_customer_action(c))
        delete_button.grid(row=row_num, column=4, padx=5, pady=2, sticky="w")
        
        # Store references to the variables for easy access
        self.customer_rows[customer['id']] = {
            'name_var': name_var,
            'email_var': email_var,
            'address_var': address_var
        }
    
    def add_customer_action(self):
        """Handles the action when the 'Add' button is clicked."""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        
        if not name or not email or not address:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        new_customer = {
            "name": name,
            "email": email,
            "address": address
        }
        
        try:
            # Call your actual add_customer() function here
            add_customer(new_customer)  # Replace with your actual function
            messagebox.showinfo("Success", "Customer added successfully.")
            # Clear the input fields
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.address_entry.delete(0, tk.END)
            # Reload customers
            self.load_customers()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add customer: {e}")
    
    def update_customer_action(self, customer):
        """Handles the action when the 'Update' button is clicked for a customer."""
        customer_id = customer['id']
        updated_name = self.customer_rows[customer_id]['name_var'].get().strip()
        updated_email = self.customer_rows[customer_id]['email_var'].get().strip()
        updated_address = self.customer_rows[customer_id]['address_var'].get().strip()
        
        if not updated_name or not updated_email or not updated_address:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        updated_customer = {
            "id": customer_id,
            "name": updated_name,
            "email": updated_email,
            "address": updated_address
        }
        
        try:
            # Call your actual update_customer() function here
            update_customer(updated_customer)  # Replace with your actual function
            messagebox.showinfo("Success", "Customer updated successfully.")
            # Reload customers
            self.load_customers()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update customer: {e}")
    
    def delete_customer_action(self, customer):
        """Handles the action when the 'Delete' button is clicked for a customer."""
        customer_id = customer['id']
        customer_name = customer['name']
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{customer_name}'?")
        if not confirm:
            return
        
        try:
            # Call your actual delete_customer() function here
            delete_customer(customer_id)  # Replace with your actual function
            messagebox.showinfo("Success", "Customer deleted successfully.")
            # Reload customers
            self.load_customers()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete customer: {e}")

# Placeholder functions for REST API calls
def get_customers():
    """
    Replace this function with your actual implementation.
    It should return a list of dictionaries with keys 'id', 'name', 'email', 'address'.
    """
    # Example dummy data
    return [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "address": "123 Elm Street"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "address": "456 Oak Avenue"},
    ]

def add_customer(customer_data):
    """
    Replace this function with your actual implementation.
    It should accept a dictionary with keys 'name', 'email', 'address'.
    """
    print("Adding customer:", customer_data)

def update_customer(customer_data):
    """
    Replace this function with your actual implementation.
    It should accept a dictionary with keys 'id', 'name', 'email', 'address'.
    """
    print("Updating customer:", customer_data)

def delete_customer(customer_id):
    """
    Replace this function with your actual implementation.
    It should accept the customer's id.
    """
    print("Deleting customer with id:", customer_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()
