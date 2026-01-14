import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("CustomTkinter")
        self.resizable(False, False)
        #self.iconbitmap("icon.ico")
        
        
        
app = App()
app.mainloop()