@echo off
:: IR Sniper Script created by:
:: 		Glenn P. Edwards Jr.
:: https://hiddenillusion.github.com
::       @hiddenillusion
:: Version 0.1
:: Date: 2013-11-19
:: (while at FireEye)

set dirname="%computername%_%FullDate%"

:: Choose the program to dump the systems memory
SET mem_dumper=DumpIt.exe
ECHO Tools\%mem_dumper% /Q /N /T RAW /O %dirname%\%computername%.raw >> %dirname%\%computername%.txt

IF "%PROCESSOR_ARCHITECTURE%"=="x86" (
  START /wait Tools\%mem_dumper% /Q /N /T RAW /O %dirname%\%computername%.raw
) ELSE (
  START /wait Tools\x64\%mem_dumper% /Q /N /T RAW /O %dirname%\%computername%.raw
)
