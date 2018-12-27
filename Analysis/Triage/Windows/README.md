Script | Requirements | Notes
--- | --- | ---
`WindowsTriage.py` | Python 2.7+ | External tools are not used so locked windows files still need to be acquired via other means.
[`IR-sniper-batch\ir_sniper.bat`](#ir_sniper.bat) | External tool downloads prior to using. | Tested on Windows XP+

# ir_sniper.bat

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


### Notes:
- Using the DMP format of `DumptIt` generated a BSOD in Windows XP SP2
- There are plenty of other programs or methods one can use to grab locked files other than FGET (`ntsfcopy`, `icat` etc.)
- Other options for memory dumping exist as well (`winpmem` etc.)

## Usage

  > The intention of this script is to grab some key information & artifacts of forensic interest from a Windows system.

Generally, the artifacts will be extracted for offline parsing & analysis. The main exception to this is the MD5 hashing performed on the C:\, which wouldn't otherwise be available without a full disk image. To help distinguish tasks performed via this script, the prefix `ir_` is generally applied to most `Tools\` (unless there are some terms that restrict this).

1. From an elevated command prompt, run `ir_sniper.bat` . By default, the following will be collected:

- [x] Network information
  - `ipconfig`
  - `ipconfig /displaydns`
  - _%systemroot%\system32\drivers\etc\hosts_ via `FGET`
- [x] System Information
  - `systeminfo`
  - `fsutil fsinfo drives`
  - `wmic qfe list full`
  - _%windir%\setupapi.log_, _%windir%\setupact.log_, _%windir%\setuperr.log_ & _%windir%\inf\setupapi.dev.log_ via `FGET`
- [x] $MFT
  - via `FGET`
- [x] Registry Hives
  - _System_, _Security_, _SAM_ & _Software_ via `FGET`
  - each user's _NTUSER.DAT_ & _UsrClass.dat_ via `FGET`
- [x] Prefetch
  - via `xcopy` or `Robocopy64`
- [x] Scheduled Tasks
  - via `xcopy` or `Robocopy64`
- [x] Event Logs
  - _Application_, _Security_ & _System_ via `FGET`
  - _Application_, _Security_, _System_, _OAlerts_, _Microsoft-Windows-TaskScheduler%4Operational_, _microsoft-windows-RemoteDesktopServices-RemoteDesktopSessionManager%4Admin_, _Microsoft-Windows-TerminalServices-LocalSessionManager%4Operational_ & _Windows PowerShell_ via `FGET`
- [x] Recursive MD5 Hashing of C:\
  - via `md5deep` or `md5deep64`
- [x] Memory dump
  - via `DumpIt`
- [x] All results compressed via `7z`

**Note:** If you don't want to acquire a memory dump, remove the `:memAcquire` section or its reference within `:userReg`
