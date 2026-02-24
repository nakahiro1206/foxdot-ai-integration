from src.fs import FileSystem, FileSystemWatcher
from src.agent import MucisComposerService
from src.process import ProcessManager
import streamlit as st
from typing import Literal, overload

fs = FileSystem()
fs_watcher = FileSystemWatcher()
process_manager = ProcessManager()
music_composer_service = MucisComposerService(fs=fs)


# Define type hints for get_resource function
@overload
def get_resource(resource_type: Literal["FileSystem"]) -> FileSystem: ...
@overload
def get_resource(resource_type: Literal["FileSystemWatcher"]) -> FileSystemWatcher: ...
@overload
def get_resource(
    resource_type: Literal["MucisComposerService"],
) -> MucisComposerService: ...
@overload
def get_resource(resource_type: Literal["ProcessManager"]) -> ProcessManager: ...


@st.cache_resource
def get_resource(resource_type):  # type: ignore[no-redef]
    if resource_type == "FileSystem":
        return fs
    elif resource_type == "FileSystemWatcher":
        return fs_watcher
    elif resource_type == "MucisComposerService":
        return music_composer_service
    elif resource_type == "ProcessManager":
        return process_manager
    else:
        raise ValueError(f"Unknown resource type: {resource_type}")
