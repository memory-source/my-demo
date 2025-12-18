# my-demo# **🏠 Dorm Helper \- User Manual**

## **1\. Prerequisites**

Before using the Dorm Helper, ensure you have the following installed on your computer:

1. **Python** (3.6 or higher): [Download Here](https://www.python.org/downloads/)  
2. **Git**: [Download Here](https://www.google.com/search?q=https://git-scm.com/downloads)

**⚠️ Important:** When installing Git on Windows, make sure to select **"Use Git from the Windows Command Prompt"** during the setup process so the Python script can find it.

## **2\. Initial Setup (One-time only)**

Since this tool uses Git to sync data between roommates, you need to set up a shared repository first.

### **Step A: Create a Remote Repository**

1. Go to **GitHub** (or GitLab/Gitee).  
2. Create a **New Repository**.  
3. Name it dorm-helper-data (or similar).  
4. Select **Private** (to keep your data safe).  
5. Check "Add a README file" (this initializes the repo).  
6. Create the repository and copy the **HTTPS URL** (e.g., https://github.com/YourUsername/dorm-helper-data.git).

### **Step B: Clone to Your Computer**

1. Open your command prompt (CMD or Terminal).  
2. Navigate to where you want to store the project.  
3. Run the clone command:  
   git clone \[https://github.com/YourUsername/dorm-helper-data.git\](https://github.com/YourUsername/dorm-helper-data.git)

4. Enter the newly created folder:  
   cd dorm-helper-data

### **Step C: Add the Script**

1. Copy the dorm\_helper.py file (the code provided previously) into this folder.  
2. (Optional) Create a .gitignore file to ignore unnecessary files:  
   \_\_pycache\_\_/  
   \*.pyc

## **3\. How to Run**

1. Open your terminal inside the project folder.  
2. Run the script:  
   python dorm\_helper.py

### **What happens on startup?**

* The tool will automatically try to **Sync (Pull)** data from the cloud.  
* If it's your first time opening it today, you will see a **Daily Reminder** (Duty, Deadlines).

## **4\. Command Reference**

Once the tool is running (Dorm) \>, you can use these commands:

| Feature | Command | Example | Description |
| :---- | :---- | :---- | :---- |
| **Deadlines** | add | add 2023-12-25 Math Final | Adds a new deadline. |
|  | list | list or list Math | Shows all tasks or searches for "Math". |
|  | delete | delete 1 | Deletes the task at index \#1 (check list first). |
| **Shopping** | shop add | shop add Toilet Paper | Adds item. Merges count if it already exists. |
|  | shop list | shop list | Shows current shopping list with quantities. |
|  | shop clear | shop clear | Clears the entire list (after buying). |
| **Duty** | duty | duty | Shows who is on duty today. |
|  | duty next | duty next | Rotates to the next person and updates the date. |
| **System** | save | save | Saves data locally and syncs to cloud. |
|  | quit | quit | Saves, Syncs (Push), and closes the app. |
|  | help | help | Shows this list of commands. |

## **5\. Synchronization Workflow**

The sync magic happens automatically:

1. **Start:** The app runs git pull \--rebase. This downloads any changes your roommates made while you were away.  
2. **Edit:** You add a deadline or update the shopping list. The app marks the data as "Dirty" (Modified).  
3. **Exit:** When you type quit, the app detects the changes and automatically runs:  
   * git add dorm\_data.json  
   * git commit \-m "Update..."  
   * git push

**Note:** If you are offline, the app will skip the sync and just save locally. You can sync later by running the app again when you have internet.

## **6\. Troubleshooting**

**Q: "Git command not found" error?**

* **Fix:** You need to install Git and add it to your System PATH variables. Reinstall Git and check the "Add to PATH" option.

**Q: Sync failed / Conflict detected?**

* **Fix:** This happens if two people edit the same data at the exact same time.  
* Close the Python script.  
* Run git pull manually in your terminal to see the error.  
* If there is a conflict, edit dorm\_data.json to fix it, then commit and push manually.

**Q: Authentication failed during Push?**

* **Fix:** Ensure your computer remembers your GitHub passwords/tokens. You might need to set up a "Credential Helper" or use SSH keys.
