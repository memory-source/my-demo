import json
import os
import subprocess
import datetime

# Data file path
DATA_FILE = "dorm_data.json"

# Default data (auto-generated on first run)
DEFAULT_DATA = {
    "config": {
        "last_opened": ""
    },
    "roster": ["Zhang San", "Li Si", "Wang Wu", "Zhao Liu"],  # Default duty personnel (can be modified manually)
    "ddls": [],
    "shopping": {}
}

class DormHelper:
    def __init__(self):
        self.data = self.load_data()
        self.check_daily_reminder()

    # Load data (create default data if file doesn't exist)
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Data file corrupted, using default data")
                return DEFAULT_DATA.copy()
        else:
            print("📁 Data file not found, creating default data")
            return DEFAULT_DATA.copy()

    # Save data to file
    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print("✅ Local data saved")

    # Git command execution (sync function)
    def _git_command(self, args):
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=True
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    # Sync data on startup
    def startup_sync(self):
        print("🌐 Syncing with cloud...")
        if self._git_command(["pull", "--rebase"]):
            print("✅ Sync successful!")
            self.data = self.load_data()  # Reload data after sync
            return True
        else:
            print("⚠️ Sync failed (Offline or Git error). Using local data.")
            return False

    # Sync data on shutdown
    def shutdown_sync(self):
        if self._git_command(["add", DATA_FILE]):
            today = datetime.date.today().isoformat()
            self._git_command(["commit", "-m", f"Update data {today}"])
            self._git_command(["push"])
            print("✅ Cloud sync completed")

    # Daily reminder logic
    def check_daily_reminder(self):
        today = datetime.date.today().isoformat()
        if self.data["config"]["last_opened"] != today:
            self.data["config"]["last_opened"] = today
            self.save_data()

    # --------------------------
    # Deadline Functions
    # --------------------------
    def add_ddl(self, args):
        if len(args) < 2:
            print("❌ Format error! Example: add 2025-12-25 Final English Exam")
            return
        date_str, title = args[0], " ".join(args[1:])
        # Simple date format validation
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("❌ Date format error! Please use YYYY-MM-DD")
            return
        # Add to list
        self.data["ddls"].append({
            "id": len(self.data["ddls"]) + 1,
            "date": date_str,
            "title": title
        })
        print(f"✅ Added deadline: {date_str} - {title}")

    def list_ddls(self, args):
        query = " ".join(args) if args else ""
        sorted_ddls = sorted(self.data["ddls"], key=lambda x: x["date"])
        print("\n📅 Deadline list:")
        if not sorted_ddls:
            print("   (No deadlines)")
            return
        for idx, ddl in enumerate(sorted_ddls, 1):
            if query in ddl["title"] or query in ddl["date"]:
                print(f"   [{idx}] {ddl['date']} | {ddl['title']}")

    def delete_ddl(self, args):
        if len(args) < 1:
            print("❌ Format error! Example: delete 1")
            return
        try:
            idx = int(args[0]) - 1  # Convert to list index
            if 0 <= idx < len(self.data["ddls"]):
                deleted = self.data["ddls"].pop(idx)
                print(f"✅ Deleted: {deleted['date']} - {deleted['title']}")
            else:
                print("❌ Index does not exist!")
        except ValueError:
            print("❌ Please enter a numeric index!")

    # --------------------------
    # Shopping List Functions
    # --------------------------
    def shop_add(self, args):
        if len(args) < 1:
            print("❌ Format error! Example: shop add Toilet Paper")
            return
        item = args[0]
        if item in self.data["shopping"]:
            self.data["shopping"][item] += 1
        else:
            self.data["shopping"][item] = 1
        print(f"✅ Added [{item}] to shopping list (current quantity: {self.data['shopping'][item]})")

    def shop_list(self, args):
        print("\n🛒 Shopping list:")
        if not self.data["shopping"]:
            print("   (No items)")
            return
        for idx, (item, count) in enumerate(self.data["shopping"].items(), 1):
            print(f"   [{idx}] {item} × {count}")

    def shop_clear(self):
        self.data["shopping"].clear()
        print("✅ Shopping list cleared")

    # --------------------------
    # Duty Roster Functions
    # --------------------------
    def duty_list(self):
        print("\n🧹 Duty roster:")
        if not self.data["roster"]:
            print("   (No duty personnel)")
            return
        print(f"   Current duty: {self.data['roster'][0]}")
        print("   Rotation order:")
        for idx, person in enumerate(self.data["roster"], 1):
            print(f"      [{idx}] {person}")

    def duty_next(self):
        if len(self.data["roster"]) < 2:
            print("❌ At least 2 duty personnel are required to rotate!")
            return
        current = self.data["roster"].pop(0)
        self.data["roster"].append(current)
        print(f"✅ Duty rotated, current duty: {self.data['roster'][0]}")

    # --------------------------
    # Help Information
    # --------------------------
    def show_help(self):
        help_text = """
📚 Dormitory Helper Command Instructions:
【Deadline Management】
  add <date(YYYY-MM-DD)> <task>  - Add deadline (Example: add 2025-12-25 Term Paper)
  list [keyword]                  - View/search deadlines (Example: list paper)
  delete <index>                  - Delete deadline (Example: delete 1)

【Shopping List Management】
  shop add <item>                - Add item to shopping list (Example: shop add Laundry Detergent)
  shop list                      - View shopping list
  shop clear                     - Clear shopping list

【Duty Roster Management】
  duty list                      - View duty order
  duty next                      - Rotate to next duty person

【Data Sync】
  save                           - Save and sync data to cloud
  quit                           - Save data and exit program
  help                           - View help information
        """
        print(help_text)

# Command line entry point
if __name__ == "__main__":
    helper = DormHelper()
    helper.startup_sync()  # Startup sync

    # Welcome message
    today = datetime.date.today().isoformat()
    print("=" * 50)
    print(f"🏠 Dorm Helper | {today}")
    print("=" * 50)
    print("🔔 [Daily Reminder]")
    print(f"🧹 Duty Today: {helper.data['roster'][0] if helper.data['roster'] else 'None'}")
    print("📅 Upcoming Deadlines:")
    sorted_ddls = sorted(helper.data["ddls"], key=lambda x: x["date"])[:3]
    if sorted_ddls:
        for ddl in sorted_ddls:
            print(f"   - {ddl['date']} : {ddl['title']}")
    else:
        print("   (None)")
    print("-" * 50)

    # Command loop
    while True:
        try:
            cmd = input("(Dorm) > ").strip().split()
            if not cmd:
                continue
            # Parse command
            if cmd[0] == "add":
                helper.add_ddl(cmd[1:])
            elif cmd[0] == "list":
                helper.list_ddls(cmd[1:])
            elif cmd[0] == "delete":
                helper.delete_ddl(cmd[1:])
            elif cmd[0] == "shop":
                if len(cmd) < 2:
                    print("❌ Format error! Example: shop add Toilet Paper / shop list")
                    continue
                if cmd[1] == "add":
                    helper.shop_add(cmd[2:])
                elif cmd[1] == "list":
                    helper.shop_list(cmd[2:])
                elif cmd[1] == "clear":
                    helper.shop_clear()
                else:
                    print("❌ Unknown subcommand! Supported: shop add / list / clear")
            elif cmd[0] == "duty":
                if len(cmd) < 2:
                    helper.duty_list()
                elif cmd[1] == "next":
                    helper.duty_next()
                elif cmd[1] == "list":
                    helper.duty_list()
                else:
                    print("❌ Unknown subcommand! Supported: duty list / next")
            elif cmd[0] == "save":
                helper.save_data()
                helper.shutdown_sync()
            elif cmd[0] == "quit":
                helper.save_data()
                helper.shutdown_sync()
                print("👋 Goodbye!")
                break
            elif cmd[0] == "help":
                helper.show_help()
            else:
                print("❌ Unknown command! Enter help to view supported commands")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            helper.save_data()
            helper.shutdown_sync()
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")