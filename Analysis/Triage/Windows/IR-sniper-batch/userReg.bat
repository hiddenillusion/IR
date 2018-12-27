@echo off
:: IR Sniper Script created by:
:: 		Glenn P. Edwards Jr.
:: https://hiddenillusion.github.com
::       @hiddenillusion
:: Version 0.1
:: Date: 2013-11-19
:: (while at FireEye)

::userReg
FOR /f "tokens=*" %%a IN ('reg query "hklm\software\microsoft\windows nt\currentversion\profilelist"^| findstr "S-1-5-21"') DO CALL :REGCHECK "%%a"

:REGCHECK
	set SPACECHECK=
	FOR /f "tokens=3,4,5" %%b in ('reg query %1 /v ProfileImagePath') DO SET USERREGPATH=%%b %%c %%d

	FOR /f "tokens=2" %%e in ('echo %USERREGPATH%') DO SET SPACECHECK=%%e
	IF ["%SPACECHECK%"]==[""] (GOTO REGCHECK2) ELSE (GOTO USERCHECK)

:REGCHECK2
	FOR /f "tokens=3" %%h in ('reg query %1 /v ProfileImagePath') DO SET USERREGPATH=%%h
	GOTO USERCHECK

:USERCHECK
	FOR /f "tokens=3 delims=\" %%f in ('echo %USERREGPATH%') DO SET USERREG=%%f
	GOTO User_Reg_Extract

:User_Reg_Extract
	for /F "tokens=*" %%a in ('echo %USERREGPATH%') do set newpath=%%a
	::ECHO    [.] %USERREG%
	Tools\%tool_prefix%FGET.exe -extract "%newpath%\NTUSER.DAT" %dirname%\%computername%_reg_NTUSER_%USERREG%
	Tools\%tool_prefix%FGET.exe -extract "%newpath%\AppData\Local\Microsoft\Windows\UsrClass.dat" %dirname%\%computername%_reg_UsrClass_%USERREG%
