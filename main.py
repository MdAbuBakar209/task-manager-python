from colorama import Fore, Style, init
init(autoreset=True, convert=True)

import json

# Load tasks
try:
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
except:
    tasks = []

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

# 🔥 UI FUNCTIONS
def print_header():
    print(Fore.CYAN + "=" * 45)
    print(Style.BRIGHT + "           TASK MANAGER CLI APP")
    print(Fore.CYAN + "=" * 45 + Style.RESET_ALL)

def print_menu():
    print_header()
    print(Fore.YELLOW + "\n📌 MENU" + Style.RESET_ALL)
    print("1. ➕ Add Task")
    print("2. 📋 View All Tasks")
    print("3. ⏳ Pending Tasks")
    print("4. ✅ Completed Tasks")
    print("5. ✔ Mark Task as Done")
    print("6. ❌ Delete Task")
    print("7. 🧹 Clear All Tasks")
    print("8. 🔄 Undo Task")
    print("9. 🚀 Mark ALL Done")
    print("10. 🚪 Exit")
    print("-" * 45)

def show_tasks(title, condition=None):
    print(Fore.CYAN + f"\n--- {title} ---" + Style.RESET_ALL)
    found = False

    for i, t in enumerate(tasks, start=1):
        if condition is None or condition(t):
            status = Fore.GREEN + "✔ DONE" if t["done"] else Fore.RED + "❌ PENDING"
            print(f"{i}. {t['task']} [{status}{Style.RESET_ALL}]")
            found = True

    if not found:
        print(Fore.YELLOW + "⚠ No tasks found." + Style.RESET_ALL)

# 🔁 MAIN LOOP
while True:
    print_menu()

    choice = input("Enter your choice: ")

    if choice not in ["1","2","3","4","5","6","7","8","9","10"]:
        print(Fore.RED + "❌ Invalid choice! Enter 1-10." + Style.RESET_ALL)
        continue

    # ADD TASK
    if choice == "1":
        task = input("Enter task: ").strip()

        if any(t["task"].lower() == task.lower() for t in tasks):
            print(Fore.YELLOW + "⚠ WARNING: Task already exists!" + Style.RESET_ALL)
            continue

        tasks.append({"task": task, "done": False})
        save_tasks()
        print(Fore.GREEN + "✔ Task added successfully!" + Style.RESET_ALL)

    # VIEW ALL
    elif choice == "2":
        if not tasks:
            print(Fore.CYAN + "🎉 You are all caught up!" + Style.RESET_ALL)
        else:
            show_tasks("ALL TASKS")

    # PENDING
    elif choice == "3":
        show_tasks("PENDING TASKS", lambda t: not t["done"])

    # COMPLETED
    elif choice == "4":
        show_tasks("COMPLETED TASKS", lambda t: t["done"])

    # MARK DONE
    elif choice == "5":
        if not tasks:
            print(Fore.YELLOW + "⚠ No tasks available." + Style.RESET_ALL)
        else:
            show_tasks("MARK TASK AS DONE")
            try:
                index = int(input("Enter task number: ")) - 1
                if index < 0 or index >= len(tasks):
                    print(Fore.RED + "❌ Invalid number!" + Style.RESET_ALL)
                    continue

                tasks[index]["done"] = True
                save_tasks()
                print(Fore.GREEN + "✔ Task marked as completed!" + Style.RESET_ALL)
            except:
                print(Fore.RED + "❌ Invalid input!" + Style.RESET_ALL)

    # DELETE TASK
    elif choice == "6":
        if not tasks:
            print(Fore.YELLOW + "⚠ No tasks to delete." + Style.RESET_ALL)
        else:
            show_tasks("DELETE TASK")
            try:
                index = int(input("Enter task number: ")) - 1
                if index < 0 or index >= len(tasks):
                    print(Fore.RED + "❌ Invalid number!" + Style.RESET_ALL)
                    continue

                removed = tasks.pop(index)
                save_tasks()
                print(Fore.RED + f"❌ Deleted: {removed['task']}" + Style.RESET_ALL)
            except:
                print(Fore.RED + "❌ Invalid input!" + Style.RESET_ALL)

    # CLEAR ALL
    elif choice == "7":
        if not tasks:
            print(Fore.YELLOW + "⚠ No tasks to clear." + Style.RESET_ALL)
        else:
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == "yes":
                tasks.clear()
                save_tasks()
                print(Fore.GREEN + "🧹 All tasks cleared!" + Style.RESET_ALL)
            else:
                print("Cancelled.")

    # UNDO TASK
    elif choice == "8":
        show_tasks("UNDO TASK", lambda t: t["done"])
        try:
            index = int(input("Enter task number to undo: ")) - 1
            if index < 0 or index >= len(tasks):
                print(Fore.RED + "❌ Invalid number!" + Style.RESET_ALL)
                continue

            tasks[index]["done"] = False
            save_tasks()
            print(Fore.GREEN + "🔄 Task marked as pending!" + Style.RESET_ALL)
        except:
            print(Fore.RED + "❌ Invalid input!" + Style.RESET_ALL)

    # MARK ALL DONE
    elif choice == "9":
        if not tasks:
            print(Fore.YELLOW + "⚠ No tasks available." + Style.RESET_ALL)
        else:
            for t in tasks:
                t["done"] = True
            save_tasks()
            print(Fore.GREEN + "🚀 All tasks marked as DONE!" + Style.RESET_ALL)

    # EXIT
    elif choice == "10":
        save_tasks()
        print(Fore.CYAN + "💾 Tasks saved. Exiting..." + Style.RESET_ALL)
        break