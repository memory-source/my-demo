import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from dorm_assistant import DormHelper

class DormHelperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dormitory Helper")
        self.root.geometry("750x600")
        self.root.option_add("*Font", "SimHei 10")
        self.root.encoding = "utf-8"

        self.dorm_helper = DormHelper()
        self.dorm_helper.startup_sync()
        self.init_ui()

    def init_ui(self):
        self.tab_control = ttk.Notebook(self.root)
        
        self.tab_reminder = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_reminder, text="Daily Reminder")
        self.update_reminder_tab()
        
        self.tab_ddl = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_ddl, text="Deadlines")
        self.init_ddl_tab()
        
        self.tab_shopping = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_shopping, text="Shopping List")
        self.init_shopping_tab()
        
        self.tab_duty = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_duty, text="Duty Roster")
        self.update_duty_tab()
        
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(self.bottom_frame, text="Sync Data", command=self.sync_data).pack(side="left", padx=5)
        ttk.Button(self.bottom_frame, text="Save Data", command=self.save_data).pack(side="left", padx=5)
        ttk.Button(self.bottom_frame, text="Help", command=self.show_help).pack(side="left", padx=5)
        ttk.Button(self.bottom_frame, text="Exit", command=self.quit_app).pack(side="right", padx=5)

    def update_reminder_tab(self):
        for widget in self.tab_reminder.winfo_children():
            widget.destroy()
        
        today_str = datetime.date.today().isoformat()
        frame = ttk.Frame(self.tab_reminder)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ttk.Label(frame, text=f"Dormitory Helper | {today_str}", font=("SimHei", 14, "bold")).pack(anchor="w", pady=5)
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=5)
        
        reminder_frame = ttk.Frame(frame)
        reminder_frame.pack(anchor="w", pady=10)
        
        current_duty = self.dorm_helper.data['roster'][0] if self.dorm_helper.data['roster'] else "None"
        ttk.Label(reminder_frame, text=f"🧹 Today's Duty: {current_duty}", font=("SimHei", 12)).pack(anchor="w", pady=3)
        
        ttk.Label(reminder_frame, text="📅 Upcoming Deadlines (Top 3):", font=("SimHei", 12, "bold")).pack(anchor="w", pady=5)
        sorted_ddls = sorted(self.dorm_helper.data['ddls'], key=lambda x: x['date'])
        if not sorted_ddls:
            ttk.Label(reminder_frame, text="   No deadlines", font=("SimHei", 11)).pack(anchor="w")
        else:
            for task in sorted_ddls[:3]:
                ttk.Label(reminder_frame, text=f"   - {task['date']} : {task['title']}", font=("SimHei", 11)).pack(anchor="w")

        ttk.Label(reminder_frame, text="🛒 Shopping List (Top 5):", font=("SimHei", 12, "bold")).pack(anchor="w", pady=5)
        shopping_data = self.dorm_helper.data['shopping']
        if not shopping_data:
            ttk.Label(reminder_frame, text="   No items", font=("SimHei", 11)).pack(anchor="w")
        else:
            for idx, (item, count) in enumerate(list(shopping_data.items())[:5], 1):
                ttk.Label(reminder_frame, text=f"   - {item} x {count}", font=("SimHei", 11)).pack(anchor="w")

    def init_ddl_tab(self):
        input_frame = ttk.Frame(self.tab_ddl)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").pack(side="left", padx=5)
        self.ddl_date = ttk.Entry(input_frame, width=15)
        self.ddl_date.pack(side="left", padx=5)
        self.ddl_date.insert(0, datetime.date.today().isoformat())
        
        ttk.Label(input_frame, text="Task:").pack(side="left", padx=5)
        self.ddl_title = ttk.Entry(input_frame, width=40)
        self.ddl_title.pack(side="left", padx=5)
        
        ttk.Button(input_frame, text="Add", command=self.add_ddl).pack(side="left", padx=5)
        
        self.ddl_listbox = tk.Listbox(self.tab_ddl, width=90, height=18, font=("SimHei", 10))
        self.ddl_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        
        btn_frame = ttk.Frame(self.tab_ddl)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_ddl).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_ddl_list).pack(side="left", padx=5)
        
        self.refresh_ddl_list()

    def add_ddl(self):
        date = self.ddl_date.get().strip()
        title = self.ddl_title.get().strip()
        if not date or not title:
            messagebox.showwarning("Error", "Date and task cannot be empty")
            return
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Error", "Incorrect date format. Use YYYY-MM-DD")
            return
        
        self.dorm_helper.add_ddl([date, title])
        self.ddl_date.delete(0, tk.END)
        self.ddl_title.delete(0, tk.END)
        self.ddl_date.insert(0, datetime.date.today().isoformat())
        self.refresh_ddl_list()

    def refresh_ddl_list(self):
        self.ddl_listbox.delete(0, tk.END)
        sorted_ddls = sorted(self.dorm_helper.data['ddls'], key=lambda x: x['date'])
        if not sorted_ddls:
            self.ddl_listbox.insert(tk.END, "No deadlines")
            return
        for idx, ddl in enumerate(sorted_ddls, 1):
            self.ddl_listbox.insert(tk.END, f"[{idx}] {ddl['date']} | {ddl['title']}")

    def delete_ddl(self):
        selected = self.ddl_listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        sorted_ddls = sorted(self.dorm_helper.data['ddls'], key=lambda x: x['date'])
        if not sorted_ddls: return 
        
        ddl_id = sorted_ddls[idx]['id']
        original_idx = next(i for i, d in enumerate(self.dorm_helper.data['ddls']) if d['id'] == ddl_id)
        self.dorm_helper.data['ddls'].pop(original_idx)
        self.refresh_ddl_list()

    def init_shopping_tab(self):
        input_frame = ttk.Frame(self.tab_shopping)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Item Name:").pack(side="left", padx=5)
        self.shop_item = ttk.Entry(input_frame, width=40)
        self.shop_item.pack(side="left", padx=5)
        
        ttk.Button(input_frame, text="Add", command=self.add_shopping_item).pack(side="left", padx=5)
        
        self.shop_listbox = tk.Listbox(self.tab_shopping, width=90, height=18, font=("SimHei", 10))
        self.shop_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        
        btn_frame = ttk.Frame(self.tab_shopping)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_shopping_item).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_shopping_list).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_shopping_list).pack(side="left", padx=5)
        
        self.refresh_shopping_list()

    def add_shopping_item(self):
        item = self.shop_item.get().strip()
        if not item:
            return
        self.dorm_helper.shop_add([item])
        self.shop_item.delete(0, tk.END)
        self.refresh_shopping_list()

    def refresh_shopping_list(self):
        self.shop_listbox.delete(0, tk.END)
        shopping_data = self.dorm_helper.data['shopping']
        if not shopping_data:
            self.shop_listbox.insert(tk.END, "List is empty")
            return
        
        sorted_items = sorted(shopping_data.items(), key=lambda x: x[0])
        for idx, (item_name, count) in enumerate(sorted_items, 1):
            self.shop_listbox.insert(tk.END, f"[{idx}] {item_name} x {count}")

    def delete_shopping_item(self):
        selected = self.shop_listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        shopping_data = self.dorm_helper.data['shopping']
        if "List is empty" in self.shop_listbox.get(0):
            return
        
        item_line = self.shop_listbox.get(idx)
        item_name = item_line.split(" x ")[0].split("] ")[1]
        del shopping_data[item_name]
        self.refresh_shopping_list()

    def clear_shopping_list(self):
        shopping_data = self.dorm_helper.data['shopping']
        if not shopping_data:
            return
        if messagebox.askyesno("Confirm", "Clear all shopping items?"):
            self.dorm_helper.shop_clear()
            self.refresh_shopping_list()

    def update_duty_tab(self):
        for widget in self.tab_duty.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(self.tab_duty)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ttk.Label(frame, text="🧹 Dormitory Duty Roster", font=("SimHei", 14, "bold")).pack(anchor="w", pady=5)
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=5)
        
        duty_frame = ttk.Frame(frame)
        duty_frame.pack(anchor="w", pady=10)
        
        duty_list = self.dorm_helper.data['roster']
        current_duty = duty_list[0] if duty_list else "None"
        
        ttk.Label(duty_frame, text=f"Today's Duty:", font=("SimHei", 12)).pack(anchor="w", pady=3)
        ttk.Label(duty_frame, text=f"   {current_duty}", font=("SimHei", 14, "bold"), foreground="red").pack(anchor="w", pady=2)
        
        ttk.Button(duty_frame, text="Rotate to Next", command=self.rotate_duty, width=15).pack(anchor="w", pady=8)
        
        ttk.Label(duty_frame, text="Full Rotation Order:", font=("SimHei", 12, "bold")).pack(anchor="w", pady=5)
        if not duty_list:
            ttk.Label(duty_frame, text="   No duty personnel", font=("SimHei", 11)).pack(anchor="w")
        else:
            for idx, person in enumerate(duty_list, 1):
                if person == current_duty:
                    ttk.Label(duty_frame, text=f"   [{idx}] {person} (Current)", font=("SimHei", 11, "bold"), foreground="red").pack(anchor="w")
                else:
                    ttk.Label(duty_frame, text=f"   [{idx}] {person}", font=("SimHei", 11)).pack(anchor="w")

        ttk.Button(frame, text="Edit Duty Personnel", command=self.edit_duty_roster).pack(anchor="w", padx=10, pady=10)

    def rotate_duty(self):
        duty_list = self.dorm_helper.data['roster']
        if len(duty_list) < 2:
            messagebox.showwarning("Warning", "At least 2 people required to rotate")
            return
        current = duty_list.pop(0)
        duty_list.append(current)
        self.update_duty_tab()
        self.update_reminder_tab()

    def edit_duty_roster(self):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Duty Personnel")
        edit_win.geometry("400x350")
        
        ttk.Label(edit_win, text="Please enter duty personnel (one per line):", font=("SimHei", 10)).pack(pady=10)
        
        text_area = tk.Text(edit_win, width=40, height=10, font=("SimHei", 10))
        text_area.pack(padx=20, pady=5)
        
        current_roster = self.dorm_helper.data['roster']
        if current_roster:
            text_area.insert("1.0", "\n".join(current_roster))
            
        def save_roster():
            content = text_area.get("1.0", tk.END).strip()
            new_roster = [name.strip() for name in content.split("\n") if name.strip()]
            
            if not new_roster:
                messagebox.showwarning("Error", "List cannot be empty", parent=edit_win)
                return
            
            self.dorm_helper.data['roster'] = new_roster
            self.update_duty_tab()
            self.update_reminder_tab()
            edit_win.destroy()

        btn_frame = ttk.Frame(edit_win)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="OK", command=save_roster).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=edit_win.destroy).pack(side="left", padx=10)

    def sync_data(self):
        if self.dorm_helper._git_command(['pull', '--rebase']):
            self.dorm_helper.data = self.load_data()
            self.refresh_all_tabs()
            messagebox.showinfo("Success", "Data synced")
        else:
            messagebox.showerror("Failed", "Sync failed. Check network or git setup.")

    def save_data(self):
        self.dorm_helper.save_data()
        self.dorm_helper.shutdown_sync()
        messagebox.showinfo("Success", "Data saved and synced")

    def show_help(self):
        help_text = "Dormitory Helper Guide:\n\n1. Duty: Click Rotate to switch. Edit to change names.\n2. Shopping: Add items. Duplicates increase count.\n3. Deadlines: Add dates (YYYY-MM-DD).\n4. Data saves automatically on exit."
        messagebox.showinfo("Help", help_text)

    def quit_app(self):
        if messagebox.askyesno("Exit", "Exit Dormitory Helper?"):
            self.dorm_helper.save_data()
            self.dorm_helper.shutdown_sync()
            self.root.destroy()

    def refresh_all_tabs(self):
        self.update_reminder_tab()
        self.refresh_ddl_list()
        self.refresh_shopping_list()
        self.update_duty_tab()

    def load_data(self):
        return self.dorm_helper.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = DormHelperGUI(root)
    root.mainloop()