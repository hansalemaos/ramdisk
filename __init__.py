import ctypes
import shutil
import string
import subprocess
from math import ceil

windll = ctypes.LibraryLoader(ctypes.WinDLL)
user32 = windll.user32
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def get_drives() -> list:
    """
    Retrieves a list of available drive letters.

    Returns:
        list: List of available drive letters.
    """
    bitmask = windll.kernel32.GetLogicalDrives()
    drives = []
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


def exe_subprocess(*args, **kwargs) -> subprocess.Popen:
    r"""
    Executes a subprocess command invisibly.

    Args:
        *args: Positional arguments to pass to subprocess.run().
        **kwargs: Keyword arguments to pass to subprocess.run().

    Returns:
        subprocess.Popen: A Popen object representing the executed subprocess.
    """
    return subprocess.run(*args, **kwargs, capture_output=True, **invisibledict)


imdiskexe = shutil.which("imdisk.exe")
if not imdiskexe:
    i = ""
    while i not in ["n", "y"]:
        i = input("imdisk.exe not found! Install? [y/n]").strip().lower()
    if i == "y":
        from getfilenuitkapython import get_filepath

        installimdisk = get_filepath("install_imdisk.bat")
        exe_subprocess(installimdisk)
        imdiskexe = shutil.which("imdisk.exe")


def _formatdr(drive_letter: str) -> str:
    r"""
    Formats a drive letter string.

    Args:
        drive_letter (str): The drive letter to format.

    Returns:
        str: Formatted drive letter.
    """
    return drive_letter.rstrip(": ").upper()


def create_hd(size_in_megabyte: int = 1024, drive_letter: str = "Z", fs: str = "ntfs"):
    r"""
    Creates a virtual hard drive.

    Args:
        size_in_megabyte (int): Size of the hard drive in megabytes.
        drive_letter (str): Drive letter to assign to the hard drive.
        fs (str): File system to format the hard drive with.

    Returns:
        subprocess.Popen: A Popen object representing the executed subprocess.
    """
    drive_letter = _formatdr(drive_letter)
    return exe_subprocess(
        [
            imdiskexe,
            "-a",
            "-s",
            f"{ceil(size_in_megabyte)}M",
            "-m",
            f"{drive_letter}:",
            "-p",
            f"/fs:{fs} /q /y",
        ]
    )




def add_mb_to_hd(drive_letter:str, size_in_megabyte:int=1024)->subprocess.Popen:
    r"""
    Adds additional megabytes to a virtual hard drive.

    Args:
        drive_letter (str): Drive letter of the hard drive.
        size_in_megabyte (int): Size in megabytes to add to the hard drive.

    Returns:
        subprocess.Popen: A Popen object representing the executed subprocess.
    """
    drive_letter = _formatdr(drive_letter)
    return exe_subprocess(
        [imdiskexe, "-e", "-s", f"{ceil(size_in_megabyte)}M", "-m", f"{drive_letter}:"]
    )


def remove_hd(drive_letter: str, force: bool = True) -> subprocess.Popen:
    r"""
    Removes a virtual hard drive.

    Args:
        drive_letter (str): Drive letter of the hard drive.
        force (bool): Flag indicating whether to force detachment. Default is True.

    Returns:
        subprocess.Popen: A Popen object representing the executed subprocess.
    """
    drive_letter = _formatdr(drive_letter)
    detachletter = "-d"
    if force:
        detachletter = detachletter.upper()
    return exe_subprocess([imdiskexe, detachletter, "-m", f"{drive_letter}:"])


def remove_all_hds(force: bool = True) -> None:
    r"""
    Removes all virtual hard drives.

    Args:
        force (bool): Flag indicating whether to force detachment. Default is True.
    """
    for d in get_drives():
        remove_hd(drive_letter=d, force=force)


def list_hds() -> list:
    r"""
    Lists all virtual hard drives.

    Returns:
        list: List of virtual hard drives.
    """
    return [
        x.strip().decode("utf-8", "ignore")
        for x in exe_subprocess([imdiskexe, "-l"]).stdout.strip().splitlines()
    ]

