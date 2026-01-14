import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__() # 가장 먼저 실행
        
        # 변수 설정
        self.Playlist_folder = None
        self.play_list = []
        
        self.geometry("1080x540")
        self.title("MeloniMP3player")
        self.resizable(False, False)

        # 메인 그리드 설정
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        
        self.grid_columnconfigure(0, weight=1)
        
        # 메인 container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        # 오른쪽 영역(곡 목록)이 늘어나도록 설정
        self.main_container.grid_columnconfigure(1, weight=1)

        # 메뉴 바
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
        
        # --- 왼쪽: 재생 fr ---
        self.play_frame = ctk.CTkFrame(self.main_container, width=300, height=450, fg_color="gray20")
        self.play_frame.grid(row=0, column=0, sticky="nsw")
        self.play_frame.grid_propagate(False)
        self.play_frame.columnconfigure(0, weight=1)
        
        self.music_img_frame = ctk.CTkFrame(self.play_frame, width=250, height=250, fg_color="gray30")
        self.music_img_frame.grid(row=0, column=0, pady=(25, 0))
        self.music_img_frame.grid_propagate(False)
        
        self.play_button_frame = ctk.CTkFrame(self.play_frame, width=250, height=100, fg_color="gray10")
        self.play_button_frame.grid(row=1, column=0, pady=(25,0))
        self.play_button_frame.grid_propagate(False)
        self.play_button_frame.columnconfigure((0, 1, 2), weight=1) 
        self.play_button_frame.rowconfigure(0, weight=1) 
        
        # 재생 버튼 등 설정
        left_icon = Image.open("img/lefr_next.png")
        self.left_next_img = ctk.CTkImage(dark_image=left_icon, size=(40, 40))
        self.left_next_bt = ctk.CTkButton(self.play_button_frame, image=self.left_next_img, text="", 
                                          width=60, height=60, fg_color="transparent", hover_color="gray20")
        self.left_next_bt.grid(row=0, column=0)
        
        play_icon = Image.open("img/play.png")
        self.play_img = ctk.CTkImage(dark_image=play_icon, size=(40, 40))
        self.play_bt = ctk.CTkButton(self.play_button_frame, image=self.play_img, text="", 
                                     width=60, height=60, fg_color="transparent", 
                                     hover_color="gray20", command=self.Play_button_click)
        self.play_bt.grid(row=0, column=1)
        
        right_icon = Image.open("img/right_next.png")
        self.right_next_img = ctk.CTkImage(dark_image=right_icon, size=(40, 40))
        self.right_next_bt = ctk.CTkButton(self.play_button_frame, image=self.right_next_img, text="", 
                                           width=60, height=60, fg_color="transparent", hover_color="gray20")
        self.right_next_bt.grid(row=0, column=2)

        # --- 오른쪽: 곡 목록 fr ---
        # column=1 로 변경하여 재생기 오른쪽에 배치
        self.list_frame = ctk.CTkScrollableFrame(self.main_container, width=650, height=450, fg_color="gray20")
        self.list_frame.grid(row=0, column=1, padx=(20, 0), sticky="nsew")

    # --- 함수 ---
    def Play_button_click(self):
        if not self.file_check():
            self.select_playlist_folder()
        else:
            print("재생 중...")

    def file_check(self):
        if not self.Playlist_folder:
            return False
        return True
        
    def select_playlist_folder(self):
        folder = filedialog.askdirectory(title="음악 폴더를 선택하세요")
        if folder:
            self.Playlist_folder = folder
            all_file = os.listdir(self.Playlist_folder)
            self.play_list = [file for file in all_file if file.lower().endswith(".mp3")]
            print(f"목록 업데이트: {len(self.play_list)}곡 발견")
            self.update_list_ui() # UI에 목록 표시 (함수 추가 필요)

    def update_list_ui(self):
        """가져온 노래 목록을 화면에 표시 (예시)"""
        # 기존 목록 삭제
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        # 새 목록 추가
        for song in self.play_list:
            btn = ctk.CTkButton(self.list_frame, text=song, anchor="w", fg_color="transparent")
            btn.pack(fill="x", pady=2)

    def menu_file_click(self):
        self.select_playlist_folder()

    def menu_setting_click(self):
        print("설정 클릭")

app = App()
app.mainloop()