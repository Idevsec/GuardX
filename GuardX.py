import subprocess
import platform
import psutil
from tkinter import Tk, Button, Label, Text, Scrollbar, Frame, messagebox, simpledialog
import threading
import time
import webbrowser 

class FirewallNotifierGUI:
    def __init__(self, master):
        self.master = master
        master.title("GuardX")
        master.config(bg="#292929")

        self.label = Label(master, text="GuardX", font=('calibri', 20, 'bold'), bg="#292929", fg="white")
        self.label.pack(pady=(20, 10))

        self.text_output = Text(master, height=30, width=120, bg="#1E1E1E", fg="white", font=('calibri', 10))
        self.text_output.pack(pady=(0, 10), padx=10)
        self.scrollbar = Scrollbar(master, command=self.text_output.yview, bg="#1E1E1E")
        self.scrollbar.pack(side="right", fill="y")
        self.text_output.config(yscrollcommand=self.scrollbar.set)

        # Button frame to organize buttons horizontally
        button_frame = Frame(master, bg="#292929")
        button_frame.pack()

        self.list_connections_button = Button(button_frame, text="List Connections", command=self.list_connections, font=('calibri', 10, 'bold'), bg="#2ecc71", fg="white", relief="flat", activebackground="#27ae60", activeforeground="white")
        self.list_connections_button.pack(side="left", padx=5, pady=5)

        self.map_connections_button = Button(button_frame, text="Map Connections with Routes", command=self.map_connections_with_routes, font=('calibri', 10, 'bold'), bg="#3498db", fg="white", relief="flat", activebackground="#2980b9", activeforeground="white")
        self.map_connections_button.pack(side="left", padx=5, pady=5)

        self.adapter_info_button = Button(button_frame, text="Get Adapter Information", command=self.get_adapter_info, font=('calibri', 10, 'bold'), bg="#9b59b6", fg="white", relief="flat", activebackground="#8e44ad", activeforeground="white")
        self.adapter_info_button.pack(side="left", padx=5, pady=5)

        self.enable_firewall_button_win = Button(button_frame, text="Enable Firewall (Windows)", command=self.enable_firewall_windows, font=('calibri', 10, 'bold'), bg="#006400", fg="white", relief="flat", activebackground="#c0392b", activeforeground="white")
        self.enable_firewall_button_win.pack(side="left", padx=5, pady=5)

        self.disable_firewall_button_win = Button(button_frame, text="Disable Firewall (Windows)", command=self.disable_firewall_windows, font=('calibri', 10, 'bold'), bg="#006400", fg="white", relief="flat", activebackground="#c0392b", activeforeground="white")
        self.disable_firewall_button_win.pack(side="left", padx=5, pady=5)

        self.enable_firewall_button_linux = Button(button_frame, text="Enable Firewall (Linux)", command=self.enable_firewall_linux, font=('calibri', 10, 'bold'), bg="#e74c3c", fg="white", relief="flat", activebackground="#c0392b", activeforeground="white")
        self.enable_firewall_button_linux.pack(side="left", padx=5, pady=5)

        self.disable_firewall_button_linux = Button(button_frame, text="Disable Firewall (Linux)", command=self.disable_firewall_linux, font=('calibri', 10, 'bold'), bg="#e74c3c", fg="white", relief="flat", activebackground="#c0392b", activeforeground="white")
        self.disable_firewall_button_linux.pack(side="left", padx=5, pady=5)

        self.clear_button = Button(button_frame, text="Clear", command=self.clear_text_output, font=('calibri', 10, 'bold'), bg="#34495e", fg="white", relief="flat", activebackground="#2c3e50", activeforeground="white")
        self.clear_button.pack(side="left", padx=5, pady=5)
    
            # Footer label with hyperlink
        self.footer_label = Label(
            master,
            text="Made with Coffee by IDevSec",
            font=('calibri', 10, 'italic', 'underline'),  # Underline to indicate a hyperlink
            bg="#292929",
            fg="white",
            cursor="hand2"
        )
        self.footer_label.pack(side="bottom", pady=10)

        # Bind left-click event to open the hyperlink
        self.footer_label.bind("<Button-1>", lambda e: self.open_idevsec_link())

    def open_idevsec_link(self):
        # Open the IDevSec LinkedIn page in the default web browser
        webbrowser.open("https://www.linkedin.com/company/idevsec")

    def list_connections(self):
        try:
            connections = psutil.net_connections()
            output = "\n".join([f"PID: {conn.pid}, Local Address: {conn.laddr}, Remote Address: {conn.raddr}, Status: {conn.status}" for conn in connections])
            self.update_text_output(output)
        except Exception as e:
            self.show_error_message(f"Failed to list connections: {e}")

    def map_connections_with_routes(self):
        try:
            if platform.system() == 'Linux':
                output = subprocess.check_output(['netstat', '-rn']).decode("utf-8")
            elif platform.system() == 'Windows':
                routes = psutil.net_if_stats()
                output = "\n".join([f"Interface: {interface}\nRoutes: {routes[interface]}" for interface in routes])
            self.update_text_output(output)
        except Exception as e:
            self.show_error_message(f"Failed to map connections with routes: {e}")

    def get_adapter_info(self):
        try:
            adapters = psutil.net_if_addrs()
            output = "\n".join([f"Adapter: {adapter_name}\nIP Address: {addr.address}, Netmask: {addr.netmask}, Broadcast IP: {addr.broadcast}" for adapter_name, addrs in adapters.items() for addr in addrs])
            self.update_text_output(output)
        except Exception as e:
            self.show_error_message(f"Failed to get adapter information: {e}")

    def enable_firewall_windows(self):
        try:
            subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'], check=True)
            self.show_info_message("Firewall Status", "Windows Firewall enabled.")
        except Exception as e:
            self.show_error_message(f"Failed to enable Windows firewall: {e}")

    def disable_firewall_windows(self):
        try:
            subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'off'], check=True)
            self.show_info_message("Firewall Status", "Windows Firewall disabled.")
        except Exception as e:
            self.show_error_message(f"Failed to disable Windows firewall: {e}")

    def enable_firewall_linux(self):
        try:
            subprocess.run(['ufw', 'enable'], check=True)
            self.show_info_message("Firewall Status", "Firewall enabled.")
        except Exception as e:
            self.show_error_message(f"Failed to enable Linux firewall: {e}")

    def disable_firewall_linux(self):
        try:
            subprocess.run(['ufw', 'disable'], check=True)
            self.show_info_message("Firewall Status", "Firewall disabled.")
        except Exception as e:
            self.show_error_message(f"Failed to disable Linux firewall: {e}")

    def clear_text_output(self):
        self.text_output.delete(1.0, "end")

    def update_text_output(self, text):
        self.text_output.delete(1.0, "end")
        self.text_output.insert("end", text)

    def show_info_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error_message(self, title, message):
        messagebox.showerror(title, message)

if __name__ == "__main__":
    root = Tk()
    root.geometry("1400x800")
    my_gui = FirewallNotifierGUI(root)
    root.mainloop()