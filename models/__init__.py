#!/usr/bin/python3
"""
This module contains an instance of FileStorage and uses reload() method on it
"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
