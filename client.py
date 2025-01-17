
from threading import Thread 
import tkinter
import socket

def receive():
	"""Receive message"""
	while True:
		try:
			msg = client_socket.recv(1024).decode()
			msg_list.insert(tkinter.END, msg)
		except OSError:
			break

def send(event=None):
	msg = my_msg.get()
	my_msg.set("") 
	client_socket.send(msg.encode())
	if msg == "{quit}":
		client_socket.close()
		top.quit()

def on_closing(event=None):
	my_msg.set("{quit}")
	send()

top = tkinter.Tk()
top.title("Chatting room")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your message")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list=tkinter.Listbox(messages_frame, height=40, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill = tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill = tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable = my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

host="127.0.0.1"
port=7072

client_socket=socket.socket()
client_socket.connect((host, port))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()