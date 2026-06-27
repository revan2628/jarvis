import random
import threading
import webbrowser
import re
import os
from speech import speak
import subprocess
from urllib.parse import quote
import time
import vad

def handle_youtube(query):
    if "youtube" in query:
        phrases = ["Opening it",
                   'certainly',
                   'Opening Youtube',
                   'Done']
        y = False
        patterns = [r"search for (.+?) on youtube",
                    r"search for (.+?) in youtube",
                    r"open youtube and search for (.+)",
                    r"look up (.+?) on youtube"]
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                phrases = ["Searching Youtube",
                           "certainly",
                           "Right away sir"]
                y = True
                speakphrase = random.choice(phrases)
                speak(speakphrase)
                searchfor = match.group(1)
                webbrowser.open(f"https://www.youtube.com/results?search_query={quote(searchfor)}")
                return True
        if not y:
            speakphrase = random.choice(phrases)
            speak(speakphrase)
            webbrowser.open("https://www.youtube.com")
            return True
        return False

def handle_locking(query):
    locks = ["lock my computer",
            "lock the screen",
            "lock yourself",
            "lock screen",
            "lock computer"]
    for lock in locks:
        if lock in query:
            os.system("loginctl lock-session")
            return True
    return False

def handle_source_code(query):
    if "source code" in query:
        current_file = os.path.abspath(__file__)
        subprocess.Popen(["ptyxis",
                          "--new-window",
                          "--",
                          "vim",
                          current_file])
        return True
    return False


def handle_files(query):
    if "find" in query or ("open" in query and ("book" in query or "folder" in query)):
        patterns = [r"open the (.+?) book",
                    r"open the (.+?) folder",
                    r"open (.+?) book",
                    r"find the (.+?) book",
                    r"find the (.+?) folder",
                    r"find and open (.+?) folder",
                    r"find and open the (.+?) book",
                    r"find and open the (.+?) folder",
                    r"where is the (.+?) folder", #doesnt
                    r"where is the (.+?) book",   #really
                    r"where is (.+?)",            #work
                    r"find and open (.+)",
                    r"find (.+)"]
        
        matches  = []
        if "book" in query:
            match = re.search(r"(\w+)\s+book", query)
            book = match.group(1)
            result = subprocess.run(
                    ['locate', '-ib', book],
                    capture_output=True,
                    text=True
                    )
            for path in result.stdout.splitlines():
                name = os.path.splitext(os.path.basename(path))[0].lower()

                if name == book:
                    matches.append(path)
        
        elif "folder" in query:
            match = re.search(r"(\w+)\s+folder", query)
            folder = match.group(1)
            result = subprocess.run(
                    ['locate', '-ib', folder],
                    capture_output=True,
                    text=True
                    )
            for path in result.stdout.splitlines():
                if os.path.isdir(path):
                    if os.path.basename(path).lower() == folder:
                        matches.append(path)

        else:
            for pattern in patterns:
                match = re.search(pattern, query)
                if match:
                    file = match.group(1)
                    result = subprocess.run(
                            ['locate', '-ib', file],
                            capture_output=True,
                            text=True
                            )
            matches  = result.stdout.splitlines()

        if matches:
            yesspeech = ["certainly sir",
                         "consider it done",
                         "done sir",
                         "It is ready when you are sir"]
            subprocess.run(["xdg-open", matches[0]])
            print(matches[0])
            speak(random.choice(yesspeech))
            return True
        else:
            failspeech = ["File not found sir",
                          "unable to locate the file sir",
                          "search concluded, no matching file or folder"]
            speak(random.choice(failspeech)) 
            return True
    return False

def handle_show_tasks(query):
    todocommands = ["show my tasks list",
                    "show my todo list",
                    "show tasks list",
                    "show todo list",
                    "show the tasks list",
                    "show the todo list",
                    "what are my tasks",
                    "what else do i have to do",
                    "what else do i need to do",
                    "show my tasks"]
    for showcommand in todocommands:
        if showcommand in query:
            taskspaths = subprocess.run(
                    ['locate', '-i', 'tasks.txt'],
                    capture_output=True,
                    text=True
                    )
            matches = taskspaths.stdout.splitlines()
            with open(matches[0]) as f:
                tasks = f.readlines()
            if not tasks:
                notasks = ["Your tasks list is empty sir",
                           "You have no tasks to take care of sir"]
                speak(random.choice(notasks))
            else:
                speak(f"You have {len(tasks)} tasks sir")
                for i,task in enumerate(tasks, start = 1):
                    print(f"Task {i}. {task.strip()}")
                    speak(f"Task {i}; {task.strip()}")
            return True
    return False

def handle_add_tasks(query):
    if "remember" in query or "to do list" in query or "tasks list" in query:
        patterns = [r"remember that i have to (.+)",
                    r"remember that i need to (.+)",
                    r"remember that i should (.+)",
                    r"add to my tasks list that i need to (.+)",
                    r"add to my tasks list that i have to (.+)",
                    r"add to my tasks list that i should (.+)",
                    r"add to my todo list that i need to (.+)",
                    r"add to my todo list that i have to (.+)",
                    r"add to my todo list that i should (.+)",
                    r"add to the tasks list that i need to (.+)",
                    r"add to the tasks list that i have to (.+)",
                    r"add to the tasks list that i should (.+)",
                    r"add to the todo list that i need to (.+)",
                    r"add to the todo list that i have to (.+)",
                    r"add to the todo list that i should (.+)"]
    
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                task = match.group(1)
                taskspaths = subprocess.run(
                        ['locate', '-ibr', '^tasks.txt$'],
                        capture_output=True,
                        text=True
                        )
                matches = taskspaths.stdout.splitlines()
                with open(matches[0], 'a') as f:
                    f.write(task + '\n')
                print("Task added")
                speak("Task added")
                return True
        return False
    return False


def handle_remove_tasks(query):
    alphanum = {
        "first": "1",
        "second": "2",
        "third": "3",
        "fourth": "4",
        "fifth": "5",
        "sixth": "6",
        "seventh": "7",
        "eighth": "8",
        "ninth": "9",
        "tenth": "10",
        "eleventh": "11",
        "twelfth": "12",
        "thirteenth": "13",
        "fourteenth": "14",
        "fifteenth": "15",
        "sixteenth": "16",
        "seventeenth": "17",
        "eighteenth": "18",
        "nineteenth": "19",
        "twentieth": "20"
    }
    if "remove" in query and ("task" in query or "tasks" in query):    
        y = False
        query = query.replace("and ", "")
        query = query.replace(",", "")
        for word, number in alphanum.items():
            query = query.replace(word, number)
        rmtasks = [r"remove the tasks numbered (.+)",
                   r"remove the (.+?) tasks"]
        for rmtask in rmtasks:
            match = re.search(rmtask, query)
            if match:
                y = True
                numbers = list(map(int, match.group(1).split()))
                taskspaths = subprocess.run(
                        ['locate', '-ibr', '^tasks.txt$'],
                        capture_output=True,
                        text=True
                        )
                matches = taskspaths.stdout.splitlines()
                with open(matches[0]) as f:
                    tasks = f.readlines()
                for num in sorted(numbers, reverse=True):
                    if 1<= num <= len(tasks):
                        tasks.pop(num-1)
                with open(matches[0], 'w') as f:
                    f.writelines(tasks)
                print("Tasks Removed")
                responses = ["Tasks Removed",
                            "Done.",
                            "Successful."]
                speak(random.choice(responses))
                return True
        if not y:
            speak("certainly sir, which tasks would you like to remove?")
            answer = input("certainly sir, which task(s) would you like to remove?\n").lower()
            if answer == "none" or answer == "nothing":
                return True
            else:
                answer = answer.replace("and ", "")
                answer = answer.replace(",", "")
                for word, number in alphanum.items():
                    answer = answer.replace(word, number)
                print(query)
                numbers = list(map(int, answer.split()))
                taskspaths = subprocess.run(
                        ['locate', '-ibr', '^tasks.txt$'],
                        capture_output=True,
                        text=True
                        )
                matches = taskspaths.stdout.splitlines()
                with open(matches[0]) as f:
                    tasks = f.readlines()
                for num in sorted(numbers, reverse=True):
                    if 1<= num <= len(tasks):
                        tasks.pop(num-1)
                with open(matches[0], 'w') as f:
                    f.writelines(tasks)
                print("Tasks Removed")
                responses = ["Tasks Removed",
                            "Done.",
                            "Successful."]
                speak(random.choice(responses))
                return True
            return False
        return False
    return False



while True:
    query = vad.listen().lower()
    query = query.replace(".", "").replace("?","").replace(",", "").strip() 
    print(repr(query))
    if (
        handle_youtube(query)
        or handle_locking(query)
        or handle_source_code(query)
        or handle_files(query)
        or handle_show_tasks(query)
        or handle_add_tasks(query)
        or handle_remove_tasks(query)
    ):
        continue

    print("Sorry sir, I didn't understand.")
