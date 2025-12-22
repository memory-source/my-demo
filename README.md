Dormitory Helper - 宿舍管理工具 🏠
A lightweight, user-friendly dormitory management tool with both Command Line Interface (CLI) and Graphical User Interface (GUI). Designed for students to track deadlines, manage shopping lists, and rotate duty rosters—with cloud sync via Git!
Features ✨
Function	Description
Deadline Tracker	Add, view, and delete upcoming tasks (e.g., exams, assignments) with dates
Shopping List	Manage shared dorm items (auto-increment quantities for duplicates)
Duty Roster	Rotate daily cleaning duties and edit the personnel list
Cloud Sync	Sync data across devices using Git (auto-save on exit)
Dual Interface	Use CLI for quick commands or GUI for visual management
Screenshots 📸
GUI Interface

image
(Replace with actual screenshot after setup: show the 4 tabs + main features)
CLI Interface
plaintext
🏠 Dorm Helper | 2025-12-25
==================================================
🔔 [Daily Reminder]
🧹 Duty Today: Zhang San
📅 Upcoming Deadlines:
   - 2025-12-25 : Final English Exam
   - 2025-12-30 : Term Paper Submission
--------------------------------------------------
(Dorm) > help
📚 Dormitory Helper Command Instructions:
...
Prerequisites 📋
Before running the tool, ensure you have:
Python 3.8+ installed (download from python.org)
Git installed (for cloud sync: git-scm.com)
A GitHub/GitLab repository (to sync dorm_data.json across devices)
Install Dependencies
No external Python packages required! The tool uses only built-in libraries:
tkinter (for GUI, included with standard Python installations)
json/os/subprocess (for data handling and Git sync)
Installation 🚀
1. Clone the Repository
bash
运行
git clone https://github.com/your-username/dormitory-helper.git
cd dormitory-helper
2. (Optional) Configure Git Sync
To enable cloud sync (share data with roommates):
Create a new Git repository (e.g., on GitHub)
Initialize Git in the project folder:
bash
运行
git init
git remote add origin https://github.com/your-username/your-repo-name.git
git add .
git commit -m "Initial commit"
git push -u origin main
Share the repo with your roommates—everyone can pull/push updates automatically!
How to Use 🎯
Run the GUI (Recommended for Beginners)
bash
运行
python dorm_helper_gui.py
GUI Tabs Guide:
Daily Reminder: Quick overview of today’s duty, upcoming deadlines, and shopping list items.
Deadlines: Add tasks with dates, delete selected items, or refresh the list.
Shopping List: Add shared items, delete individual entries, or clear the entire list.
Duty Roster: View the rotation order, rotate to the next person, or edit the personnel list.
Run the CLI (For Power Users)
bash
运行
python dorm_assistant.py
CLI Commands Cheat Sheet:
Command	Action
add 2025-12-25 Final English Exam	Add a deadline
list	View all deadlines
list paper	Search deadlines containing "paper"
delete 1	Delete the 1st deadline in the list
shop add Toilet Paper	Add an item to the shopping list
shop list	View the shopping list
shop clear	Clear all shopping list items
duty list	View the duty roster
duty next	Rotate to the next duty person
save	Save and sync data to the cloud
help	Show command instructions
quit	Save data and exit
Data Management 📂
All data is stored in dorm_data.json (auto-generated on first run)
Data structure:
json
{
  "config": {"last_opened": "2025-12-25"},
  "roster": ["Zhang San", "Li Si", "Wang Wu", "Zhao Liu"],
  "ddls": [{"id": 1, "date": "2025-12-25", "title": "Final English Exam"}],
  "shopping": {"Toilet Paper": 2, "Laundry Detergent": 1}
}
Backup Warning: Never manually edit dorm_data.json while the app is running—this may corrupt data.
If data is corrupted: Delete dorm_data.json and restart the app (default data will be regenerated).
