import logging
import os
import os.path
import threading
import time

class TimeoutSwitchingFileHandler(logging.Handler):
    def __init__(self, filename, min_timeout=60, max_timeout=3600, create_directory=False):
        super().__init__()
        self.basename = filename
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout
        self.create_directory = create_directory
        self.fh = None
        self.last_emit = 0
        self.first_emit = 0
        self.last_emit = 0
        cleanup = threading.Thread(target=self.cleanup_loop, daemon=True)
        cleanup.start()

    def emit(self, record):
        msg = self.format(record)
        now = time.time()
        if not self.fh:
            now_tm = time.localtime(now)
            filename = self.basename + time.strftime("%Y-%m-%d-%H-%M-%S", now_tm) + "-%06d" % (now % 1 * 1000000) + ".log"
            if self.create_directory:
                dirname = os.path.dirname(filename)
                os.makedirs(dirname, exist_ok=True)
            self.fh = open(filename, "a")
            self.first_emit = now
        self.fh.write(msg)
        self.fh.write("\n")
        self.fh.flush()
        self.last_emit = now

    def cleanup_loop(self):
        while True:
            time.sleep(1)
            self.acquire()
            now = time.time()
            if self.fh and now - self.last_emit > self.min_timeout:
                self.fh.close()
                self.fh = None
            if self.fh and now - self.first_emit > self.max_timeout:
                self.fh.close()
                self.fh = None
            self.release()

class TimedSwitchingFileHandler(logging.Handler):
    def __init__(self, filename, when='h', utc=False, create_directory=False):
        super().__init__()
        self.basename = filename
        when = when.lower()
        if when == 's':
            self.timestamp_format = "%Y-%m-%d-%H-%M-%S"
        elif when == 'm':
            self.timestamp_format = "%Y-%m-%d-%H-%M"
        elif when == 'h':
            self.timestamp_format = "%Y-%m-%d-%H"
        elif when == 'd':
            self.timestamp_format = "%Y-%m-%d"
        elif when == 'w':
            self.timestamp_format = "%Gw%V"
        else:
            raise ValueError(f"Unknown value “{when}” for when")
        self.utc = utc
        self.create_directory = create_directory
        self.current_filename = None
        self.fh = None

    def emit(self, record):
        msg = self.format(record)
        now = time.time()
        if self.utc:
            now_tm = time.gmtime(now)
        else:
            now_tm = time.localtime(now)
        new_filename =  self.basename + time.strftime(self.timestamp_format, now_tm) + ".log"
        if new_filename != self.current_filename:
            if self.fh:
                self.fh.close()
            if self.create_directory:
                new_dirname = os.path.dirname(new_filename)
                os.makedirs(new_dirname, exist_ok=True)
            self.fh = open(new_filename, "a")
            self.current_filename = new_filename
        self.fh.write(msg)
        self.fh.write("\n")
        self.fh.flush()

