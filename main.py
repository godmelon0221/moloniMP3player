import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("MeloniMP3player")
        self.resizable(False, False)
        self.iconbitmap("img/icon.ico")
        
        
        
app = App()
app.mainloop()