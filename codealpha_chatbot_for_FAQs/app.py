import tkinter as tk
from tkinter import scrolledtext
from chatbot import FAQChatbot

# Initialize chatbot
bot = FAQChatbot("faqs.json")

# -----------------------------
# GUI FUNCTIONS
# -----------------------------
def add_message(sender, message):
    chat.config(state="normal")        # temporarily enable
    chat.insert(tk.END, f"{sender}: {message}\n\n")
    chat.config(state="disabled")      # make read-only again
    chat.yview(tk.END)

def send_message(event=None):
    user_msg = entry.get().strip()
    if not user_msg:
        return

    add_message("You", user_msg)

    response = bot.get_response(user_msg)
    add_message("Bot", response)

    entry.delete(0, tk.END)

# -----------------------------
# TKINTER UI SETUP
# -----------------------------
root = tk.Tk()
root.title("FAQ Chatbot")

# Chat display (read-only)
chat = scrolledtext.ScrolledText(
    root,
    width=60,
    height=20,
    state="disabled",
    wrap=tk.WORD
)
chat.pack(padx=10, pady=10)

# Input area frame
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

# Label on the left
label = tk.Label(input_frame, text="Type your message here:")
label.pack(side=tk.LEFT, padx=5)

# Entry box
entry = tk.Entry(input_frame, width=40)
entry.pack(side=tk.LEFT, padx=5)
entry.bind("<Return>", send_message)   # Enter key sends message

# Send button
send_btn = tk.Button(input_frame, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT, padx=5)

# Welcome message
add_message("Bot", "Hello! Ask me anything about the FAQs.")

root.mainloop()