#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

active_room = -1


def receive():
    global msg_list
    while True:
        msg = s.recv(1024).decode()
        print(f"{msg} - decoded shit")
        if msg[0] == '9':
            msg_list.insert(tkinter.END, msg[1:])
        else:
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


def send(event=None):
    global my_msg
    msg = f"4{username}: {my_msg.get()}"
    print(msg)
    my_msg.set("")
    s.sendall(msg.encode())


def add_room(number):
    s.sendall(f"1{number}".encode())
    print("Room Created")
    for widget in root.winfo_children():
        widget.destroy()
    label = tkinter.Label(root, text="Room Succesfully created")
    label.pack()
    time.sleep(0.5)
    create_main_menu()


def button1_command():
    for widget in root.winfo_children():
        widget.destroy()
    label = tkinter.Label(root, text="Give a Number of a Room you wanna create")
    label.pack()

    input_box = tkinter.Entry(root)
    input_box.pack()

    submit_button = tkinter.Button(root, text="Continue", command=lambda: add_room(input_box.get()))
    submit_button.pack()


def parse_all_rooms(str):
    return [room.split(":") for room in str.split("/")][:-1]


def join_room(number):
    global active_room
    s.sendall(f"2{number}".encode())
    active_room = number
    create_main_menu()


def button2_command():
    for widget in root.winfo_children():
        widget.destroy()
    s.sendall("52".encode())


def button3_command():
    global my_msg, msg_list
    for widget in root.winfo_children():
        widget.destroy()
    messages_frame = tkinter.Frame(root)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    exit_button = tkinter.Button(root, text="X", command=create_main_menu, width=5, height=2)
    exit_button.pack(side="top", anchor="e")
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(root, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(root, text="Send", command=send)
    send_button.pack()
    label = tkinter.Label(root, text=f"Currently in Room {active_room}")
    label.pack()


def button4_command():
    print("Button 4 pressed")


def button5_command():
    global input_box
    for widget in root.winfo_children():
        widget.destroy()
    label = tkinter.Label(root, text="Enter username:")
    label.pack()

    input_box = tkinter.Entry(root)
    input_box.pack()

    submit_button = tkinter.Button(root, text="Continue", command=on_submit)
    submit_button.pack()


def button6_command():
    s.sendall("6".encode())


def create_main_menu():
    for widget in root.winfo_children():
        widget.destroy()
    button1 = tkinter.Button(text="Create a Room", command=button1_command, width=20, height=4)
    button1.pack()

    button2 = tkinter.Button(text="Join a Room", command=button2_command, width=20, height=4)
    button2.pack()

    button3 = tkinter.Button(text="Open chat window", command=button3_command, width=20, height=4)
    button3.pack()

    button4 = tkinter.Button(text="Delete Room", command=button4_command, width=20, height=4)
    button4.pack()

    button5 = tkinter.Button(text="Change username", command=button5_command, width=20, height=4)
    button5.pack()

    button5 = tkinter.Button(text="Quit", command=button6_command, width=20, height=4)
    button5.pack()


def on_submit():
    global username, input_box
    username = input_box.get()
    create_main_menu()


username = "DEFAULT"
HOST = "192.168.1.64"
PORT = 1234

ADDR = (HOST, PORT)
root = tkinter.Tk()
root.title("IRC CHAT APP")
root.geometry("500x500")

s = socket(AF_INET, SOCK_STREAM)
s.connect(ADDR)
button5_command()
receive_thread = Thread(target=receive, daemon=True)
receive_thread.start()
tkinter.mainloop()
