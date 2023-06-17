# A collection of functions that interact with the imdisk.exe utility

## pip install ramdisk


The provided module provides a collection of functions that interact with the imdisk.exe utility, which is a third-party tool for creating and managing virtual disk drives in Windows.

The advantages of using this module and the imdisk.exe utility include:

### Creating virtual hard drives: 

The module allows you to create virtual hard drives of specified sizes and file systems, which can be useful for various purposes such as testing, virtualization, or creating temporary storage.

### Adding capacity to virtual hard drives: 

The module provides a function to add additional capacity (in megabytes) to existing virtual hard drives. This allows you to dynamically increase the storage space of a virtual drive without recreating it.

### Removing virtual hard drives: 

The module offers the ability to remove virtual hard drives. This allows you to free up system resources by removing unnecessary virtual drives when they are no longer needed.

### Listing virtual hard drives: 

The module provides a function to list all currently existing virtual hard drives. This can be useful for obtaining information about the virtual drives present in the system.

### Invisible execution: 

The module utilizes the subprocess module to execute commands invisibly, without displaying any console windows. This can be beneficial when performing automated or background tasks that don't require user interaction.



### Tested against Windows 10 / Python 3.10 / Anaconda 3

The scan_processes function can be useful for system administrators, security analysts, or anyone who needs to perform a comprehensive scan and analysis of running processes on a Windows system. Here are some advantages of using this code:

Process scanning: The function allows users to scan processes based on partial process names or regular expressions, providing flexibility in defining the target processes for analysis.

Registry filtering: Users can specify custom regular expression filters for registry keys, enabling them to include or exclude specific keys based on their patterns. This feature allows for fine-grained control over the registry data to be collected.

File filtering: The function supports filtering files based on forbidden folders and a string pattern. Users can exclude specific folders or files based on their paths, allowing them to focus on relevant files and ignore unnecessary ones.

File copying: The function facilitates copying files from the scanned processes to a specified destination folder. This can be valuable for further analysis or investigation of the files associated with the processes.

Data aggregation: The function collects registry data and file information from multiple processes and aggregates them into pandas DataFrames. This consolidated data can be easily analyzed, processed, or exported for further investigation.

Exception handling: The code includes exception handling to ensure that the scanning process continues even if exceptions are encountered. It provides the ability to gracefully handle errors and continue scanning other processes.


## Example - getting faster procdumps 

```python
from PyPDump import ProcDump # writes only to HDDs
pid=19288
dumpfile = r"Z:\MiniDumpWithFullMemoryx.dmp"

p1=create_hd(size_in_megabyte=1024, drive_letter='Z', fs='ntfs')
p2=add_mb_to_hd('Z',8048)
erg = (
            ProcDump(executeable=r"C:\ProgramData\chocolatey\bin\procdump.exe")
            .o()
            .ma()
            .add_own_parameter_or_option(f"{pid}")
            .add_target_file_or_folder([dumpfile])
            .run()
        )
alldi=list_hds()
print(alldi)
remove_hd(drive_letter='Z',force=True)
remove_all_hds(force=True)

```	