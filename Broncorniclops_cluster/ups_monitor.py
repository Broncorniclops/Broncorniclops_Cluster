import time
import os
import socket
import threading
import RPi.GPIO as GPIO

SHUTDOWN_DELAY = 15
SOCKET_PATH = "/tmp/ups_notify.sock"

class UPSMonitor:
    def __init__(self):
        self.last_acc_state = True
        self.shutdown_triggered = False
        self.shutdown_timer = None
        self.acc_pin = 17  # GPIO pin for ACC detection
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.acc_pin, GPIO.IN)

    def acc_state(self):
        try:
            return GPIO.input(self.acc_pin) == GPIO.HIGH
        except Exception as e:
            print("ACC signal read error:", e)
            return True

    def send_shutdown_notice(self):
        try:
            if os.path.exists(SOCKET_PATH):
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                    client.connect(SOCKET_PATH)
                    client.sendall(b"shutdown_pending")
        except Exception as e:
            print("Socket send failed:", e)

    def perform_shutdown(self):
        print("Shutting down system...")
        os.system("sudo shutdown -h now")

    def check_loop(self):
        while True:
            acc = self.acc_state()

            if not acc and self.last_acc_state:
                print("ACC off — scheduling shutdown in", SHUTDOWN_DELAY, "sec")
                self.send_shutdown_notice()
                self.shutdown_timer = threading.Timer(SHUTDOWN_DELAY, self.perform_shutdown)
                self.shutdown_timer.start()

            self.last_acc_state = acc
            time.sleep(2)

if __name__ == "__main__":
    monitor = UPSMonitor()
    monitor.check_loop()