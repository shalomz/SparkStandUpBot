import standup
import pickle
import threading
from datetime import datetime
import standup
from bot_config import bot_name



#SAVE_FILE = "save.dat"

#condition = threading.Condition()

iq = None
oq = None


def process(mu):
    cmd = mu.text
    if cmd.startswith(bot_name):
        cmd = cmd[len(bot_name):].lstrip()
    #global standups
    if cmd == "/newmeeting":
        new_standup = standup.standup(mu.person_email)
       #new_standup.iq.put(mu)
        mu.response = new_standup.create()    #TODO change to standup oq
        print(mu.response)
        print("mf 3.1")
        oq.put(mu)

    elif cmd == "/owned":
        mu.response = standup.owned_standups(mu.person_email)
       # mu.response = len(standup.standups)
        print("mf 3")
        oq.put(mu)

    elif cmd.startswith("/report"):
        try:
            cmd = cmd.split()[1]  #name
            mu.response = standup.report(mu.person_email, cmd)
        except IndexError:
            mu.response = "usage: /report meeting_name"

        oq.put(mu)
    elif cmd.startswith("/run"):
        try:
            cmd = cmd.split()[1]  #name
            mu.response = standup.run(mu.person_email, cmd)
        except IndexError:
            mu.response = "usage: /run meeting_name"
        oq.put(mu)

    elif cmd.startswith("/when"):
        try:
            cmd = cmd.split()[1]  # name
            mu.response = standup.upcoming_time(mu.person_email, cmd)
        except IndexError:
            mu.response = "usage: /when meeting_name"
        oq.put(mu)

    elif cmd.startswith("/cancel"):
        try:
            cmd = cmd.split()[1]  # name
            mu.response = standup.delete_standup(mu.person_email, cmd)
        except IndexError:
            mu.response = "usage: /delete meeting_name"
        oq.put(mu)

    elif cmd.startswith("/addroom"):
        try:
            cmd = cmd.split()[1]  # name
            mu.response = standup.add_room(mu.person_email, cmd, mu.room_id)
        except IndexError:
            mu.response = "usage: /addroom meeting_name"
        oq.put(mu)

    elif cmd.startswith("/removeroom"):
        try:
            cmd = cmd.split()[1]  # name
            mu.response = standup.add_room(mu.person_email, cmd, mu.room_id)
        except IndexError:
            mu.response = "usage: /removeroom meeting_name"
        oq.put(mu)


    elif cmd.startswith("/skipnext"):

       try:
           cmd = cmd.split()[1]  # name
           mu.response = standup.skip_next(mu.person_email, cmd)
       except IndexError:
           mu.response = "usage: /skipnext 'meeting name'"
       oq.put(mu)

    elif cmd.startswith("/viewmeeting"):
     #   print("got viewqeustions")
        try:
            cmd = cmd.split()[1]
            mu.response = standup.view_meeting(mu.person_email, cmd)
        except IndexError:
            mu.response = "usage: /viewmeeting 'meeting name'"
        oq.put(mu)

    elif cmd.startswith("/viewquestions"):
        print("got viewqeustions")
        try:
            cmd = cmd.split()[1]
            mu.response = standup.view_questions(mu.person_email, cmd)
        except IndexError:
            mu.response = "usage: /viewquestions 'meeting name'"
        oq.put(mu)

    elif cmd.startswith("/defaultquestions"):
        try:

            cmd = cmd.split()[1]   #meeting name

            mu.response = standup.add_default_questions(mu.person_email, cmd)
        except(IndexError, ValueError):
            mu.response = "usage: /defaultquestions 'meeting name'"
        oq.put(mu)

    elif cmd.startswith("/addquestion"):
        try:
            lst = cmd.split()
            cmd = lst[1]
            question = " ".join(lst[2:])
            print(question)
            mu.response = standup.add_question(mu.person_email, cmd, question)
        except IndexError:
            mu.response = "usage: /addquestion 'new question'"
        oq.put(mu)

    elif cmd.startswith("/deletequestion"):
        try:
            lst = cmd.split()  #"cmd = /deletequestion abc 2"
            cmd = lst[1]   # cmd = abc
            print(cmd)
            qno = int(lst[2])  #qno = 2
            print(qno)
            mu.response = standup.delete_question(mu.person_email, cmd, qno)
        except IndexError:
            mu.response = "usage: /deletequestion 'standup name' 'question number"
        except ValueError:
            mu.response = "Please use /viewquestions to check the question numbers. usage: /deletequestion 'standup name' 'question number"
        oq.put(mu)


    elif cmd == "/help":
        resp = "/newmeeting  - create a new meeting \n\n" \
                "/viewmeeting 'meeting name - show details of the meeting \n\n" \
                "/owned - see meetings created by you\n\n" \
               "/report 'meeting name' - see report\n\n" \
               "/run 'meeting name - run the meeting \n\n" \
                "/when 'meeting  name' - show next scheduled time\n\n" \
                "/cancel 'meeting name' - delete meeting \n\n" \
                "/skipnext 'meeting  name' - skip next scheduled meeting \n\n" \
                "/addroom 'meeting  name' - report will be shared in the room\n\n" \
                "/viewquestions 'meeting  name' - view the questions\n\n" \
                "/defaultquestions 'meeting name' - add default question for the meeting\n\n" \
                "/addquestion 'meeting  name' - add question to meeting\n\n" \
                "/deletequestion 'meeting name' 'question number' - delete particualr question\n\n" \
                "/removeroom 'meeting  name' - stop sharing report in the room\n\n" \
                "/add 'meeting name' 'email' - add new participant to meeting \n\n" \
               "/delete 'meeting name' 'email' - delete participant from meeting \n\n"


        mu.response = resp
        oq.put(mu)

    elif cmd.startswith("/add"):
        try:
            cmd = cmd.split()  # standup name
            mu.response = standup.add(mu.person_email, cmd[1], cmd[2])
        except IndexError:
            mu.response = "usage: /add 'standup name' 'email'"
        oq.put(mu)

    elif cmd.startswith("/delete"):
        try:
            cmd = cmd.split()  # standup name
            mu.response = standup.delete(mu.person_email, cmd[1], cmd[2])
        except IndexError:
            mu.response = "usage: /delete 'standup name' 'email'"
        oq.put(mu)


    else:
        if mu.person_email in standup.subscriptions:
            print("sending to standup")
            mu.response = standup.subscriptions[mu.person_email].process(mu.text, mu.person_email)
            oq.put(mu)
        else:
            mu.response = "try /help for help"
            oq.put(mu)

def timer(_condition):
   # global condition
    condition = _condition
    condition.acquire()
    print("acquired")
    while True:
        delta_t = None
        if standup.standups.get_min():
            delta_t = standup.standups.get_min().upcoming - datetime.now()
            if delta_t.total_seconds() < 0:
                print("starting standup")
                current = standup.standups.del_min()
                condition.release()
                worker_thread = threading.Thread(target=current.run)
                worker_thread.daemon = True
                #current.run()
                current.upcoming = standup.standup.find_upcoming(current.days, current.time[0], current.time[1])
                standup.update_standup(current)
                worker_thread.start()
                condition.acquire()
                continue
        print("before wait")
        if delta_t:
            print("in delta_t")
            condition.wait(delta_t.total_seconds())   #releases the lock
        else:
            condition.wait()
        print("notified")

def oq_consumer(q):
    while True:
        if not q.empty():
            print("new itme in queue")
            oq.put(q.get())

def start(incoming_q, outgoing_q):
    global iq, oq
    iq = incoming_q
    oq = outgoing_q
  #  global standups
    try:
        with open(standup.SAVE_FILE, "rb") as savefile:
            while True:
                try:
                    content = (pickle.load(savefile))
                    if isinstance(content, standup.standup):
                        print(content)
                        standup.standups.insert(content)
                except(EOFError):
                    break
    except FileNotFoundError:
        pass

    timer_thread = threading.Thread(target=timer, args=(standup.condition,))
    timer_thread.daemon = True
    timer_thread.start()

    oq_thread = threading.Thread(target=oq_consumer, args=(standup.standup_oq,))
    oq_thread.daemon = True
    oq_thread.start()
    while True:
        while not iq.empty():
            print("mf 2")
            process(iq.get())