import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
from dorm_assistant import DormHelper  # Import core logic class

class DormHelperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dormitory Helper")
        self.root.geometry("750x600")
        # Solve Chinese display issues (kept for potential future use)
        self.root.option_add("*Font", "SimHei 10")
        self.root.encoding = "utf-8"

        # Initialize core logic
        self.dorm_helper = DormHelper()
        self.dorm_helper.startup_sync()  # Sync data on startup
        self.init_ui()

    def init_ui(self):
        # Tab container
        self.tab_control = ttk.Notebook(self.root)
        
        # 1. Daily Reminder Tab
        self.tab_reminder = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_reminder, text="Daily Reminder")
        self.update_reminder_tab()
        
        # 2. Deadlines Tab
        self.tab_ddl = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_ddl, text="Deadlines")
        self.init_ddl_tab()
        
        # 3. Shopping List Tab
        self.tab_shopping = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_shopping, text="Shopping List")
        self.init_shopping_tab()
        
        # 4. Duty Roster Tab
        self.tab_duty = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_duty, text="Duty Roster")
        self.update_duty_tab()
        
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        # Bottom button bar
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(self.bottom_frame, text="Sync Data", command=self.sync_data).pack(side="left", padx=5)
        ttk.Button(self.bottom_frame, text="Save Data", command=self.save_data).pack(side="left", padx=5)
        ttk.Button(self.bottom_frame, text="Help", command=self.show_help).pack(side="left", padx=5)
        ttk.Button(self.bottom_frame, text="Exit", command=self.quit_app).pack(side="right", padx=5)

    # --------------------------
    # Daily Reminder Tab
    # --------------------------
    def update_reminder_tab(self):
        for widget in self.tab_reminder.winfo_children():
            widget.destroy()
        
        today_str = datetime.date.today().isoformat()
        frame = ttk.Frame(self.tab_reminder)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Title
        ttk.Label(frame, text=f"Dormitory Helper | {today_str}", font=("SimHei", 14, "bold")).pack(anchor="w", pady=5)
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=5)
        
        # Core reminder content
        reminder_frame = ttk.Frame(frame)
        reminder_frame.pack(anchor="w", pady=10)
        
        # Duty information
        current_duty = self.dorm_helper.data['roster'][0] if self.dorm_helper.data['roster'] else "None"
        ttk.Label(reminder_frame, text=f"🧹 Today's Duty: {current_duty}", font=("SimHei", 12)).pack(anchor="w", pady=3)
        
        # Upcoming deadlines
        ttk.Label(reminder_frame, text="📅 Upcoming Deadlines (Top 3):", font=("SimHei", 12, "bold")).pack(anchor="w", pady=5)
        sorted_ddls = sorted(self.dorm_helper.data['ddls'], key=lambda x: x['date'])
        if not sorted_ddls:
            ttk.Label(reminder_frame, text="   No deadlines", font=("SimHei", 11)).pack(anchor="w")
        else:
            for task in sorted_ddls[:3]:
                ttk.Label(reminder_frame, text=f"   - {task['date']} : {task['title']}", font=("SimHei", 11)).pack(anchor="w")

        # Shopping list reminder
        ttk.Label(reminder_frame, text="🛒 Shopping List (Top 5):", font=("SimHei", 12, "bold")).pack(anchor="w", pady=5)
        shopping_data = self.dorm_helper.data['shopping']
        if not shopping_data:
            ttk.Label(reminder_frame, text="   No items to buy", font=("SimHei", 11)).pack(anchor="w")
        else:
            for idx, (item, count) in enumerate(list(shopping_data.items())[:5], 1):
                ttk.Label(reminder_frame, text=f"   - {item} × {count}", font=("SimHei", 11)).pack(anchor="w")

    # --------------------------
    # Deadlines Tab
    # --------------------------
    def init_ddl_tab(self):
        # Top input area
        input_frame = ttk.Frame(self.tab_ddl)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").pack(side="left", padx=5)
        self.ddl_date = ttk.Entry(input_frame, width=15)
        self.ddl_date.pack(side="left", padx=5)
        self.ddl_date.insert(0, datetime.date.today().isoformat())  # Default to today
        
        ttk.Label(input_frame, text="Task Name:").pack(side="left", padx=5)
        self.ddl_title = ttk.Entry(input_frame, width=40)
        self.ddl_title.pack(side="left", padx=5)
        
        ttk.Button(input_frame, text="Add", command=self.add_ddl).pack(side="left", padx=5)
        
        # List display area
        self.ddl_listbox = tk.Listbox(self.tab_ddl, width=90, height=18, font=("SimHei", 10))
        self.ddl_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Bottom buttons
        btn_frame = ttk.Frame(self.tab_ddl)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_ddl).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh List", command=self.refresh_ddl_list).pack(side="left", padx=5)
        
        self.refresh_ddl_list()  # Initial load

    def add_ddl(self):
        date = self.ddl_date.get().strip()
        title = self.ddl_title.get().strip()
        if not date or not title:
            messagebox.showwarning("Input Error", "Date and task name cannot be empty!")
            return
        # Date format validation
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Format Error", "Incorrect date format! Please use YYYY-MM-DD")
            return
        # Call core logic to add
        self.dorm_helper.add_ddl([date, title])
        # Clear input boxes
        self.ddl_date.delete(0, tk.END)
        self.ddl_title.delete(0, tk.END)
        self.ddl_date.insert(0, datetime.date.today().isoformat())
        self.refresh_ddl_list()
        messagebox.showinfo("Success", "Deadline added successfully!")

    def refresh_ddl_list(self):
        self.ddl_listbox.delete(0, tk.END)
        sorted_ddls = sorted(self.dorm_helper.data['ddls'], key=lambda x: x['date'])
        if not sorted_ddls:
            self.ddl_listbox.insert(tk.END, "📅 No deadlines, click above to add～")
            return
        for idx, ddl in enumerate(sorted_ddls, 1):
            self.ddl_listbox.insert(tk.END, f"[{idx}] {ddl['date']} | {ddl['title']}")

    def delete_ddl(self):
        selected = self.ddl_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to delete first!")
            return
        idx = selected[0]
        sorted_ddls = sorted(self.dorm_helper.data['ddls'], key=lambda x: x['date'])
        # Find original index (since list is sorted, need to match id)
        ddl_id = sorted_ddls[idx]['id']
        original_idx = next(i for i, d in enumerate(self.dorm_helper.data['ddls']) if d['id'] == ddl_id)
        # Delete
        self.dorm_helper.data['ddls'].pop(original_idx)
        self.refresh_ddl_list()
        messagebox.showinfo("Success", "Deadline has been deleted!")

    # --------------------------
    # Shopping List Tab
    # --------------------------
    def init_shopping_tab(self):
        # Top input area
        input_frame = ttk.Frame(self.tab_shopping)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Item Name:").pack(side="left", padx=5)
        self.shop_item = ttk.Entry(input_frame, width=40)
        self.shop_item.pack(side="left", padx=5)
        
        ttk.Button(input_frame, text="Add to List", command=self.add_shopping_item).pack(side="left", padx=5)
        
        # List display area
        self.shop_listbox = tk.Listbox(self.tab_shopping, width=90, height=18, font=("SimHei", 10))
        self.shop_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Bottom button area
        btn_frame = ttk.Frame(self.tab_shopping)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_shopping_item).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_shopping_list).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh List", command=self.refresh_shopping_list).pack(side="left", padx=5)
        
        self.refresh_shopping_list()  # Initial load

    def add_shopping_item(self):
        item = self.shop_item.get().strip()
        if not item:
            messagebox.showwarning("Input Error", "Item name cannot be empty!")
            return
        # Call core logic to add
        self.dorm_helper.shop_add([item])
        # Clear input box
        self.shop_item.delete(0, tk.END)
        self.refresh_shopping_list()
        messagebox.showinfo("Success", f"Added [{item}] to shopping list!")

    def refresh_shopping_list(self):
        self.shop_listbox.delete(0, tk.END)
        shopping_data = self.dorm_helper.data['shopping']
        if not shopping_data:
            self.shop_listbox.insert(tk.END, "🛒 Shopping list is empty, click above to add items～")
            return
        # Display sorted by item name
        sorted_items = sorted(shopping_data.items(), key=lambda x: x[0])
        for idx, (item_name, count) in enumerate(sorted_items, 1):
            self.shop_listbox.insert(tk.END, f"[{idx}] {item_name} × {count}")

    def delete_shopping_item(self):
        selected = self.shop_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an item to delete first!")
            return
        idx = selected[0]
        shopping_data = self.dorm_helper.data['shopping']
        if "shopping list is empty" in self.shop_listbox.get(0):
            return
        # Get selected item name
        item_line = self.shop_listbox.get(idx)
        item_name = item_line.split(" × ")[0].split("] ")[1]
        # Delete
        del shopping_data[item_name]
        self.refresh_shopping_list()
        messagebox.showinfo("Success", f"Deleted [{item_name}]!")

    def clear_shopping_list(self):
        shopping_data = self.dorm_helper.data['shopping']
        if not shopping_data:
            messagebox.showinfo("Notice", "Shopping list is already empty!")
            return
        confirm = messagebox.askyesno("Confirm Clear", "Do you want to clear all shopping items? (Irreversible)")
        if confirm:
            self.dorm_helper.shop_clear()
            self.refresh_shopping_list()
            messagebox.showinfo("Success", "Shopping list has been cleared～")

    # --------------------------
    # Duty Roster Tab
    # --------------------------
    def update_duty_tab(self):
        # Clear existing content
        for widget in self.tab_duty.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(self.tab_duty)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Title
        ttk.Label(frame, text="🧹 Dormitory Duty Roster", font=("SimHei", 14, "bold")).pack(anchor="w", pady=5)
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=5)
        
        # Core content area
        duty_frame = ttk.Frame(frame)
        duty_frame.pack(anchor="w", pady=10)
        
        # Today's duty
        duty_list = self.dorm_helper.data['roster']
        current_duty = duty_list[0] if duty_list else "None"
        ttk.Label(duty_frame, text=f"Today's Duty:", font=("SimHei", 12)).pack(anchor="w", pady=3)
        ttk.Label(duty_frame, text=f"   {current_duty}", font=("SimHei", 14, "bold"), foreground="red").pack(anchor="w", pady=2)
        
        # Rotation button
        ttk.Button(duty_frame, text="Rotate to Next", command=self.rotate_duty, width=15).pack(anchor="w", pady=8)
        
        # Full duty rotation order
        ttk.Label(duty_frame, text="Full Rotation Order:", font=("SimHei", 12, "bold")).pack(anchor="w", pady=5)
        if not duty_list:
            ttk.Label(duty_frame, text="   No duty personnel, please edit dorm_data.json to add", font=("SimHei", 11)).pack(anchor="w")
            return
        # Display all personnel
        for idx, person in enumerate(duty_list, 1):
            if person == current_duty:
                ttk.Label(duty_frame, text=f"   [{idx}] {person} (Current)", font=("SimHei", 11, "bold"), foreground="red").pack(anchor="w")
            else:
                ttk.Label(duty_frame, text=f"   [{idx}] {person}", font=("SimHei", 11)).pack(anchor="w")

        # Add/edit duty personnel (optional function)
        ttk.Button(frame, text="Edit Duty Personnel", command=self.edit_duty_roster).pack(anchor="w", padx=10, pady=10)

    def rotate_duty(self):
        duty_list = self.dorm_helper.data['roster']
        if len(duty_list) < 2:
            messagebox.showwarning("Cannot Rotate", "At least 2 duty personnel are required to rotate!")
            return
        # Rotation logic
        current = duty_list.pop(0)
        duty_list.append(current)
        # Refresh interface
        self.update_duty_tab()
        self.update_reminder_tab()
        messagebox.showinfo("Rotation Successful", f"Rotated to next person: {duty_list[0]}")

    def edit_duty_roster(self):
        # Read current duty personnel
        current_roster = self.dorm_helper.data['roster']
        current_str = "\n".join(current_roster) if current_roster else "Please enter duty personnel, one per line"
        # Pop up input box
        new_str = simpledialog.askstring(
            "Edit Duty Personnel",
            "Please enter duty personnel (one per line, order determines rotation):",
            initialvalue=current_str,
            parent=self.root
        )
        if new_str is None:  # Cancel input
            return
        # Process input (remove duplicates, empty lines)
        new_roster = [name.strip() for name in new_str.split("\n") if name.strip()]
        if not new_roster:
            messagebox.showwarning("Input Error", "Duty personnel cannot be empty!")
            return
        # Update data
        self.dorm_helper.data['roster'] = new_roster
        self.update_duty_tab()
        self.update_reminder_tab()
        messagebox.showinfo("Success", "Duty personnel list has been updated!")

    # --------------------------
    # General Functions
    # --------------------------
    def sync_data(self):
        messagebox.showinfo("Syncing", "Syncing data, please wait...")
        if self.dorm_helper._git_command(['pull', '--rebase']):
            self.dorm_helper.data = self.load_data()  # Reload synced data
            self.refresh_all_tabs()
            messagebox.showinfo("Success", "Data has been synced to latest version!")
        else:
            messagebox.showerror("Failed", "Sync failed! Please check:\n1. Network connection\n2. Git installation\n3. Current directory is a Git repository")

    def save_data(self):
        self.dorm_helper.save_data()
        self.dorm_helper.shutdown_sync()
        messagebox.showinfo("Success", "Data has been saved and synced to cloud!")

    def show_help(self):
        help_text = """
📚 Dormitory Helper User Guide:

【Daily Reminder】
- Displays today's duty, upcoming deadlines and shopping list
- Data updates in real-time, no manual refresh needed

【Deadlines】
1. Enter date (YYYY-MM-DD) and task name, click "Add"
2. Select a task and click "Delete Selected" to remove
3. Click "Refresh List" to update display

【Shopping List】
1. Enter item name, click "Add to List" (duplicates auto-increment count)
2. Select an item and click "Delete Selected" to remove individually
3. Click "Clear All" to remove all items

【Duty Roster】
1. Click "Rotate to Next" to automatically switch duty personnel
2. Click "Edit Duty Personnel" to modify the duty list (one name per line)
3. Current duty person is highlighted in red

【Data Sync】
- Click "Sync Data": Pull latest data from cloud (requires Git repository)
- Click "Save Data": Save local changes and push to cloud
- Data is automatically saved when exiting

⚠️ Note:
1. Ensure dorm_data.json is in the same directory as the executable
2. Sync function requires Git installation and configured repository
3. If data file is corrupted, delete it and restart the program (generates default data automatically)
        """
        messagebox.showinfo("Help Information", help_text)

    def quit_app(self):
        if messagebox.askyesno("Confirm Exit", "Do you want to exit Dormitory Helper?\nCurrent data will be saved automatically."):
            self.dorm_helper.save_data()
            self.dorm_helper.shutdown_sync()
            self.root.destroy()

    def refresh_all_tabs(self):
        self.update_reminder_tab()
        self.refresh_ddl_list()
        self.refresh_shopping_list()
        self.update_duty_tab()

    # Reload data (used after sync)
    def load_data(self):
        return self.dorm_helper.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = DormHelperGUI(root)
    root.mainloop()