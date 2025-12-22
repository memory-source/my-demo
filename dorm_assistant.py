import json
import os
import subprocess
import datetime

DATA_FILE = "dorm_data.json"

DEFAULT_DATA = {
    "config": {
        "last_opened": ""
    },
    "roster": ["Zhang San", "Li Si", "Wang Wu", "Zhao Liu"],
    "ddls": [],
    "shopping": {}
}

class DormHelper:
    def __init__(self):
        self.data = self.load_data()
        self.check_daily_reminder()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return DEFAULT_DATA.copy()
        else:
            return DEFAULT_DATA.copy()

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

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

    def startup_sync(self):
        if self._git_command(["pull", "--rebase"]):
            self.data = self.load_data()
            return True
        return False

    def shutdown_sync(self):
        if self._git_command(["add", DATA_FILE]):
            today = datetime.date.today().isoformat()
            self._git_command(["commit", "-m", f"Update data {today}"])
            self._git_command(["push"])

    def check_daily_reminder(self):
        today = datetime.date.today().isoformat()
        if self.data["config"]["last_opened"] != today:
            self.data["config"]["last_opened"] = today
            self.save_data()

    def add_ddl(self, args):
        if len(args) < 2:
            print("Format error. Example: add 2025-12-25 Final Exam")
            return
        date_str, title = args[0], " ".join(args[1:])
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Date format error. Use YYYY-MM-DD")
            return
        
        self.data["ddls"].append({
            "id": len(self.data["ddls"]) + 1,
            "date": date_str,
            "title": title
        })
        print(f"Added deadline: {date_str} - {title}")

    def list_ddls(self, args):
        query = " ".join(args) if args else ""
        sorted_ddls = sorted(self.data["ddls"], key=lambda x: x["date"])
        print("\nDeadline list:")
        if not sorted_ddls:
            print("   (No deadlines)")
            return
        for idx, ddl in enumerate(sorted_ddls, 1):
            if query in ddl["title"] or query in ddl["date"]:
                print(f"   [{idx}] {ddl['date']} | {ddl['title']}")

    def delete_ddl(self, args):
        if len(args) < 1:
            return
        try:
            idx = int(args[0]) - 1
            if 0 <= idx < len(self.data["ddls"]):
                deleted = self.data["ddls"].pop(idx)
                print(f"Deleted: {deleted['date']} - {deleted['title']}")
            else:
                print("Index does not exist")
        except ValueError:
            print("Please enter a number")

    def shop_add(self, args):
        if len(args) < 1:
            return
        item = args[0]
        if item in self.data["shopping"]:
            self.data["shopping"][item] += 1
        else:
            self.data["shopping"][item] = 1
        print(f"Added [{item}] (count: {self.data['shopping'][item]})")

    def shop_list(self, args):
        print("\nShopping list:")
        if not self.data["shopping"]:
            print("   (Empty)")
            return
        for idx, (item, count) in enumerate(self.data["shopping"].items(), 1):
            print(f"   [{idx}] {item} x {count}")

    def shop_clear(self):
        self.data["shopping"].clear()
        print("Shopping list cleared")

    def duty_list(self):
        print("\nDuty roster:")
        if not self.data["roster"]:
            print("   (No personnel)")
            return
        print(f"   Current: {self.data['roster'][0]}")
        print("   Order:")
        for idx, person in enumerate(self.data["roster"], 1):
            print(f"      [{idx}] {person}")

    def duty_next(self):
        if len(self.data["roster"]) < 2:
            print("Need at least 2 people to rotate")
            return
        current = self.data["roster"].pop(0)
        self.data["roster"].append(current)
        print(f"Rotated. Current: {self.data['roster'][0]}")

if __name__ == "__main__":
    helper = DormHelper()
    helper.startup_sync()

    today = datetime.date.today().isoformat()
    print(f"Dorm Helper | {today}")
    
    print(f"Duty Today: {helper.data['roster'][0] if helper.data['roster'] else 'None'}")
    
    sorted_ddls = sorted(helper.data["ddls"], key=lambda x: x["date"])[:3]
    if sorted_ddls:
        print("Upcoming Deadlines:")
        for ddl in sorted_ddls:
            print(f"   - {ddl['date']} : {ddl['title']}")
    
    while True:
        try:
            cmd = input("(Dorm) > ").strip().split()
            if not cmd:
                continue
            
            if cmd[0] == "add":
                helper.add_ddl(cmd[1:])
            elif cmd[0] == "list":
                helper.list_ddls(cmd[1:])
            elif cmd[0] == "delete":
                helper.delete_ddl(cmd[1:])
            elif cmd[0] == "shop":
                if len(cmd) < 2:
                    continue
                if cmd[1] == "add":
                    helper.shop_add(cmd[2:])
                elif cmd[1] == "list":
                    helper.shop_list(cmd[2:])
                elif cmd[1] == "clear":
                    helper.shop_clear()
            elif cmd[0] == "duty":
                if len(cmd) < 2:
                    helper.duty_list()
                elif cmd[1] == "next":
                    helper.duty_next()
                elif cmd[1] == "list":
                    helper.duty_list()
            elif cmd[0] == "save":
                helper.save_data()
                helper.shutdown_sync()
            elif cmd[0] == "quit":
                helper.save_data()
                helper.shutdown_sync()
                break
        except KeyboardInterrupt:
            helper.save_data()
            helper.shutdown_sync()
            break
        except Exception as e:
            print(f"Error: {str(e)}")