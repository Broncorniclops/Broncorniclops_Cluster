
from pid_manager import PIDManager
import tkinter as tk
from tkinter import simpledialog, filedialog
import json

pid_manager = PIDManager()

class PIDDebugger:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("CAN PID Debugger")
        self.output = tk.Text(self.window, height=30, width=80)
        self.output.pack()

        button_frame = tk.Frame(self.window)
        button_frame.pack()

        export_btn = tk.Button(button_frame, text="Export PID List", command=self.export_pid_list)
        export_btn.pack(side=tk.LEFT)

        refresh_btn = tk.Button(button_frame, text="Refresh Display", command=self.refresh_display)
        refresh_btn.pack(side=tk.LEFT)

        self.window.bind("<Double-Button-1>", self.on_double_click)

        self.seen_pids = set()

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

    def run(self):
        self.window.mainloop()

# Example usage:
if __name__ == "__main__":
    debugger = PIDDebugger()
    debugger.run()
