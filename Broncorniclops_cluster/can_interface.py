
import can
import time
import threading
from pid_manager import PIDManager

PID_NAMES = {
    "0C": "RPM",
    "0D": "Speed",
    "05": "Coolant Temp",
    "0F": "Intake Temp",
    "10": "MAF",
    "2F": "Fuel Level",
    "11": "Throttle Position",
    "1F": "Run Time",
    "46": "Ambient Air Temp",
    "00": "Supported PIDs 01-20",
    "20": "Supported PIDs 21-40",
    "40": "Supported PIDs 41-60",
    "60": "Supported PIDs 61-80"
}

class CANInterface:
    def __init__(self):
        self.sensor_manager = None
        self.debugger = None
        self.bus = None
        self.running = False
        self.tracked_pids = set()
        self.pid_manager = PIDManager()

    def start(self):
        try:
            self.bus = can.interface.Bus(channel='can0', bustype='socketcan')
            self.bus.set_filters([{"can_id": 0x000, "can_mask": 0x000}])
            print("CAN interface started on can0")
            self.running = True
            threading.Thread(target=self.read_loop, daemon=True).start()
            self.auto_detect_pids()
            threading.Thread(target=self.send_requests_loop, daemon=True).start()
        except Exception as e:
            print("CAN bus init failed:", e)

    def read_loop(self):
        while self.running:
            msg = self.bus.recv()
            if msg is None or not msg.data:
                continue
            self.process_frame(msg.arbitration_id, list(msg.data))

    def send_requests_loop(self):
        while self.running:
            for pid in sorted(self.tracked_pids):
                try:
                    data = [0x02, 0x01, int(pid, 16)] + [0x00]*5
                    msg = can.Message(arbitration_id=0x7DF, data=data, is_extended_id=False)
                    self.bus.send(msg)
                    time.sleep(0.05)
                except Exception as e:
                    print("CAN request send error:", e)
            time.sleep(1)

    def auto_detect_pids(self):
        supported = set()
        for pid_query in [0x00, 0x20, 0x40, 0x60]:
            try:
                data = [0x02, 0x01, pid_query] + [0x00] * 5
                msg = can.Message(arbitration_id=0x7DF, data=data, is_extended_id=False)
                self.bus.send(msg)
                time.sleep(0.1)

                response = self.bus.recv(timeout=1)
                if response is None or response.arbitration_id not in [0x7E8, 0x7E9]:
                    continue
                data = list(response.data)
                if data[1] != 0x41 or data[2] != pid_query:
                    continue
                bitfield = data[3:7]
                for i in range(32):
                    if bitfield[i // 8] & (1 << (7 - (i % 8))):
                        pid = pid_query + 1 + i
                        pid_hex = f"{pid:02X}"
                        supported.add(pid_hex)
                        label = PID_NAMES.get(pid_hex, "Unknown PID")
                        print(f"Detected PID 0x{pid_hex}: {label}")
                        self.pid_manager.register_pid(pid_hex, label)
            except Exception as e:
                print("PID auto-detect error:", e)

        self.tracked_pids = supported

    def process_frame(self, frame_id, data):
        if len(data) < 3:
            return
        mode = data[1]
        pid = f"{data[2]:02X}"
        if mode != 0x41:
            return

        decoded_value = self.decode_pid(pid, data[3:])
        if self.sensor_manager:
            self.sensor_manager.update_from_can(pid, decoded_value)
        if self.debugger:
            self.debugger.add_entry(frame_id, pid, data, decoded_value)

    def decode_pid(self, pid, data_bytes):
        try:
            if pid == "0C": return (data_bytes[0] * 256 + data_bytes[1]) // 4
            elif pid == "0D": return data_bytes[0]
            elif pid == "05": return data_bytes[0] - 40
            elif pid == "0F": return data_bytes[0] - 40
            elif pid == "10": return (data_bytes[0] * 256 + data_bytes[1]) / 100
            elif pid == "2F": return data_bytes[0] * 100 / 255
            elif pid == "11": return data_bytes[0] * 100 / 255
            elif pid == "1F": return data_bytes[0] * 256 + data_bytes[1]
            elif pid == "46": return data_bytes[0] - 40
            else: return f"0x{''.join(format(b, '02X') for b in data_bytes)}"
        except:
            return "decode error"
