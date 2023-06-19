import os
import pwd
import platform
import psutil
import json
import sys
from subprocess import run, PIPE


def getPlatformInfo():
    operating_sys = platform.system()
    
    with open('/etc/os-release', 'r') as file:
        distro = file.readline()[12::].strip('\n').strip('"')

    architecture = platform.architecture()[0]
    computer_name = platform.node()
    username = pwd.getpwuid(os.getuid()).pw_name
    
    return operating_sys, distro, architecture, computer_name, username


def get_local_ip_addr():
    get_local_ip_command = "hostname -I | awk '{print $1}'"
    local_ip_addr = run(get_local_ip_command, stdout=PIPE, shell=True).stdout.decode('UTF-8').strip('\n')
    
    return local_ip_addr


def getProcessorInfo():
    with open('/proc/cpuinfo', 'r') as file:
        lines = file.readlines()
        cpuLine = lines[4]
        cpuName = cpuLine[13::].strip('\n')
            
        return cpuName


def getResourceUsage():
    cpuUsagePercentage = str(psutil.cpu_percent(interval=0.5)) + '%'
    cpuThreadCount = str(psutil.cpu_count())
    cpuFrequency = str(psutil.cpu_freq()[0]*(10**-3))[:4:] + " Ghz"

    memoryFullInfo = psutil.virtual_memory()
    memoryTotal = str(memoryFullInfo[0]*(10**-9))[:4] + " Gb"
    memoryUsed = str(memoryFullInfo[3]*(10**-9))[:4] + " Gb"

    rootPartitionInfo = psutil.disk_usage('/')
    rootPartitionTotal = str(rootPartitionInfo[0]*(10**-9))[:4] + " Gb"
    rootPartitionUsed = str(rootPartitionInfo[1]*(10**-9))[:4] + " Gb"

    return cpuUsagePercentage, cpuThreadCount, cpuFrequency, memoryTotal, memoryUsed, rootPartitionTotal, rootPartitionUsed


def create_json(path):
    json_path = os.path.join(path, 'LinuxSystemInfo.json')

    data = {
        "Operating System": getPlatformInfo()[0],
        "Distro": getPlatformInfo()[1],
        "Architecture": getPlatformInfo()[2],
        "Computer Name": getPlatformInfo()[3],
        "User": getPlatformInfo()[4],
    
        "Processor": getProcessorInfo(),
        "CPU Usage": getResourceUsage()[0],
        "CPU Cores": getResourceUsage()[1],
        "Current CPU Frequency": getResourceUsage()[2],

        "Total Memory": getResourceUsage()[3],
        "Used Memory": getResourceUsage()[4],

        "Total Disk Size": getResourceUsage()[5],
        "Used Disk Size": getResourceUsage()[6],

        "Local IP Adress": get_local_ip_addr() 
    }

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=3)
        file.write("\n")
        print("JSON file created.")


def main(path):
    getPlatformInfo()
    get_local_ip_addr()
    getProcessorInfo()
    getResourceUsage()
    create_json(path)


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        raise Exception('You must enter a target path!')
    
    cwd = os.getcwd()
    path = args[1]
    target_path = os.path.join(cwd, path)

    main(target_path)