switchinglogfilehandlers
========================

A collection of switching log file handlers for the Python logging system.
Unlike the *rotating* log file handlers in the Python core which always
write to a file with a fixed name and peridically rename that, these
handlers always open a new file with a unique name - old files will
never be renamed.

TimedSwitchingFileHandler
-------------------------

This file handler starts a new file at regular intervals, comparable to
the TimedRotatingFileHandler.

TimeoutSwitchingFileHandler
---------------------------

This file handler automatically closes the log file after a period of
inactivity (or after the file has been open for some time whichever
comes first) and then opens a new file at the next emit.

This is useful for long-running processes where short periods of
activity alternate with periods of inactivity. Log switchse will
typically occur during inactivity, so each log file will include one
complete active period. Also, since the log files are closed, they can
be safely compressed or removed.
