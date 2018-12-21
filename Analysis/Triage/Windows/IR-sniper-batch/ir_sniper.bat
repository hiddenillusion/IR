@echo off
:: IR Sniper Script created by:
:: 		Glenn P. Edwards Jr.
:: https://hiddenillusion.github.com
::       @hiddenillusion
:: Version 0.1.2
:: Date: 2013-11-19
:: (while at FireEye)


:: To-Do
::	[X] delete folder with files after completion?
::	[ ] test if this script works from a share or removable media

::check perms
net session >nul 2>&1
if not %errorLevel% == 0 (
    echo Failure: Administrative rights required.
    pause >nul
)

::Change Directory to the script's one, since Stupid windows will execute at "\windows\system32" when chosen to run as administrator...
cd /d "%~d0%~p0"

::Get Date and Time
For /F "tokens=1,2,3,4 delims=/ " %%A in ('Date /t') do @(
Set FullDate="%%D-%%C-%%B"
)

For /F "tokens=1,2,3 delims=: " %%A in ('time /t') do @(
Set FullTime="%%A-%%B"
)

::set dirname="%computername%_%FullDate%_%FullTime%"
set dirname="%computername%_%FullDate%"
mkdir "%dirname%"
set tool_prefix=ir_

ECHO [+] Collection started at %DATE%  %TIME%
ECHO [+] Collection started at %DATE%  %TIME% >> %dirname%\%computername%.txt

:: Basic stuff
ECHO [+] Basic Volatile Data
ECHO [+] Basic Volatile Data >> %dirname%\%computername%.txt
ipconfig >> %dirname%\%computername%_ipconfig.txt
ipconfig /displaydns >> %dirname%\%computername%_ipconfig_dns.txt
systeminfo >> %dirname%\%computername%_systeminfo.txt

:: Will need to do some checking of the record size/UseLargeFRS because will fail on $MFT records @ 4k instead of standard 512
ECHO [-] $MFT
ECHO [-] $MFT >> %dirname%\%computername%.txt
Tools\%tool_prefix%FGET.exe -extract %systemdrive%\$MFT %dirname%\%computername%_MFT >> %dirname%\%computername%.txt

ECHO [-] Registry
ECHO [-] Extracting Registry >> %dirname%\%computername%.txt
Tools\%tool_prefix%FGET.exe -extract %windir%\system32\config\software %dirname%\%computername%_reg_software >> %dirname%\%computername%.txt
Tools\%tool_prefix%FGET.exe -extract %windir%\system32\config\system %dirname%\%computername%_reg_system >> %dirname%\%computername%.txt
Tools\%tool_prefix%FGET.exe -extract %windir%\system32\config\security %dirname%\%computername%_reg_security >> %dirname%\%computername%.txt
Tools\%tool_prefix%FGET.exe -extract %windir%\system32\config\sam %dirname%\%computername%_reg_sam >> %dirname%\%computername%.txt

::cpu_check
IF "%PROCESSOR_ARCHITECTURE%"=="x86" (GOTO 32bit) ELSE (GOTO 64bit)

:32bit
	set cpu=32
	ECHO [+] CPU is 32 bit
	ECHO [+] CPU is 32 bit >> %dirname%\%computername%.txt

	ECHO [-] Prefetch
	ECHO [-] Prefetch >> %dirname%\%computername%.txt
	mkdir %dirname%\Prefetch\
	Tools\%tool_prefix%xcopy.exe /q /c /e %windir%\Prefetch  %dirname%\Prefetch >> %dirname%\%computername%.txt
	ECHO [-] Tasks
	ECHO [-] Tasks >> %dirname%\%computername%.txt
	mkdir %dirname%\Tasks\
	Tools\%tool_prefix%xcopy.exe /q /c /e %windir%\Tasks  %dirname%\Tasks >> %dirname%\%computername%.txt

	::version_check
	ver | find "Version 6." >nul
	IF %ERRORLEVEL% NEQ 0 (GOTO WinXP) ELSE (GOTO Win7)

:64bit
	set cpu=64
	ECHO [+] CPU is 64 bit
	ECHO [+] CPU is 64 bit >> %dirname%\%computername%.txt

	ECHO [-] Prefetch
	ECHO [-] Prefetch >> %dirname%\%computername%.txt
	Tools\%tool_prefix%\x64\Robocopy64.exe %windir%\Prefetch *.pf %dirname%\Prefetch >> %dirname%\%computername%.txt
	ECHO [-] Tasks
	REM for some reason I don't think this copies everything...
	ECHO [-] Tasks >> %dirname%\%computername%.txt
	Tools\%tool_prefix%\x64\Robocopy64.exe %windir%\Tasks %dirname%\Tasks /E >> %dirname%\%computername%.txt
	Tools\%tool_prefix\x64\%Robocopy64.exe %windir%\System32\Tasks %dirname%\Tasks /E >> %dirname%\%computername%.txt

	::version_check
	ver | find "Version 6." >nul
	IF %ERRORLEVEL% NEQ 0 (GOTO WinXP) ELSE (GOTO Win7)

:WinXP
	Echo [+] WinXP
	ECHO [-] Event logs
	ECHO [-] Event logs >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\config\AppEvent.Evt %dirname%\%computername%_eventLog_Application.evt >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\config\SecEvent.Evt %dirname%\%computername%_eventLog_Security.evt >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\config\SysEvent.Evt %dirname%\%computername%_eventLog_System.evt >> %dirname%\%computername%.txt

	Tools\%tool_prefix%FGET.exe -extract %windir%\SchedLgU.txt %dirname%\%computername%_SchedLgU.txt >> %dirname%\%computername%.txt

	GOTO Misc

:Win7
	ECHO [+] Win7
	ECHO [-] Event logs
	ECHO [-] Event logs >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\winevt\Logs\Application.evtx %dirname%\%computername%_eventLog_Application.evtx >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\winevt\Logs\Security.evtx %dirname%\%computername%_eventLog_Security.evtx >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\winevt\Logs\System.evtx %dirname%\%computername%_eventLog_System.evtx >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\winevt\Logs\OAlerts.evtx %dirname%\%computername%_eventLog_OAlerts.evtx >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\winevt\Logs\Microsoft-Windows-TaskScheduler%4Operational.evtx %dirname%\%computername%_eventLog_TaskScheduler.evtx >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\winevt\Logs\microsoft-windows-RemoteDesktopServices-RemoteDesktopSessionManager%4Admin.evtx %dirname%\%computername%_eventLog_RDP-SessionManager.evtx >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\System32\winevt\Logs\Microsoft-Windows-TerminalServices-LocalSessionManager%4Operational.evtx %dirname%\%computername%_eventLog_TerminalServices-LocalSessionManager.evtx >> %dirname%\%computername%.txt

	Tools\%tool_prefix%FGET.exe -extract %windir%\Tasks\SchedLgU.txt %dirname%\%computername%_SchedLgU.txt >> %dirname%\%computername%.txt
	GOTO Misc

:Misc
	ECHO [-] Misc.
	ECHO [-] Misc. >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %systemroot%\system32\drivers\etc\hosts %dirname%\%computername%_hosts.txt >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\setupapi.log %dirname%\%computername%_setupapi.log >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\setupact.log %dirname%\%computername%_setupact.log >> %dirname%\%computername%.txt
	Tools\%tool_prefix%FGET.exe -extract %windir%\setuperr.log %dirname%\%computername%_setuperr.log >> %dirname%\%computername%.txt
	::Tools\%tool_prefix%FGET.exe -extract %windir%\inf\setupapi.dev.log %dirname%\%computername%_setupapi.dev.log >> %dirname%\%computername%.txt
	GOTO userReg

:userReg
	ECHO [-] User's Registry
	ECHO [-] User's Registry >> %dirname%\%computername%.txt
	START /wait /min userReg.bat ^& EXIT
	GOTO memAcquire

:memAcquire
	ECHO [-] Memory Dump
	START /wait /min memAcquire.bat ^& EXIT
	GOTO Complete

:Complete
	ECHO [+] Collection completed at %DATE% %TIME%
	ECHO [+] Collection completed at %DATE% %TIME% >> %dirname%\%computername%.txt
	GOTO Compress

:Compress
	ECHO [+] Compressing data
	ECHO [+] Compressing data >> %dirname%\%computername%.txt
	Tools\%tool_prefix%7z.exe a %dirname%.7z %dirname%

	ECHO [+] Deleting uncompressed copy of data
	ECHO [+] Deleting uncompressed copy of data >> %dirname%\%computername%.txt
	ECHO [+] rmdir /s /q %dirname% >> %dirname%\%computername%.txt
	rmdir /s /q %dirname%
	EXIT
