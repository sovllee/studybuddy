import socket
from threading import Thread
import tkinter as tk


class SecondPage(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)

        self.title("Second Page")
        self.geometry('400x300')

        self.label = tk.Label(self, text="Welcome to the Second Page!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.close_button = tk.Button(self, text="Close", command=self.close_window)
        self.close_button.pack(pady=10)


        start_button = tk.Button(self, text="Start a Chat", command=self.open_chat_app)
        start_button.pack()

    def close_window(self):
        self.destroy()

    def open_chat_app(self):
        self.withdraw()  # Hide the second page
        chat_app = ChatApplication()
        chat_app.protocol("WM_DELETE_WINDOW", self.on_closing)
        chat_app.mainloop()

    def on_closing(self):
        self.destroy()


class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chat Application")

        self.message_list = tk.Listbox(self, width=50, height=20)
        self.message_list.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(self, width=50)
        self.message_entry.pack(pady=5)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.host = "0.0.0.0"
        self.port = 8080
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.socket.send(message.encode())
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                self.message_list.insert(tk.END, message)
            except Exception as e:
                print("Error receiving message:", e)
                break

    def start_server(self):
        clients = {}

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))
        server_sock.listen(5)
        print("Server listening on port", self.port)

        def handle_clients(conn):
            name = conn.recv(1024).decode()
            welcome = f"Welcome {name}. Start a chat with your friend:)"
            conn.send(bytes(welcome, "utf8"))
            msg = name + " has joined the chat"
            broadcast(bytes(msg, "utf8"))

            clients[conn] = name

            while True:
                msg = conn.recv(1024)
                broadcast(msg, name + ":")

        def broadcast(msg, prefix=""):
            for client in clients:
                client.send(bytes(prefix, "utf8") + msg)

        while True:
            client_conn, client_address = server_sock.accept()
            print(client_address, "has connected")
            client_conn.send(bytes("Welcome to the chat room. Please type your name to continue", "utf8"))
            Thread(target=handle_clients, args=(client_conn,)).start()


if __name__ == "__main__":
    second_page = SecondPage()
    second_page.mainloop()
