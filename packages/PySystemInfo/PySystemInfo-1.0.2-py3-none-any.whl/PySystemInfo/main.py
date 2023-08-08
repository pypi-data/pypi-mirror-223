import platform
import psutil
import subprocess
import cpuinfo
import socket
import GPUtil

def get_motherboard_info():
    try:
        result = subprocess.check_output(['wmic', 'baseboard', 'get', 'Manufacturer,Product']).decode('utf-8')
        lines = result.strip().splitlines()
        if len(lines) >= 2:
            manufacturer, product = lines[1].split(None, 1)
            return manufacturer, product
        else:
            return None, None
    except Exception as e:
        print(f"Error occurred while getting the motherboard info: {e}")
        return None, None

def get_ram_info():
    memory_info = psutil.virtual_memory()
    return memory_info.total / (1024 ** 3), memory_info.available / (1024 ** 3)

def get_disk_info():
    for partition in psutil.disk_partitions():
        if 'fixed' in partition.opts or 'rw' in partition.opts:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                yield (partition.device, partition.mountpoint, partition.fstype, 
                       usage.total / (1024 ** 3), usage.used / (1024 ** 3))
            except PermissionError:
                continue

def get_network_info():
    net_info = [(interface, addr.address) for interface, addrs in psutil.net_if_addrs().items() 
                for addr in addrs if addr.family == socket.AF_INET]
    return net_info

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        return [(gpu.name, gpu.memoryTotal, gpu.memoryUsed, gpu.memoryFree, 
                 gpu.load * 100, (gpu.memoryUsed / gpu.memoryTotal) * 100) for gpu in gpus]
    except Exception as e:
        print(f"Error occurred while getting graphics card info: {e}")
        return []

def print_system_info():
    
    print("OS information:")
    print("Operating System:", platform.system())
    print("OS version:", platform.version())
    print("OS build:", platform.release())
    print("Computer architecture:", platform.machine())
    print("Processor name:", platform.processor())

    print("\nCPU information:")
    print("CPU Core count:", psutil.cpu_count(logical=False))
    print("CPU Thread count:", psutil.cpu_count(logical=True))
    print("CPU Usage (%):", psutil.cpu_percent(interval=1))

    print("\nMemory information:")
    total_ram, available_ram = get_ram_info()
    print("Total RAM capacity (GB):", total_ram)
    print("Available RAM capacity (GB):", available_ram)

    print("\nDisk information:")
    for disk in get_disk_info():
        print(f"Device: {disk[0]}, Mount: {disk[1]}, File system: {disk[2]}, Capacity (GB): {disk[3]}, Usage (GB): {disk[4]}")

    print("\nNetwork information:")
    for net_info in get_network_info():
        print(f"Interface: {net_info[0]}, IPv4 Address: {net_info[1]}")

    m_board_manufacturer, m_board_product = get_motherboard_info()
    print("\nMotherboard information:")
    print("Motherboard manufacturer:", m_board_manufacturer)
    print("Motherboard model:", m_board_product)

    cpu_info = cpuinfo.get_cpu_info()
    print("\nProcessor information:")
    print("Processor manufacturer:", cpu_info.get('vendor_id_raw', 'Unknown'))
    print("Processor model:", cpu_info.get('brand_raw', 'Unknown'))

    print("\nGraphics card information:")
    gpus = get_gpu_info()

    if not gpus:
        print("None GPU")
    else:
        for i, gpu in enumerate(gpus):
            print(f"------ GPU {i + 1} ------")
            print(f"Model: {gpu[0]}")
            print(f"Total memory (MB): {gpu[1]}")
            print(f"Used memory (MB): {gpu[2]}")
            print(f"Free memory (MB): {gpu[3]}")
            print(f"GPU usage (%): {gpu[4]}%")
            print(f"Memory usage (%): {gpu[5]}%")