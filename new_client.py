import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    global msg_list
    while True:  # continuous loop that receives messages
        msg = s.recv(1024).decode()
        # check if a message is a chat text or a command
        if msg[0] == '9':
            msg_arr = msg.split()
            if msg_arr[0] == '9/w':  # check if it's a whisper
                if msg_arr[1] == username:
                    msg_list.insert(tkinter.END, " ".join(msg_arr[2:]))
            else:
                msg_list.insert(tkinter.END, msg[1:])  # append the message to the message frame

        else:  # print out data about the connected to the server clients and rooms
            data = parse_all_rooms(msg)
            label = tkinter.Label(root, text="Available Rooms: ")
            label.pack()
            print(data)
            for room in data:
                new_label = tkinter.Label(root, text=f"Room number {room[0]} - connected users : {room[1]}")
                new_label.pack()

            input_box = tkinter.Entry(root)
            input_box.pack()

            submit_button = tkinter.Button(root, text="Continue", command=lambda: join_room(input_box.get()))
            submit_button.pack()


def send():
    global my_msg
    msg = my_msg.get().split()
    # check if a given message is a whisper and if so change the format
    if msg[0] == "/w":
        sent_msg = f"7{msg[0]} {msg[1]} [DM]{username}: {' '.join(msg[2:])}"
    else:
        sent_msg = f"4{username}: {my_msg.get()}"
    print(sent_msg)
    my_msg.set("")
    s.sendall(sent_msg.encode())


def add_room(number):
    # send a command to create a new room
    s.sendall(f"1{number}".encode())
    print("Room Created")
    clean_window()
    label = tkinter.Label(root, text="Room Successfully created")
    label.pack()
    time.sleep(0.5)
    create_main_menu()


def create_a_room():
    clean_window()
    label = tkinter.Label(root, text="Give a Number of a Room you wanna create")
    label.pack()

    input_box = tkinter.Entry(root)
    input_box.pack()

    submit_button = tkinter.Button(root, text="Continue", command=lambda: add_room(input_box.get()))
    submit_button.pack()


def parse_all_rooms(str):  # decode information about the connected clients and rooms
    return [room.split(":") for room in str.split("/")][:-1]


def join_room(number):
    global active_room
    # join  room with a given number
    s.sendall(f"2{number}".encode())
    active_room = number
    open_chat_window()


def get_rooms_info():
    clean_window()
    # ask server about the connected clients
    s.sendall("52".encode())


def open_chat_window():
    global my_msg, msg_list
    clean_window()

    # Create a frame that will contain all the messages in the chat
    messages_frame = tkinter.Frame(root)
    my_msg = tkinter.StringVar()
    my_msg.set("")
    scrollbar = tkinter.Scrollbar(messages_frame)
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    exit_button = tkinter.Button(root, text="X", command=create_main_menu, width=5, height=2)
    exit_button.pack(side="top", anchor="e")
    msg_list.pack()
    messages_frame.pack()

    # create an input text field
    entry_field = tkinter.Entry(root, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(root, text="Send", command=send)
    send_button.pack()
    label = tkinter.Label(root, text=f"Currently in Room {active_room}")
    label.pack()


def leave_room_window():
    clean_window()
    label = tkinter.Label(root, text="Give a Number of a Room you wanna leave")
    label.pack()

    input_box = tkinter.Entry(root)
    input_box.pack()

    submit_button = tkinter.Button(root, text="Continue", command=lambda: leave_room(input_box.get()))
    submit_button.pack()

def leave_room(number):
    # send a command to leave an existing room
    s.sendall(f"3{number}".encode())
    print("Room left")
    clean_window()
    label = tkinter.Label(root, text="Room Successfully left")
    label.pack()
    time.sleep(0.5)
    create_main_menu()

def change_username():
    # setup username
    global input_box
    clean_window()
    label = tkinter.Label(root, text="Enter username:")
    label.pack()

    input_box = tkinter.Entry(root)
    input_box.pack()

    submit_button = tkinter.Button(root, text="Continue", command=on_submit)
    submit_button.pack()


def quit():
    # disconnect from the server and close the client
    s.sendall("6".encode())
    root.destroy()


def clean_window():
    # destroy all objects on the screen
    for widget in root.winfo_children():
        widget.destroy()


def create_main_menu():
    clean_window()
    button1 = tkinter.Button(text="Create a Room", command=create_a_room, width=20, height=4)
    button1.pack()

    button2 = tkinter.Button(text="Join a Room", command=get_rooms_info, width=20, height=4)
    button2.pack()

    button3 = tkinter.Button(text="Open chat window", command=open_chat_window, width=20, height=4)
    button3.pack()

    button4 = tkinter.Button(text="Delete Room", command=leave_room_window, width=20, height=4)
    button4.pack()

    button5 = tkinter.Button(text="Change username", command=change_username, width=20, height=4)
    button5.pack()

    button6 = tkinter.Button(text="Quit", command=quit, width=20, height=4)
    button6.pack()


def on_submit():
    global username, input_box
    username = input_box.get()
    create_main_menu()


# default connection
username = "DEFAULT"
active_room = -1

# connecting to server
HOST = "192.168.1.64"
PORT = 1234
ADDR = (HOST, PORT)

s = socket(AF_INET, SOCK_STREAM)
s.connect(ADDR)

# create GUI
root = tkinter.Tk()
root.title("IRC CHAT APP")
root.geometry("500x500")
change_username()

# create listening thread
receive_thread = Thread(target=receive, daemon=True)
receive_thread.start()
tkinter.mainloop()
