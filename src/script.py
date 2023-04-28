import csv
import re
from datetime import datetime, timedelta

def parse_log(file_path):
    connections = []

    with open(file_path, 'r') as log_file:
        for line in log_file:
            if "sslvpn" in line and "vpntunnel" in line:
                timestamp_str = re.search(r"\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} (?:AM|PM)", line).group()
                timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M:%S %p")
                connections.append(("start", timestamp))
            elif "Ras: connection to fortissl terminated" in line:
                timestamp_str = re.search(r"\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} (?:AM|PM)", line).group()
                timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M:%S %p")
                connections.append(("end", timestamp))

    return connections

def create_csv_files(connections):
    daily_connections = {}
    daily_durations = {}

    i = 0
    while i < len(connections):
        if connections[i][0] == "start" and i + 1 < len(connections) and connections[i + 1][0] == "end":
            start, end = connections[i][1], connections[i + 1][1]
            day = start.date()

            if day not in daily_connections:
                daily_connections[day] = []
                daily_durations[day] = timedelta()

            daily_connections[day].append((start, end))
            daily_durations[day] += end - start

            i += 2
        else:
            i += 1

    with open("connections.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["day", "start", "end"])

        for day, connections in daily_connections.items():
            for start, end in connections:
                writer.writerow([day, start.time(), end.time()])

    with open("durations.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["day", "duration"])

        for day, duration in daily_durations.items():
            writer.writerow([day, duration])

if __name__ == "__main__":
    log_file_path = "logs/log6.log"
    connections = parse_log(log_file_path)
    create_csv_files(connections)
