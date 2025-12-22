# 🏠 Dormitory Helper

**Dormitory Helper** is a lightweight, all-in-one desktop application designed to help roommates manage shared responsibilities. It tracks duty rosters, shopping lists, and academic deadlines, with built-in cloud synchronization capabilities using Git.

## ✨ Features

* **🧹 Duty Roster Management**
    * **Auto-Rotation**: Rotates duty personnel to the next person with a single click.
    * **Visual Highlighting**: Clearly highlights the current person on duty in red.
    * **Custom Order**: Allows editing of the full roster order (names are entered one per line).
* **🛒 Shared Shopping List**
    * **Smart Adding**: Automatically increments quantities for duplicate items (e.g., adding "Milk" twice sets the count to 2).
    * **Management**: easy removal of individual items or clearing of the entire list.
* **📅 Deadline Tracker**
    * **Organization**: Tracks tasks with dates (YYYY-MM-DD) and automatically sorts them by urgency.
    * **Dashboard**: Displays the top 3 upcoming deadlines on the main reminder tab.
* **🔔 Daily Reminder**
    * A startup dashboard showing today's duty, urgent deadlines, and the shopping list at a glance.
* **☁️ Cloud Sync**
    * **Git Integration**: Built-in logic to sync data between roommates' computers using Git commands (`pull` on startup, `push` on exit).

## 📂 File Description

* **`dorm_helper_gui.exe`**: The main executable application. Run this to start the program.
* **`dorm_data.json`**: The database file storing your roster, shopping list, and deadlines. **Do not delete this** unless you want to reset data.
* **`dorm_helper_gui.py`**: The frontend source code (GUI).
* **`dorm_assistant.py`**: The backend source code (Logic).

## 🚀 Usage Instructions

1.  **Run the App**: Double-click `dorm_helper_gui.exe`.
2.  **Data Persistence**: Ensure `dorm_helper_gui.exe` and `dorm_data.json` are always in the same folder. The app saves data automatically upon exit.
3.  **Editing Roster**: Go to the "Duty Roster" tab and click "Edit Duty Personnel". Enter names one per line in the pop-up window.

## ☁️ How to Set Up Sync (Optional)

The application attempts to sync data using Git automatically. For this to work:

1.  **Git Required**: Ensure Git is installed on your computer.
2.  **Repository Setup**: The folder containing the application must be a valid Git repository connected to a remote server (like GitHub).
3.  **Automatic Behavior**:
    * **On Startup**: The app runs `git pull --rebase` to fetch the latest changes from roommates.
    * **On Exit**: The app runs `git add`, `git commit`, and `git push` to upload your changes.

*If Git is not configured, the app will function normally in "Offline Mode".*

## 🛠️ Developer Notes

If you wish to modify the source code and rebuild the executable:

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2.  Build the executable:
    ```bash
    python -m PyInstaller --onefile --windowed dorm_helper_gui.py
    ```