# PySystemInfo
- It's a package that allows you to easily find out the system information of your computer through Python
> PYPI : https://pypi.org/project/PySystemInfo/
# PiP install
```
pip install PySystemInfo
```
# Key Features
> [OS Information]
```python
PySystemInfo.platform.system() : OS
PySystemInfo.platform.version() : OS Version
PySystemInfo.platform.release() : OS Release
PySystemInfo.platform.machine() : OS Architecture
PySystemInfo.platform.processor() : Processor Name
```
> [CPU Information]
```python
PySystemInfo.psutil.cpu_count(logical=False) : CPU Core Count
PySystemInfo.psutil.cpu_count(logical=True) : CPU Thread Count
PySystemInfo.psutil.cpu_percent(interval=1) : CPU Usage
```
> [Memory Information]
```python
PySystemInfo.get_ram_info() : return count : 2
0 : Total_ram
1 : Available_ram
```
> [Disk Information]
```python
PySystemInfo.get_disk_info() : return count : 5
0 : Device
1 : Mount
2 : File System
3 : Capacity
4 : Usage
```
> [Network Information]
```python
PySystemInfo.get_network_info() : return count : 2
0 : Interface
1 : IPv4 Address
```
> [Motherboard Information]
```python
PySystemInfo.get_motherboard_info() : return count : 2
0 : Manufacturer
1 : Model
```
> [Processor Information]
```python
PySystemInfo.cpuinfo.get_cpu_info().get('vendor_id_raw') : Vendor ID
PySystemInfo.cpuinfo.get_cpu_info().get('hardware_raw') : Hardware
PySystemInfo.cpuinfo.get_cpu_info().get('brand_raw') : Brand
PySystemInfo.cpuinfo.get_cpu_info().get('hz_advertised_friendly') : Hz Advertised Friendly
PySystemInfo.cpuinfo.get_cpu_info().get('hz_actual_friendly') : Hz Actual Friendly
PySystemInfo.cpuinfo.get_cpu_info().get('hz_advertised') : Hz Advertised
PySystemInfo.cpuinfo.get_cpu_info().get('hz_actual') : Hz Actual
PySystemInfo.cpuinfo.get_cpu_info().get('arch') : Arch
PySystemInfo.cpuinfo.get_cpu_info().get('bits') : Bits
PySystemInfo.cpuinfo.get_cpu_info().get('count') : Count
PySystemInfo.cpuinfo.get_cpu_info().get('arch_string_raw') Arch String Raw
PySystemInfo.cpuinfo.get_cpu_info().get('l1_data_cache_size') : L1 Data Cache Size
PySystemInfo.cpuinfo.get_cpu_info().get('l1_instruction_cache_size') : L1 Instruction Cache Size
PySystemInfo.cpuinfo.get_cpu_info().get('l2_cache_size') : L2 Cache Size
PySystemInfo.cpuinfo.get_cpu_info().get('l2_cache_line_size') : L2 Cache Line Size
PySystemInfo.cpuinfo.get_cpu_info().get('l2_cache_associativity') : L2 Cache Associativity
PySystemInfo.cpuinfo.get_cpu_info().get('l3_cache_size') : L3 Cache Size
PySystemInfo.cpuinfo.get_cpu_info().get('stepping') : Stepping
PySystemInfo.cpuinfo.get_cpu_info().get('model') : Model
PySystemInfo.cpuinfo.get_cpu_info().get('family') : Family
PySystemInfo.cpuinfo.get_cpu_info().get('processor_type') : Processor Type
PySystemInfo.cpuinfo.get_cpu_info().get('flags') : Flags
```
> [Graphics Card Information]
```python
PySystemInfo.get_gpu_info : return : 6
0 : Model
1 : Total Memory
2 : Used Memory
3 : Free Memory
4 : GPU Usage
5 : Memory usage
```

# Example
```python
import PySystemInfo

print(PySystemInfo.print_system_info())
```
```python
import PySystemInfo

print(PySystemInfo.get_ram_info())
```
# ETC
> For improvements, please call Full Requests
> 
> Mail : gms8757@naver.com