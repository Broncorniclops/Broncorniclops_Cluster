import os
import subprocess

SCHEDULE_FILE = "/home/pi/.cluster_update_schedule"
CRON_LINE = "@daily /bin/bash /home/pi/update_cluster.sh # auto_update_cluster"

def clear_existing_cron():
    try:
        crontab = subprocess.check_output(['crontab', '-l'], stderr=subprocess.DEVNULL).decode()
    except subprocess.CalledProcessError:
        crontab = ""
    lines = [line for line in crontab.split('\n') if "auto_update_cluster" not in line]
    return lines

def write_crontab(lines):
    with open("/tmp/cron_temp", "w") as f:
        f.write('\n'.join(lines) + '\n')
    subprocess.run(["crontab", "/tmp/cron_temp"])
    os.remove("/tmp/cron_temp")

def apply_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        return

    with open(SCHEDULE_FILE, "r") as f:
        mode = f.read().strip()

    lines = clear_existing_cron()

    if mode == "daily":
        lines.append("@daily /bin/bash /home/pi/update_cluster.sh # auto_update_cluster")
    elif mode == "weekly":
        lines.append("@weekly /bin/bash /home/pi/update_cluster.sh # auto_update_cluster")

    write_crontab(lines)

if __name__ == "__main__":
    apply_schedule()