@echo off
REM (For Windows) Open RUN and type
REM shell:sendto
REM and paste this file there - to download subtitles from the context menu.
cls
IF %1=="" GOTO completed
	subgrab -m %~n1 -c 2
:completed
