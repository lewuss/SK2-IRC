import tkinter as tk
import socket
import threading


def button1_command():
    s.sendall("10".encode())
    print("Room Created")


def button2_command():
    s.sendall("20".encode())


def button3_command():
    global input_var, input_box, exit_button, input_label
    for widget in root.winfo_children():
        widget.destroy()
    input_var = tk.StringVar()
    input_box = tk.Entry(root, textvariable=input_var)
    input_box.pack(side="bottom", fill="x")
    send_button = tk.Button(root, text="Send", command=send_input, width=15, height=2)
    send_button.pack(side="right")
    exit_button = tk.Button(root, text="X", command=exit_command, width=5, height=2)
    exit_button.pack(side="top", anchor="e")
    input_label = tk.Label(root, text="Welcome to the chat")
    input_label.pack()
    # start a new thread to listen for incoming messages



def listen_for_messages():
    global input_label
    while True:
        data = s.recv(1024)
        print(data)
        if not data:
            break
        txt = input_label.cget("text") + '\n' + data.decode()
        input_label.destroy()
        input_label = tk.Label(root, text=txt)
        input_label.pack()


def button4_command():
    print("Button 4 pressed")


def send_input():
    input_text = input_var.get()
    input_text = f"4{input_text}"
    input_box.delete(0, 'end')
    s.sendall(input_text.encode())


def exit_command():
    for widget in root.winfo_children():
        widget.destroy()
    create_main_menu()


def create_main_menu():
    button1 = tk.Button(text="Button 1", command=button1_command, width=20, height=4)
    button1.pack()

    button2 = tk.Button(text="Button 2", command=button2_command, width=20, height=4)
    button2.pack()

    button3 = tk.Button(text="Button 3", command=button3_command, width=20, height=4)
    button3.pack()

    button4 = tk.Button(text="Button 4", command=button4_command, width=20, height=4)
    button4.pack()


# get local machine name
host = "192.168.1.64"
port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
root = tk.Tk()
root.geometry("500x500")
create_main_menu()
root.bind('<Return>', lambda event: send_input())
threading.Thread(target=listen_for_messages, daemon=True).start()
root.mainloop()
