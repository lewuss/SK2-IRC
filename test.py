# import tkinter as tk
# from socket import AF_INET, socket, SOCK_STREAM
# import threading
# username = "DEFAULT"
# HOST = "192.168.1.64"
# PORT = 1234
#
# ADDR = (HOST, PORT)
#
#
#
# s = socket(AF_INET, SOCK_STREAM)
# s.connect(ADDR)
#
# s.sendall("5".encode())
# data = s.recv(1024)
# print(data)
test_string = "0:15/1:2/2:4"
def parse_all_rooms(str):
    return [room.split(":") for room in str.split("/")]
print(parse_all_rooms(test_string))
