  > The intention of these scripts is to grab some key information & artifacts of forensic interest from a Windows system.

Script | Requirements | Notes
--- | --- | ---
[`WindowsTriage.py`](#WindowsTriage.py) | Python 2.7+ | External tools are not used so locked windows files still need to be acquired via other means. This script also handles Windows 2000 artifact locations.
[`IR-sniper-batch\ir_sniper.bat`](#ir_sniper.bat) | External tool downloads prior to using. | Tested on Windows XP+

# Artifact Matrix
Category | `WindowsTriage.py` | `ir_sniper.bat` | Command/Artifact | Notes
--- | --- | --- | --- | ---
Event Logs | N/A | :ballot_box_with_check: | _Application_<br>_Security_<br>_System_<br>_OAlerts_, _Microsoft-Windows-TaskScheduler%4Operational_<br>_microsoft-windows-RemoteDesktopServices-RemoteDesktopSessionManager%4Admin_<br> _Microsoft-Windows-TerminalServices-LocalSessionManager%4Operational_<br>_Windows PowerShell_ | `FGET`
Event Logs | :ballot_box_with_check: | :x: | _%windir%\System32\config_<br>_%windir%\system32\winevt\Logs_ | `shutil.copytree()`
Memory dump | :x: | :ballot_box_with_check: | | `DumpIt`
Network Information | :x: | :ballot_box_with_check: | `ipconfig` |
Network Information | :x: | :ballot_box_with_check: | `ipconfig /displaydns` |
Network Information | :ballot_box_with_check: | :ballot_box_with_check: | _%systemroot%\system32\drivers\etc\hosts_ | `shutil.copy()`<br>---<br>`FGET`
Registry Hives |:ballot_box_with_check: | :ballot_box_with_check: | _System_<br>_Security_<br>_SAM_<br>_Software_ | `shutil.copy()`<br>---<br>`FGET`
Registry Hives | :ballot_box_with_check: | :ballot_box_with_check: | each user's _NTUSER.DAT_ & _UsrClass.dat_ | `shutil.copy()`<br>---<br>`FGET`
Registry Hives | :ballot_box_with_check: | :x: | _%windir%\AppCompat\Programs\Amcache.hve_ | `shutil.copy()`
Prefetch | :ballot_box_with_check: | :ballot_box_with_check: | _%windir%\Prefetch_ |  `shutil.copytree()`<br>---<br>`xcopy` or `Robocopy64`
Shortcuts | :ballot_box_with_check: | :x: | _%appdata%\Roaming\Microsoft\Windows\Recent\AutomaticDestinations_ | `shutil.copytree()`
Shortcuts | :ballot_box_with_check: | :x: | _%appdata%\Roaming\Microsoft\Windows\Recent\CustomDestinations_ | `shutil.copytree()`
Shortcuts | :ballot_box_with_check: | :x: | _%appdata%\Roaming\Microsoft\Windows\Recent_ | `shutil.copytree()`
Scheduled Tasks | :ballot_box_with_check: | :ballot_box_with_check: | _%windir%\Tasks_ | `shutil.copytree()`<br>---<br>`xcopy` or `Robocopy64`
Scheduled Tasks | :ballot_box_with_check: | :ballot_box_with_check: | _%windir%\SchedLgU.txt_ | `shutil.copy()`<br>---<br>`FGET`
System Information | :x: | :ballot_box_with_check: | `systeminfo` |
System Information | :x: | :ballot_box_with_check: | `fsutil fsinfo drive` |
System Information | :x: | :ballot_box_with_check: | `wmic qfe list full` |
System Information | :ballot_box_with_check: | :ballot_box_with_check: | _%windir%\setupapi.log_<br>_%windir%\setupact.log_<br>_%windir%\setuperr.log_ <br>_%windir%\inf\setupapi.dev.log_ |  `shutil.copy()`<br>---<br>`FGET`
System Information | :x: | :ballot_box_with_check: | $MFT | `FGET`
Misc. | :ballot_box_with_check: | :x: | %windir%\AppCompat\Programs\RecentFileCache.bcf | `shutil.copy()`
Misc. | :ballot_box_with_check: | :x: | _%appdata%\Local\Miscrosoft\Terminal Server Client\Cache\bcache22.bmc_ | `shutil.copy()`
Misc. | :ballot_box_with_check: | :x: | _%userprofile%\Default.rdp_ | `shutil.copy()`
Misc. | :ballot_box_with_check: | :x: | _%userprofile%\ActivitiesCache.db_ | `shutil.copy()`
Misc. | :ballot_box_with_check: | :x: | _%appdata%\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt_ | `shutil.copy()`
Misc. | :x: | :ballot_box_with_check: | Recursive MD5 Hashing of C:\ | `md5deep` or `md5deep64`
Misc. | :x: | :ballot_box_with_check: | Compression of evidence once collected | `zipfile.ZipFile()`<br>---<br>`7z`

# `WindowsTriage.py`

## Usage

The main use case for this script is to point it at a mounted image to easily pull some sniper artifacts for later processing with additional tools.

1. From an elevated command prompt, run `python WindowsTriage.py`

# `ir_sniper.bat`

## Configuration

1. Create the following directories
    ```
    mkdir Tools
    mkdir Tools\x64
    ```
1. Download/Copy the following tools from the links/locations within the **Source** column
1. Rename, if applicable, said tool and place in the path according to the **Path + Required Name for Script** column

Tool | Path + Required Name for Script | Source
--- | --- | ---
`7z.exe` | `Tools\ir_7za.dll`| Console version from [7-zip.org](https://www.7-zip.org/download.html)
`7za.dll` | `Tools\7za.dll`| Console version from [7-zip.org](https://www.7-zip.org/download.html)
`DumptIt.exe` | `Tools\DumptIt.exe` | 32 bit version from [comae.io](https://my.comae.io/)
`DumptIt.exe` | `Tools\x64\DumptIt.exe` | 64 bit version from [comae.io](https://my.comae.io/)
`FGET.exe` | `Tools\ir_FGET.exe` | HBGary's FGET is no longer on their own website, but is available on [GitHub](https://github.com/MarkBaggett/srum-dump/blob/master/FGET.exe)
`md5deep.exe` | `Tools\ir_md5deep.exe` | 32 bit version from [GitHub](https://github.com/jessek/hashdeep/releases)
`md5deep64.exe` | `Tools\ir_md5deep64.exe` | [GitHub](https://github.com/jessek/hashdeep/releases)
`Robocopy64.exe` | `Tools\ir_Robocopy64.exe` | 64 bit version available within the _%windir%\SysWOW64\_ directory on a Windows system
`xcopy.exe` | `Tools\ir_xcopy.exe` | 32 bit version available within the _%windir%\System32\_ directory on a Windows system


### Notes
- Using the DMP format of `DumptIt` generated a BSOD in Windows XP SP2
- There are plenty of other programs or methods one can use to grab locked files other than FGET (`ntsfcopy`, `icat` etc.)
- Other options for memory dumping exist as well (`winpmem` etc.)

## Usage

Generally, the artifacts will be extracted for offline parsing & analysis. The main exception to this is the MD5 hashing performed on the C:\, which wouldn't otherwise be available without a full disk image. To help distinguish tasks performed via this script, the prefix `ir_` is generally applied to most `Tools\` (unless there are some terms that restrict this).

1. From an elevated command prompt, run `ir_sniper.bat`

**Note:** If you don't want to acquire a memory dump, remove the `:memAcquire` section or its reference within `:userReg`
