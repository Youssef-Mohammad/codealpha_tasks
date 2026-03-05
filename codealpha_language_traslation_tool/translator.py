import tkinter as tk
from tkinter import ttk, messagebox
import requests

def translate_text(text, target_lang, source_lang=None):
    """Call the Free Translate API."""
    url = "https://ftapi.pythonanywhere.com/translate"
    params = {
        "dl": target_lang,
        "text": text
    }
    if source_lang and source_lang != "auto":
        params["sl"] = source_lang
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def on_translate():
    text = input_text.get("1.0", tk.END).strip()
    source_lang = source_lang_var.get()
    target_lang = target_lang_var.get()
    
    if not text:
        messagebox.showwarning("Input Required", "Please enter text to translate.")
        return
    
    try:
        result = translate_text(text, target_lang, source_lang if source_lang != "auto" else None)
        translated = result.get("destination-text", "No translation found")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def copy_text(text_widget):
    text = text_widget.get("1.0", tk.END).strip()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        messagebox.showinfo("Copied", "Text copied to clipboard!")

# Tkinter UI setup
root = tk.Tk()
root.title("Simple Translator")

# Input text
tk.Label(root, text="Enter text:").pack(anchor="w")

input_frame = tk.Frame(root)
input_frame.pack()

input_text = tk.Text(input_frame, height=5, width=50)
input_text.pack()

copy_input_btn = ttk.Button(
    input_frame,
    text="Copy",
    command=lambda: copy_text(input_text)
)
copy_input_btn.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

# Language selection
frame = tk.Frame(root)
frame.pack(pady=5)

# Common language codes
languages = [
    ("Auto Detect", "auto"),
    ("English", "en"),
    ("Arabic", "ar"),
    ("French", "fr"),
    ("Spanish", "es"),
    ("German", "de"),
    ("Turkish", "tr"),
    ("Italian", "it"),
    ("Russian", "ru"),
    ("Chinese (Simplified)", "zh")
]

tk.Label(frame, text="Source Language:").grid(row=0, column=0, padx=5)
source_lang_var = tk.StringVar(value="auto")
source_dropdown = ttk.Combobox(frame, textvariable=source_lang_var, values=[name for name, code in languages], state="readonly")
source_dropdown.grid(row=0, column=1)

tk.Label(frame, text="Target Language:").grid(row=0, column=2, padx=5)
target_lang_var = tk.StringVar(value="Turkish")
target_dropdown = ttk.Combobox(frame, textvariable=target_lang_var, values=[name for name, code in languages], state="readonly")
target_dropdown.grid(row=0, column=3)

# Map display names back to codes
name_to_code = {name: code for name, code in languages}

# Translate button
translate_btn = ttk.Button(root, text="Translate", command=on_translate)
translate_btn.pack(pady=5)

# Output text
tk.Label(root, text="Translation:").pack(anchor="w")

output_frame = tk.Frame(root)
output_frame.pack()

output_text = tk.Text(output_frame, height=5, width=50)
output_text.pack()

copy_output_btn = ttk.Button(
    output_frame,
    text="Copy",
    command=lambda: copy_text(output_text)
)
copy_output_btn.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

root.mainloop()
