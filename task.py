import csv
import os

directory = './logs/logs/'

class Date_And_Time:
    # Log contains date in "Month/Day Time" format
    def __init__(self, date_portion):
        date_portion = date_portion.split()
        # Convert date to [month, day]
        d = date_portion[0].split('/')
        self.month = int(d[0])
        self.day = int(d[1])

        d = date_portion[1].split(':')
        self.hour = int(d[0])
        self.minute = int(d[1])
        self.seconds = int(d[2])
    
    # Overloading the <= operator 
    def __le__(self, other):
        if self.month != other.month:
            return self.month <= other.month
        if self.day != other.day:
            return self.day <= other.day
        if self.hour != other.hour:
            return self.hour <= other.hour
        if self.minute != other.minute:
            return self.minute <= other.minute
        return self.seconds <= other.seconds

class Log_Entry:
    log_type = -1
    def __init__(self, s):
        s = s.split('|')
        name_portion = s[0].strip()
        date_portion = s[1].strip()
        type_portion = s[2].strip()

        name_portion = name_portion.split()
        # Assume that id is always 4 characters long
        self.log_id = name_portion[0][1:5]
        self.log_name = name_portion[1].split(':')[1]

        # Remove brackets ( and ) from date and time
        date_portion = date_portion[1:-1]
        self.log_date = Date_And_Time(date_portion)

        # 0 for drop
        # 1 for disconnections
        # 2 for average
        type_portion = type_portion.lower()
        if "drop" in type_portion:
            self.log_type = 0
        elif "disconnected" in type_portion:
            self.log_type = 1
        elif "average" in type_portion:
            self.log_type = 2

def generate_report():
    print('Input dates in MM/DD HH:MM:SS format')
    print('Enter Date 1: ')
    L = Date_And_Time(input())
    print('Enter Date 2: ')
    R = Date_And_Time(input())
    if R <= L:   # swap
        L, R = R, L
    mp = {}     # maps ids to names
    dict = [{}, {}, {}]     # dictionaries for disconnects, drop, avg

    # For every file in directory
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            with open(directory + filename) as f:
                # Remove blank lines
                log_file = [l for l in (line.strip() for line in f) if l]
                # For every line in .log file
                for line in log_file:
                    obj = Log_Entry(line)
                    if L <= obj.log_date <= R:
                        mp[obj.log_id] = obj.log_name
                        if obj.log_id not in dict[obj.log_type]:
                            dict[obj.log_type][obj.log_id] = 1
                        else:
                            dict[obj.log_type][obj.log_id] = dict[obj.log_type][obj.log_id] + 1
    
    # Generating reports to .csv files
    with open('./drops_report.csv', 'w', encoding='UTF8', newline='') as f:
        header = ['Computer Name', 'Number of Disconnects']
        writer = csv.writer(f)
        writer.writerow(header)
        for i in dict[0]:
            data = [mp[i], dict[0][i]]
            writer.writerow(data)
    
    with open('./disconnections_report.csv', 'w', encoding='UTF8', newline='') as f:
        header = ['Computer Name', 'Number of Disconnects']
        writer = csv.writer(f)
        writer.writerow(header)
        for i in dict[1]:
            data = [mp[i], dict[1][i]]
            writer.writerow(data)
    
    with open('./averages_report.csv', 'w', encoding='UTF8', newline='') as f:
        header = ['Computer Name', 'Number of Disconnects']
        writer = csv.writer(f)
        writer.writerow(header)
        for i in dict[2]:
            data = [mp[i], dict[2][i]]
            writer.writerow(data)

if __name__ == "__main__":
    generate_report()