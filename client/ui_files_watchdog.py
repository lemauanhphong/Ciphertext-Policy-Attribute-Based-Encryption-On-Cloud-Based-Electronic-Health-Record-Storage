#!/usr/bin/python

import logging
import os
import time

from PyQt6 import uic
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class UIFileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".ui"):
            logging.info(f"UI file {event.src_path} created, compiling...")
            self.compile(event.src_path)

    def on_moved(self, event):
        if event.dest_path.endswith(".ui"):
            logging.info(f"UI file {event.dest_path} modified, recompiling...")
            self.compile(event.dest_path)

    def compile(self, ui_file):
        py_file = os.path.splitext(ui_file)[0] + ".py"

        with open(py_file, "w") as f:
            uic.compileUi(ui_file, f)


UI_FOLDER = "."

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d:%M:%S"
)

event_handler = UIFileEventHandler()
observer = Observer()
observer.schedule(event_handler, UI_FOLDER, recursive=True)

observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
