try:
    # Tkinter imports
    from tkinter import *
    from tkinter import messagebox

    # Utils
    from analysis import SentimentAnalysis

    # Client imports
    from socket import AF_INET, socket, SOCK_STREAM
    from threading import Thread
except ImportError:
    import sys
    import subprocess
    from socket import AF_INET, socket, SOCK_STREAM
    from threading import Thread
    from analysis import SentimentAnalysis
    print("[NOT IMPORTED] ~ Tkinter")
    print("[TRYING TO IMPORT]")
    subprocess.call([sys.executable, "-m", "pip", "install", "Tkinter"])
    print("[IMPORTED TKINTER]")


# Tkinter utils
root = Tk()
icon = PhotoImage('images.png')
root.resizable(0, 0)
root.title("Online Chat App")
root.geometry("500x590+300+200")
messages = []


# Tkinter GUI (making it nice looking)
class TkinterGUI(object):
    def __init__(self):
        self.title_label = self
        self.top_frame = self
        self.explanation = self
        self.button_chat = self
        self.home_screen()

    def home_screen(self):
        self.top_frame = Frame(root, bg="#99FFCC", width=500, height=100)  # add image
        self.top_frame.grid(column=0, row=1)
        self.title_label = Label(root, text="Chat App by Henry Boisdequin",
                                 width=25, height=2, bg="#CCFFFF", font=("Helvetica", 20))
        self.title_label.grid(column=0, row=2, padx=10, pady=10)
        self.explanation = Label(root, text="""This app is an Online Chat app
that is powered by machine learning. 
As the user, you will be able to chat with 
other people on an online server. 
At the end of the chat
you can decide to view a graph
which tracks how your emotions has
changed over the chat, using
sentiment analysis.

By Henry Boisdequin
        """, width=33, height=15, bg="#99FFCC", font=("Leoscar", 12))
        self.explanation.grid(column=0, row=3, padx=10, pady=10)
        self.button_chat = Button(root, text="Chat!", width=25, height=2,
                                  highlightbackground="#CCFFFF", padx=10, pady=10,
                                  command=go_to_chat)
        self.button_chat.grid(column=0, row=5)


def exit_chat(root_type):
    msg = messagebox.askyesno("Advance", "Would you like to see a graph of your emotions during the chat?")
    if msg == 0:  # if no
        root_type.destroy()
    else:  # if yes
        root_type.destroy()
        sentiment = SentimentAnalysis()
        sentiment.sentiment_score(msg_list)  # list of messages


def leave_(root_type):
    global name
    name = name_box.get().strip()
    root_type.destroy()
    chat()


def send_message_on_server():
    global ChatLog, messages
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    # display message
    while True:
        try:
            if msg != '':
                ChatLog.config(state=NORMAL)
                """Handles sending/receiving messages on the server"""
                ChatLog.insert(END, f"{name}: " + msg + '\n\n')
                client_socket.send(bytes(msg, "utf8"))
                if chat_root.destroy():
                    client_socket.close()
                    chat_root.quit()
                messages.append(msg)
                ChatLog.config(foreground="#442265", font=("Verdana", 12))
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(root.END, msg)
        except Exception as err:
            print(f"[ERROR] {err}")
            ChatLog.insert(END, f"[ERROR] {err}" + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


def go_to_chat():
    global name_box
    root.destroy()

    # ask for name and proceed if someone else has connected
    # add the if someone else has connected
    question_root = Tk()
    variable = StringVar(question_root)
    question_root.geometry("500x590+300+200")
    question_root.title("Enter Name")
    top_frame = Frame(question_root, bg="#99FFCC", width=500, height=100)
    top_frame.grid(column=0, row=1)
    Label(question_root, text="").grid(column=0, row=2)
    Label(question_root, text="Please enter your name", bg="#CCFFFF").grid(column=0, row=3)
    name_box = Entry(question_root, bd=0, bg="#99FFCC", width="29", font="Arial", textvariable=variable)
    name_box.grid(column=0, row=4)
    leave = Button(question_root, text="Click to Chat!", width=25, height=2,
                   highlightbackground="#CCFFFF", padx=10, pady=10,
                   command=lambda: leave_(question_root))
    leave.grid(column=0, row=5)


def chat():
    global ChatLog, EntryBox, chat_root, msg_list
    # enter chat room
    chat_root = Tk()
    chat_root.title("Chat Room")
    chat_root.geometry("400x500")

    # Create Chat window
    ChatLog = Text(chat_root, bd=0, bg="white", height="8", width="50", font="Arial")

    ChatLog.config(state=DISABLED)

    # Put a scrollbar on Chat window
    scrollbar = Scrollbar(chat_root, command=ChatLog.yview, cursor="heart")
    ChatLog['yscrollcommand'] = scrollbar.set

    # Create Button to be able to send message
    SendButton = Button(chat_root, font=("Verdana", 15, 'bold'), text="Send", width=6, height=2,
                        bd=0, bg="#CCFFFF", activebackground="white", fg='black',
                        command=send_message_on_server)
    ExitButton = Button(chat_root, font=("Verdana", 15, 'bold'), text="Quit",
                        width=6, height=2, bd=0, bg="#CCFFFF", activebackground="white",
                        fg="black", command=lambda: exit_chat(chat_root))

    # Create the box to enter message
    EntryBox = Text(chat_root, bd=0, bg="#99FFCC", width="29", height="5", font="Arial")
    EntryBox.bind("<Return>", send_message_on_server)

    msg_list = Listbox(chat_root, height=15, width=50, yscrollcommand=scrollbar.set)

    # Place all components on the screen
    scrollbar.place(x=376, y=6, height=386)
    ChatLog.place(x=6, y=6, height=386, width=370)
    EntryBox.place(x=128, y=401, height=90, width=265)
    SendButton.place(x=6, y=440, height=45)
    ExitButton.place(x=6, y=401, height=45)


# Finish Server
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread()
receive_thread.start()
root.mainloop()
