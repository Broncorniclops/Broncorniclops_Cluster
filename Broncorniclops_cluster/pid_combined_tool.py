
from pid_manager import PIDManager
import tkinter as tk
from tkinter import simpledialog, filedialog, ttk
import json
import can
import threading

pid_manager = PIDManager()

class CombinedPIDTool:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Digital Cluster: PID Debugger & CAN Viewer")

        self.notebook = ttk.Notebook(self.window)
        
        control_frame = tk.Frame(self.window)
        control_frame.pack()

        tk.Button(control_frame, text="Minimize", command=self.minimize).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Exit", command=self.exit).pack(side=tk.LEFT)
        self.notebook.pack(fill='both', expand=True)

        self.debugger_tab = tk.Frame(self.notebook)
        self.viewer_tab = tk.Frame(self.notebook)
        self.chart_tab = tk.Frame(self.notebook)

        self.notebook.add(self.debugger_tab, text='Live PID Debugger')
        self.notebook.add(self.viewer_tab, text='CAN Traffic Log')
        self.notebook.add(self.chart_tab, text='PID Chart (Placeholder)')

        # Debugger Tab
        self.output = tk.Text(self.debugger_tab, height=25, width=90)
        self.output.pack()
        self.seen_pids = set()

        button_frame = tk.Frame(self.debugger_tab)
        button_frame.pack()

        tk.Button(button_frame, text="Export PID List", command=self.export_pid_list).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Refresh Display", command=self.refresh_display).pack(side=tk.LEFT)

        self.output.bind("<Double-Button-1>", self.on_double_click)

        # Viewer Tab
        self.viewer_output = tk.Text(self.viewer_tab, height=25, width=90)
        self.viewer_output.pack()

        # Start CAN listener thread
        self.running = True
        try:
            self.bus = can.interface.Bus(channel='can0', bustype='socketcan')
            threading.Thread(target=self.read_can_loop, daemon=True).start()
        except Exception as e:
            self.viewer_output.insert(tk.END, f"❌ CAN bus error: {e}\n")

        # Chart Tab Placeholder
        self.chart_canvas = tk.Canvas(self.chart_tab, bg='white', height=300)
        self.chart_canvas.pack(fill='both', expand=True)

    def display_pid(self, pid, value):
        label = pid_manager.get_label(pid)
        if pid not in self.seen_pids:
            self.seen_pids.add(pid)
            if "Unknown" in label:
                pid_manager.register_pid(pid, "Unknown PID")
        line = f"{label} (PID {pid}): {value}\n"
        self.output.insert(tk.END, line)

    def on_double_click(self, event):
        line_index = self.output.index(f"@{event.x},{event.y}")
        line_text = self.output.get(f"{line_index} linestart", f"{line_index} lineend")
        if "(PID " in line_text:
            pid = line_text.split("(PID ")[1].split(")")[0]
            current_label = pid_manager.get_label(pid)
            new_label = simpledialog.askstring("Edit PID Label", f"Enter new label for PID {pid}:", initialvalue=current_label)
            if new_label:
                pid_manager.set_label(pid, new_label)
                self.output.insert(tk.END, f"✅ Updated label for PID {pid} to: {new_label}\n")

    def export_pid_list(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filepath:
            with open(filepath, 'w') as f:
                json.dump(pid_manager.all_pids(), f, indent=2)
            self.output.insert(tk.END, f"📁 Exported PID list to {filepath}\n")

    def refresh_display(self):
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "🔄 Display cleared. Ready for new PID input.\n")

    def read_can_loop(self):
        while self.running:
            msg = self.bus.recv()
            if msg and len(msg.data) >= 3:
                data = list(msg.data)
                if data[1] == 0x41:
                    pid = f"{data[2]:02X}"
                    label = pid_manager.get_label(pid)
                    decoded = self.decode_pid(pid, data[3:])
                    log_entry = f"[CAN {msg.arbitration_id:X}] {label} (PID {pid}): {decoded}\n"
                    self.viewer_output.insert(tk.END, log_entry)
                    self.display_pid(pid, decoded)

    def decode_pid(self, pid, data_bytes):
        try:
            if pid == "0C":
                return (data_bytes[0] * 256 + data_bytes[1]) // 4
            elif pid == "0D":
                return data_bytes[0]
            elif pid == "05":
                return data_bytes[0] - 40
            elif pid == "0F":
                return data_bytes[0] - 40
            elif pid == "10":
                return (data_bytes[0] * 256 + data_bytes[1]) / 100
            elif pid == "2F":
                return data_bytes[0] * 100 / 255
            elif pid == "11":
                return data_bytes[0] * 100 / 255
            elif pid == "1F":
                return data_bytes[0] * 256 + data_bytes[1]
            elif pid == "46":
                return data_bytes[0] - 40
            else:
                return f"0x{''.join(format(b, '02X') for b in data_bytes)}"
        except:
            return "decode error"

    def minimize(self):
        self.window.iconify()

    def exit(self):
        self.running = False
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CombinedPIDTool()
    app.run()
