import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ttkthemes import ThemedTk
import asyncio
import threading
from collections import deque
import os

from .artifact_window import ArtifactWindow
from utils.request_processor import process_request
from utils.token_counter import count_tokens
from config.model_limits import MODEL_LIMITS

class ChatGPTStyleInterface(ThemedTk):
    def __init__(self, api_key):
        super().__init__(theme="equilux")
        self.title("Dama UI")
        self.geometry("1280x720")

        self.api_key = api_key
        self.conversation_history = deque(maxlen=30)
        self.total_tokens = 0
        self.max_tokens = 4000
        self.artifacts = {}

        self.create_widgets()

        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.loop_thread.start()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_chat_display(left_frame)
        self.create_input_area(left_frame)
        self.create_sidebar(right_frame)

    def create_chat_display(self, parent):
        self.chat_display = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=30)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=(0, 10))
        self.chat_display.config(state=tk.DISABLED)

    def create_input_area(self, parent):
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, pady=(10, 0))

        self.user_input = ttk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)

        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=(10, 0))

    def create_sidebar(self, parent):
        self.model_var = tk.StringVar(value="gemma-7b-it")
        model_label = ttk.Label(parent, text="Model:")
        model_label.pack(pady=(0, 5))
        model_menu = ttk.OptionMenu(parent, self.model_var, "gemma-7b-it", *MODEL_LIMITS.keys())
        model_menu.pack(fill=tk.X, pady=(0, 10))

        self.system_message = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=10, width=30)
        self.system_message.pack(fill=tk.X, pady=(0, 10))
        self.system_message.insert(tk.END, "You are a helpful AI assistant.")

        clear_button = ttk.Button(parent, text="Clear Chat", command=self.clear_chat)
        clear_button.pack(fill=tk.X)

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip() == "":
            return

        self.display_message("You", user_message)
        self.user_input.delete(0, tk.END)

        self.add_to_history({"role": "user", "content": user_message})
        self.get_ai_response_async(self.model_var.get(), user_message, self.system_message.get("1.0", tk.END).strip())

    def display_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def add_to_history(self, message):
        self.conversation_history.append(message)
        self.total_tokens += count_tokens(message["content"])
        while self.total_tokens > self.max_tokens and len(self.conversation_history) > 1:
            removed_message = self.conversation_history.popleft()
            self.total_tokens -= count_tokens(removed_message["content"])

    def get_ai_response_async(self, model, prompt, system_message):
        self.display_message("AI", "Thinking...")
        asyncio.run_coroutine_threadsafe(self.get_ai_response(model, prompt, system_message), self.loop)

    async def get_ai_response(self, model, prompt, system_message):
        messages = [{"role": "system", "content": system_message}] + list(self.conversation_history)
        try:
            response = await process_request(self.api_key, model, messages)
        except Exception as e:
            response = f"An error occurred: {str(e)}"

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", "end-1c")  # Remove "AI is thinking..." message
        self.chat_display.config(state=tk.DISABLED)

        self.display_message("AI", response)
        self.add_to_history({"role": "assistant", "content": response})

        self.check_for_artifacts(response)

    def check_for_artifacts(self, response):
        artifact_types = {"code": "code", "text": "text", "html": "html"}
        for artifact_type, content_type in artifact_types.items():
            if f"<{artifact_type}>" in response and f"</{artifact_type}>" in response:
                start = response.index(f"<{artifact_type}>") + len(artifact_type) + 2
                end = response.index(f"</{artifact_type}>")
                content = response[start:end].strip()
                artifact_id = f"{artifact_type}_artifact_{len(self.artifacts) + 1}"
                
                # Save artifact to file
                artifacts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'artifacts')
                os.makedirs(artifacts_dir, exist_ok=True)
                file_path = os.path.join(artifacts_dir, f"{artifact_id}.{content_type}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.artifacts[artifact_id] = {"type": content_type, "content": content, "file_path": file_path}
                self.display_artifact(artifact_id, f"{artifact_type.capitalize()} Artifact", content, content_type)

    def display_artifact(self, artifact_id, title, content, content_type):
        artifact_window = ArtifactWindow(self, title, content, content_type)
        artifact_window.protocol("WM_DELETE_WINDOW", lambda: self.close_artifact_window(artifact_id, artifact_window))

    def close_artifact_window(self, artifact_id, window):
        window.destroy()
        if artifact_id in self.artifacts:
            del self.artifacts[artifact_id]

    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.conversation_history.clear()
        self.total_tokens = 0

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def on_closing(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.loop_thread.join()
        self.destroy()

if __name__ == "__main__":
    from config.api_keys import GROQ_API_KEY
    app = ChatGPTStyleInterface(GROQ_API_KEY)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()