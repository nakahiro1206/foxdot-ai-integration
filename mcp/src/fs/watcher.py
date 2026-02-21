from watchdog.observers import Observer
from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileSystemEventHandler,
)
from .writer import FileSystem


class UpdateHandler(FileSystemEventHandler):
    def __init__(self, fs: FileSystem) -> None:
        super().__init__()
        self.fs = fs
        self.current_files: list[str] = self.fs.list_files()

    def get_current_files(self) -> list[str]:
        # zero-computation
        return self.current_files

    def process(
        self,
        _event: DirModifiedEvent
        | FileModifiedEvent
        | DirCreatedEvent
        | FileCreatedEvent
        | DirDeletedEvent
        | FileDeletedEvent,
    ):
        # update current files
        self.current_files = self.fs.list_files()

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent):
        self.process(event)

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent):
        self.process(event)

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent):
        self.process(event)


class FileSystemWatcher:
    def __init__(self):
        self.fs = FileSystem()
        self.event_handler = UpdateHandler(self.fs)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.fs.directory, recursive=False)
        self.observer.start()

    def get_current_files(self) -> list[str]:
        return self.event_handler.get_current_files()

    def cleanup(self):
        self.observer.stop()
        self.observer.join()
