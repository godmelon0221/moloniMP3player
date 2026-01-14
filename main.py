import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        self.Playlist_folder = None
        
        super().__init__()
        self.geometry("1080x540")
        self.title("MeloniMP3player")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #메인 fr
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        #메뉴 바
        self.menu_bar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="gray10")
        self.menu_bar.grid(row=0, column=0, sticky="ew")

        self.btn_file = ctk.CTkButton(self.menu_bar, text="파일", width=60, height=30, 
                                      fg_color="transparent", hover_color="gray30",
                                      command=self.menu_file_click)
        self.btn_file.grid(row=0, column=0, padx=5, pady=5)

        self.btn_setting = ctk.CTkButton(self.menu_bar, text="설정", width=60, height=30, 
                                         fg_color="transparent", hover_color="gray30",
                                         command=self.menu_setting_click)
        self.btn_setting.grid(row=0, column=1, padx=5, pady=5)
        
        #재생 fr
        self.play_frame = ctk.CTkFrame(self.main_container, width=300, height=450, fg_color="gray20")
        self.play_frame.grid(row=0, column=0, sticky="nsw")
        self.play_frame.grid_propagate(False)
        self.play_frame.columnconfigure(0, weight=1) # 프레임 내 중앙 정렬을 위한 설정
        
        self.music_img_frame = ctk.CTkFrame(self.play_frame, width=250, height=250, fg_color="gray30")
        self.music_img_frame.grid(row=0, column=0, pady=(25, 0))
        self.music_img_frame.grid_propagate(False) # 내부 위젯에 의해 크기 변함 방지
        
        #buttons_fr
        self.play_button_frame = ctk.CTkFrame(self.play_frame, width=250, height=100, fg_color="gray10")
        self.play_button_frame.grid(row=1, column=0, pady=(25,0))
        self.play_button_frame.grid_propagate(False) # 내부 위젯에 의해 크기 변함 방지
        
        # 버튼 3개를 위해 0, 1, 2번 열을 균등하게 설정
        self.play_button_frame.columnconfigure((0, 1, 2), weight=1) 
        self.play_button_frame.rowconfigure(0, weight=1) 
        
        #buttons
        # 이전 곡 버튼
        left_icon = Image.open("img/lefr_next.png") # 변수명 오타 수정 (play_icon -> left_icon)
        self.left_next_img = ctk.CTkImage(dark_image=left_icon, size=(40, 40)) 
        
        self.left_next_bt = ctk.CTkButton(self.play_button_frame, image=self.left_next_img, text="", 
                                     width=60, height=60, fg_color="transparent", 
                                     hover_color="gray20")
        self.left_next_bt.grid(row=0, column=0) # 0번 열
        
        # 재생 버튼
        play_icon = Image.open("img/play.png")
        self.play_img = ctk.CTkImage(dark_image=play_icon, size=(40, 40)) 
        
        self.play_bt = ctk.CTkButton(self.play_button_frame, image=self.play_img, text="", 
                                     width=60, height=60, fg_color="transparent", 
                                     hover_color="gray20", command=self.Play_button)
        self.play_bt.grid(row=0, column=1) # 1번 열 (중앙)
        
        # 다음 곡 버튼
        right_icon = Image.open("img/right_next.png") # 변수명 구분
        self.right_next_img = ctk.CTkImage(dark_image=right_icon, size=(40, 40)) 
        
        self.right_next_bt = ctk.CTkButton(self.play_button_frame, image=self.right_next_img, text="", 
                                     width=60, height=60, fg_color="transparent", 
                                     hover_color="gray20",)
        self.right_next_bt.grid(row=0, column=2) # 2번 열
        

        #-------------------------------------------------------------
        #실행 로직
        #-------------------------------------------------------------
        
    #함수
    def Play_button(self):
        if self.file_check() is False:
            self.select_playlist_folder
        else:
            #TODO
            pass    
            
    def file_check(self):
        
        if self.Playlist_folder == None or self.Playlist_folder == "":
            self.select_playlist_folder()
        else:
            return True
        
    def select_playlist_folder(self):
            self.Playlist_folder = filedialog.askdirectory(title="음악 폴더를 선택하세요")  
            
            
            
    def menu_file_click(self):
        print("파일 메뉴가 클릭되었습니다.")

    def menu_setting_click(self):
        print("설정 메뉴가 클릭되었습니다.")
        

app = App()
app.mainloop()