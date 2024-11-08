"""
UI components for the Dama UI application.

This package contains the main chat interface and artifact window classes.
These components are responsible for rendering the user interface and handling
user interactions in the Dama UI application.
"""

from .chat_interface import ChatGPTStyleInterface
from .artifact_window import ArtifactWindow

__all__ = [
    'ChatGPTStyleInterface',
    'ArtifactWindow',
]

# You can add any package-level initialization code here if needed.
# For example:
#
# def initialize_ui():
#     """Initialize any UI-related resources or settings."""
#     pass
#
# initialize_ui()

# If you have any shared UI constants or utility functions,
# you can define them here as well:
#
# DEFAULT_WINDOW_SIZE = (800, 600)
#
# def create_standard_button(parent, text, command):
#     """Create a button with standard styling."""
#     from tkinter import ttk
#     return ttk.Button(parent, text=text, command=command)