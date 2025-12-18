import json
import os
import sys
import datetime
import subprocess

# --- Configuration & Constants ---
DATA_FILE = "dorm_data.json"
DEFAULT_DATA = {
    "config": {
        "lights_out": "23:00",
        "last_opened": ""  # Tracks the last date opened for daily reminders
    },
    "roster": ["Roommate A", "Roommate B", "Roommate C", "Roommate D"],
    "ddls": [],   # Format: {"title": str, "date": "YYYY-MM-DD", "id": int}
    "shopping": {} # Format: {"Item Name": Quantity}
}

class DormHelper:
    def __init__(self):
        # 1. Sync Logic: Try to pull from cloud first
        self.startup_sync()
        
        # 2. Load Data
        self.data = self.load_data()
        self.dirty = False  # Marks if data has been modified

    def load_data(self):
        """Load data from JSON. If not found, use default."""
        if not os.path.exists(DATA_FILE):
            return DEFAULT_DATA.copy()
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return DEFAULT_DATA.copy()

    def save_data(self):
        """Save memory data to JSON file."""
        if self.dirty:
            try:
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    # ensure_ascii=False allows non-English characters if needed
                    json.dump(self.data, f, ensure_ascii=False, indent=4)
                print(">>> Local data saved.")
                # Note: We do not set self.dirty = False here because we need it for Push
            except Exception as e:
                print(f"Error saving data: {e}")

    # --- Git Sync Module ---

    def _git_command(self, args):
        """Helper to run system Git commands."""
        try:
            # check=False allows us to handle errors manually without crashing
            result = subprocess.run(
                ['git'] + args,
                capture_output=True, text=True, check=False,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            return result.returncode == 0
        except FileNotFoundError:
            print("⚠️  Git not installed. Running in local mode.")
            return False
        except Exception:
            return False

    def startup_sync(self):
        """Pull latest changes on startup."""
        print("🌐 Syncing with cloud...")
        if self._git_command(['pull', '--rebase']):
            print("✅ Data is up to date.")
        else:
            print("⚠️ Sync failed (Offline or Git error). Using local data.")

    def shutdown_sync(self):
        """Push changes on exit if data was modified."""
        if not self.dirty:
            return

        print("\n💾 Committing changes to cloud...")
        self._git_command(['add', DATA_FILE])
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        commit_msg = f"Update: {timestamp}"
        
        if self._git_command(['commit', '-m', commit_msg]):
            if self._git_command(['push']):
                print("✅ Push successful.")
                self.dirty = False
            else:
                print("❌ Push failed. Check network or pull latest changes manually.")
        else:
            print("⚠️ Nothing to commit or commit failed.")

    # --- Core Features ---

    def welcome_reminder(self):
        """Show daily summary only once per day."""
        today_str = datetime.date.today().isoformat()
        last_opened = self.data["config"].get("last_opened")
        
        print("="*50)
        print(f"🏠 Dorm Helper | {today_str}")
        print("="*50)

        # Show detailed reminder if first time today
        if last_opened != today_str:
            print("🔔 [Daily Reminder]")
            
            # 1. Duty
            current_duty = self.data['roster'][0] if self.data['roster'] else "None"
            print(f"🧹 Duty Today: {current_duty}")
            
            # 2. Lights Out
            print(f"💡 Lights Out: {self.data['config'].get('lights_out', '23:00')}")
            
            # 3. Top 3 Deadlines
            sorted_ddls = sorted(self.data['ddls'], key=lambda x: x['date'])
            print("📅 Upcoming Deadlines:")
            if not sorted_ddls:
                print("   (None)")
            else:
                for task in sorted_ddls[:3]:
                    print(f"   - {task['date']} : {task['title']}")
            
            # Update config
            self.data["config"]["last_opened"] = today_str
            self.dirty = True
        else:
            print("👋 Welcome back!")
        print("-" * 50)

    def add_ddl(self, args):
        """Command: add <YYYY-MM-DD> <Title>"""
        if len(args) < 2:
            print("Usage: add <YYYY-MM-DD> <Content>")
            return
        date, title = args[0], " ".join(args[1:])
        
        new_id = len(self.data['ddls']) + 1
        self.data['ddls'].append({"id": new_id, "date": date, "title": title})
        
        print(f"✅ Deadline added: [{date}] {title}")
        self.dirty = True

    def list_items(self, args):
        """Command: list [search_term]"""
        query = args[0] if args else ""
        print(f"\n📋 Deadlines (Filter: '{query}'):")
        
        # Sort by date
        sorted_ddls = sorted(self.data['ddls'], key=lambda x: x['date'])
        count = 0
        
        for idx, item in enumerate(sorted_ddls):
            if query.lower() in item['title'].lower() or query in item['date']:
                # Calculate days left
                try:
                    d_date = datetime.datetime.strptime(item['date'], "%Y-%m-%d").date()
                    days_left = (d_date - datetime.date.today()).days
                    status = f"{days_left} days left" if days_left >= 0 else "Expired"
                except ValueError:
                    status = "Invalid Date"
                    
                print(f"[{idx+1}] {item['date']} | {item['title']} ({status})")
                count += 1
        
        if count == 0:
            print("   (Empty)")
        print("")

    def delete_item(self, args):
        """Command: delete <index>"""
        if not args or not args[0].isdigit():
            print("Usage: delete <Index Number> (Use 'list' to see numbers)")
            return
        
        idx = int(args[0]) - 1
        sorted_ddls = sorted(self.data['ddls'], key=lambda x: x['date'])
        
        if 0 <= idx < len(sorted_ddls):
            removed = sorted_ddls.pop(idx)
            self.data['ddls'] = sorted_ddls # Update main list
            print(f"🗑️ Deleted: {removed['title']}")
            self.dirty = True
        else:
            print("❌ Invalid index.")

    def shop_manager(self, args):
        """Command: shop add <item> / shop list"""
        if not args:
            print("Usage: shop list / shop add <Item> / shop clear")
            return

        cmd = args[0].lower()
        
        if cmd == "add":
            if len(args) < 2:
                print("Please specify an item name.")
                return
            item = " ".join(args[1:])
            # Merge Logic: Increment count if exists
            current_qty = self.data['shopping'].get(item, 0)
            self.data['shopping'][item] = current_qty + 1
            print(f"🛒 Added '{item}' (Total: {current_qty + 1})")
            self.dirty = True
            
        elif cmd == "list":
            print("\n🛍️ Shopping List:")
            if not self.data['shopping']:
                print("   (Empty)")
            else:
                for item, qty in self.data['shopping'].items():
                    print(f"   - {item}: {qty}")
            print("")
            
        elif cmd == "clear":
            self.data['shopping'] = {}
            print("🗑️ Shopping list cleared.")
            self.dirty = True

    def duty_manager(self, args):
        """Command: duty list / duty next"""
        if not args:
            print(f"Current Duty: {self.data['roster'][0]}")
            print("Usage: duty list / duty next")
            return
            
        if args[0] == "list":
            print(f"Roster Queue: {' -> '.join(self.data['roster'])}")
            
        elif args[0] == "next":
            # Rotation Logic: Move first to last
            person = self.data['roster'].pop(0)
            self.data['roster'].append(person)
            print(f"🔄 Roster rotated.")
            print(f"👉 Previous: {person}")
            print(f"👉 Now: {self.data['roster'][0]}")
            self.dirty = True

    # --- Main Loop ---
    def run(self):
        self.welcome_reminder()
        
        while True:
            try:
                user_input = input("(Dorm) > ").strip().split()
            except (EOFError, KeyboardInterrupt):
                self.save_data()
                self.shutdown_sync()
                break

            if not user_input:
                continue
            
            cmd = user_input[0].lower()
            args = user_input[1:]

            if cmd in ["quit", "exit"]:
                self.save_data()
                self.shutdown_sync()
                print("Bye!")
                break
            elif cmd == "save":
                self.save_data()
                self.shutdown_sync()
            elif cmd == "add":
                self.add_ddl(args)
            elif cmd == "list":
                self.list_items(args)
            elif cmd == "delete":
                self.delete_item(args)
            elif cmd == "shop":
                self.shop_manager(args)
            elif cmd == "duty":
                self.duty_manager(args)
            elif cmd == "help":
                print("\nCommands:")
                print("  add <date> <task>   : Add Deadline")
                print("  list [query]        : List/Search Deadlines")
                print("  delete <index>      : Remove Deadline")
                print("  shop add <item>     : Add to Shopping List")
                print("  shop list           : View Shopping List")
                print("  duty list / next    : View or Rotate Duty")
                print("  save / quit         : Sync & Exit\n")
            else:
                print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    app = DormHelper()
    app.run()