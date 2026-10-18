#!/usr/bin/env python3
"""
Beautiful Console To-Do List App
Stores tasks in a local JSON file so your list persists between runs.
"""

import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

# ---------- Colors ----------
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


# ---------- Data ----------
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


# ---------- UI Helpers ----------
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(f"{C.CYAN}{C.BOLD}")
    print("╔══════════════════════════════════════╗")
    print("║         ✦  M Y   T O - D O  ✦         ║")
    print("╚══════════════════════════════════════╝")
    print(f"{C.RESET}")


def divider():
    print(f"{C.DIM}────────────────────────────────────────{C.RESET}")


def menu():
    print(f"{C.YELLOW}{C.BOLD} [1]{C.RESET} Add task")
    print(f"{C.YELLOW}{C.BOLD} [2]{C.RESET} View tasks")
    print(f"{C.YELLOW}{C.BOLD} [3]{C.RESET} Mark task done")
    print(f"{C.YELLOW}{C.BOLD} [4]{C.RESET} Delete task")
    print(f"{C.YELLOW}{C.BOLD} [5]{C.RESET} Edit task")
    print(f"{C.YELLOW}{C.BOLD} [6]{C.RESET} Clear completed")
    print(f"{C.YELLOW}{C.BOLD} [0]{C.RESET} Exit")
    divider()


def priority_color(p):
    return {"High": C.RED, "Medium": C.YELLOW, "Low": C.GREEN}.get(p, C.WHITE)


def show_tasks(tasks):
    clear()
    banner()
    if not tasks:
        print(f"{C.DIM}  No tasks yet — add one to get started!{C.RESET}\n")
        return

    print(f"{C.BOLD}{'#':<4}{'Status':<8}{'Priority':<10}{'Task':<28}{'Added'}{C.RESET}")
    divider()
    for i, t in enumerate(tasks, 1):
        status = f"{C.GREEN}✔ Done{C.RESET}" if t["done"] else f"{C.RED}✘ Todo{C.RESET}"
        pcolor = priority_color(t.get("priority", "Medium"))
        pr = f"{pcolor}{t.get('priority','Medium')}{C.RESET}"
        title = t["title"]
        if t["done"]:
            title = f"{C.DIM}{title}{C.RESET}"
        print(f"{i:<4}{status:<17}{pr:<19}{title:<28}{C.DIM}{t.get('added','')}{C.RESET}")
    divider()
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    print(f"{C.CYAN}  {done}/{total} completed{C.RESET}\n")


def pause():
    input(f"{C.DIM}\nPress Enter to continue...{C.RESET}")


def get_index(tasks, prompt):
    show_tasks(tasks)
    if not tasks:
        pause()
        return None
    try:
        idx = int(input(f"{C.BLUE}{prompt}{C.RESET} ")) - 1
        if 0 <= idx < len(tasks):
            return idx
        print(f"{C.RED}Invalid task number.{C.RESET}")
    except ValueError:
        print(f"{C.RED}Please enter a valid number.{C.RESET}")
    pause()
    return None


# ---------- Actions ----------
def add_task(tasks):
    clear()
    banner()
    title = input(f"{C.BLUE}Task description: {C.RESET}").strip()
    if not title:
        print(f"{C.RED}Task can't be empty.{C.RESET}")
        pause()
        return

    print(f"{C.BLUE}Priority:{C.RESET} 1) {C.RED}High{C.RESET}  2) {C.YELLOW}Medium{C.RESET}  3) {C.GREEN}Low{C.RESET}")
    choice = input("Choose [1-3, default 2]: ").strip()
    priority = {"1": "High", "2": "Medium", "3": "Low"}.get(choice, "Medium")

    tasks.append({
        "title": title,
        "priority": priority,
        "done": False,
        "added": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_tasks(tasks)
    print(f"{C.GREEN}✔ Task added!{C.RESET}")
    pause()


def mark_done(tasks):
    idx = get_index(tasks, "Enter task number to mark done:")
    if idx is not None:
        tasks[idx]["done"] = True
        save_tasks(tasks)
        print(f"{C.GREEN}✔ Marked as done!{C.RESET}")
        pause()


def delete_task(tasks):
    idx = get_index(tasks, "Enter task number to delete:")
    if idx is not None:
        removed = tasks.pop(idx)
        save_tasks(tasks)
        print(f"{C.RED}✘ Deleted: {removed['title']}{C.RESET}")
        pause()


def edit_task(tasks):
    idx = get_index(tasks, "Enter task number to edit:")
    if idx is not None:
        new_title = input(f"{C.BLUE}New description (leave blank to keep): {C.RESET}").strip()
        if new_title:
            tasks[idx]["title"] = new_title
        save_tasks(tasks)
        print(f"{C.GREEN}✔ Task updated!{C.RESET}")
        pause()


def clear_completed(tasks):
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    save_tasks(tasks)
    print(f"{C.GREEN}✔ Removed {before - len(tasks)} completed task(s).{C.RESET}")
    pause()


# ---------- Main Loop ----------
def main():
    tasks = load_tasks()
    while True:
        clear()
        banner()
        menu()
        choice = input(f"{C.MAGENTA}Choose an option: {C.RESET}").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
            pause()
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            clear_completed(tasks)
        elif choice == "0":
            clear()
            print(f"{C.CYAN}Goodbye, Nivetha! ✦{C.RESET}")
            break
        else:
            print(f"{C.RED}Invalid option.{C.RESET}")
            pause()


if __name__ == "__main__":
    main()