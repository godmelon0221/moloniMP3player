import customtkinter as ctk
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x540")
        self.title("MeloniMP3player")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1) 

        play_frame = ctk.CTkFrame(self, width=300, height=500, fg_color="gray20")
        play_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsw")
        play_frame.grid_propagate(False)
        
        

app = App()
app.mainloop()