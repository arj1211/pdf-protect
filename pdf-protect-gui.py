import os
import time
from random import randint
from tkinter import (
    Button,
    Checkbutton,
    Entry,
    Frame,
    IntVar,
    Label,
    Text,
    Tk,
    filedialog,
)
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

from pypdf import PdfReader, PdfWriter


class PDFEncryptorApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Encryptor App")
        master.geometry("")  # Set initial size
        master.resizable(False, False)  # Make window non-resizable

        self.label = Label(master, text="PDF Encryptor")
        self.label.pack(pady=10)

        self.folder_frame = Frame(master)
        self.folder_frame.pack(padx=10, pady=10, fill="x")

        self.select_folder_button = Button(
            self.folder_frame, text="Select Folder", command=self.select_folder
        )
        self.select_folder_button.pack()

        self.preview_label = Label(self.folder_frame, text="PDF Files in the Folder:")
        self.preview_label.pack()

        # Use ScrolledText instead of Text
        self.preview_text = ScrolledText(
            self.folder_frame,
            height=10,
            width=50,
            state="disabled",
            padx=5,
            pady=5,
            wrap="none",
        )
        self.preview_text.pack()

        self.password_frame = Frame(master)
        self.password_frame.pack(padx=10, pady=10, fill="x")

        self.password_label = Label(self.password_frame, text="Enter Password:")
        self.password_label.pack()

        self.password_entry = Entry(self.password_frame, show="*")
        self.password_entry.pack()

        self.show_password_var = IntVar()
        self.show_password_checkbox = Checkbutton(
            self.password_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
        )
        self.show_password_checkbox.pack()

        self.generate_password_button = Button(
            self.password_frame,
            text="Generate Password",
            command=self.generate_password,
        )
        self.generate_password_button.pack()

        self.progress_frame = Frame(master)
        self.progress_frame.pack(padx=10, pady=10, fill="x")

        self.progress_label = Label(self.progress_frame, text="Progress:")
        self.progress_label.pack()

        self.progress_bar = Progressbar(
            self.progress_frame, length=300, mode="determinate"
        )
        self.progress_bar.pack()

        # Use ScrolledText instead of Text
        self.progress_text = ScrolledText(
            self.progress_frame,
            height=10,
            width=50,
            state="disabled",
            padx=5,
            pady=5,
            wrap="none",
        )
        self.progress_text.pack()

        self.encrypt_exit_frame = Frame(master)
        self.encrypt_exit_frame.pack(padx=10, pady=10, fill="x")

        self.encrypt_button = Button(
            self.encrypt_exit_frame, text="Encrypt PDFs", command=self.encrypt_pdfs
        )
        self.encrypt_button.pack(pady=5)

        self.exit_button = Button(
            self.encrypt_exit_frame, text="Exit", command=master.quit
        )
        self.exit_button.pack(pady=5)

        self.selected_folder = None
        self.password = None

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        if self.selected_folder:
            self.preview_label.config(
                text=f"PDF Files in the Folder: {self.selected_folder}"
            )
            self.update_preview()

    def update_preview(self):
        self.preview_text.configure(state="normal")
        self.preview_text.delete(1.0, "end")
        pdf_list = [f for f in os.listdir(self.selected_folder) if f.endswith(".pdf")]
        for pdf_file in pdf_list:
            last_char_visible = self.preview_text.bbox("end-1c")
            self.preview_text.insert("end", f"{pdf_file}\n")
            if last_char_visible:
                self.preview_text.see("end")

        if last_char_visible:
            self.preview_text.see("end")
        self.preview_text.configure(state="disabled")

    def generate_password(self):
        total_alphas = (
            [chr(ord("A") + i) for i in range(26)][:5]
            + [chr(ord("A") + i) for i in range(26)][-5:]
            + [str(i) for i in range(10)]
        )
        pw_len = 8
        generated_password = "".join(
            [total_alphas[randint(0, len(total_alphas) - 1)] for i in range(pw_len)]
        )
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, generated_password)
        return generated_password

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def add_encryption(self, input_pdf, output_pdf, password):
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(input_pdf, strict=False)

        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

        pdf_writer.encrypt(user_password=password, owner_pwd=None, use_128bit=True)

        with open(output_pdf, "wb") as fh:
            pdf_writer.write(fh)

    def encrypt_pdfs(self):
        if not self.selected_folder:
            self.label.config(text="Please select a folder.", fg="#ff9999")
            return

        new_folder_name = os.path.join(self.selected_folder, "protected")
        if not os.path.exists(new_folder_name):
            os.mkdir(new_folder_name)

        self.password = self.password_entry.get() or self.generate_password()

        t1 = time.time()

        pdf_list = [f for f in os.listdir(self.selected_folder) if f.endswith(".pdf")]

        self.progress_text.delete(1.0, "end")

        for i in range(len(pdf_list)):
            fname = pdf_list[i]
            input_path = os.path.join(self.selected_folder, fname)
            output_path = os.path.join(new_folder_name, fname)
            self.progress_text.configure(state="normal")
            last_char_visible = self.progress_text.bbox("end-1c")
            self.progress_text.insert("end", f"Encrypting {fname} ... ")
            if last_char_visible:
                self.progress_text.see("end")
            self.progress_text.configure(state="disabled")
            self.add_encryption(input_path, output_path, self.password)
            self.progress_text.configure(state="normal")
            self.progress_text.insert("end", f"Done\n")
            if last_char_visible:
                self.progress_text.see("end")
            self.progress_text.configure(state="disabled")

            progress_value = ((i + 1) / len(pdf_list)) * 100
            self.progress_bar["value"] = progress_value
            self.progress_frame.update()

        t2 = time.time()
        time_taken = "{:.2f}".format(t2 - t1)
        self.label.config(text=f"Time taken: {time_taken} seconds", fg="#00ccff")
        self.progress_text.configure(state="normal")
        h_text_divider = "~" * (len(new_folder_name) + 1) + "\n"
        last_char_visible = self.progress_text.bbox("end-1c")
        self.progress_text.insert("end", h_text_divider)
        self.progress_text.insert("end", "Encrypted PDFs are located in:\n")
        self.progress_text.insert("end", new_folder_name + "\n")
        self.progress_text.insert("end", h_text_divider)
        self.progress_text.insert("end", "Encryption process complete.")
        if last_char_visible:
            self.progress_text.see("end")
        self.progress_text.configure(state="disabled")


if __name__ == "__main__":
    root = Tk()
    app = PDFEncryptorApp(root)
    root.mainloop()
