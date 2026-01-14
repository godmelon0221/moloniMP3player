import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. 변수 초기화
        self.Playlist_folder = None
        self.play_list = []      # 전체 파일명 리스트
        self.song_buttons = {}   # {파일명: 버튼객체} 저장소 (위젯 재사용 핵심)
        self._search_job = None  # 검색 지연(디바운싱)을 위한 작업 변수
        
        self.geometry("1080x540")
        self.title("MeloniMP3player - Optimized")
        self.resizable(False, False)

        # 그리드 설정
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 2. 메뉴 바
        self.menu_bar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="gray10")
        self.menu_bar.grid(row=0, column=0, sticky="ew")

        self.btn_file = ctk.CTkButton(self.menu_bar, text="파일", width=60, height=30, 
                                      fg_color="transparent", hover_color="gray30",
                                      command=self.select_playlist_folder)
        self.btn_file.grid(row=0, column=0, padx=5, pady=5)

        # 3. 메인 컨테이너
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(1, weight=1)

        # --- 왼쪽: 재생 컨트롤 영역 ---
        self.play_frame = ctk.CTkFrame(self.main_container, width=300, height=450, fg_color="gray20")
        self.play_frame.grid(row=0, column=0, sticky="nsw")
        self.play_frame.grid_propagate(False)
        self.play_frame.columnconfigure(0, weight=1)
        
        self.music_img_frame = ctk.CTkFrame(self.play_frame, width=250, height=250, fg_color="gray30")
        self.music_img_frame.grid(row=0, column=0, pady=(25, 0))
        
        self.play_button_frame = ctk.CTkFrame(self.play_frame, width=250, height=100, fg_color="gray10")
        self.play_button_frame.grid(row=1, column=0, pady=(25,0))
        self.play_button_frame.columnconfigure((0, 1, 2), weight=1)
        
        # 버튼 아이콘 로드 (이미지 없을 시 대비)
        try:
            self.play_img = ctk.CTkImage(dark_image=Image.open("img/play.png"), size=(40, 40))
        except:
            self.play_img = None

        self.play_bt = ctk.CTkButton(self.play_button_frame, image=self.play_img, text="", 
                                     width=60, height=60, fg_color="transparent", 
                                     hover_color="gray20", command=self.Play_button_click)
        self.play_bt.grid(row=0, column=1)

        # --- 오른쪽: 검색 및 곡 목록 영역 ---
        self.right_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_container.grid(row=0, column=1, padx=(20, 0), sticky="nsew")
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)

        # 실시간 검색창
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search_change)
        
        self.search_entry = ctk.CTkEntry(self.right_container, placeholder_text="노래 제목 검색...", 
                                         textvariable=self.search_var, height=35)
        self.search_entry.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # 스크롤 가능한 곡 목록
        self.list_frame = ctk.CTkScrollableFrame(self.right_container, fg_color="gray15")
        self.list_frame.grid(row=1, column=0, sticky="nsew")

    # --- 최적화된 핵심 로직 ---

    def select_playlist_folder(self):
        """폴더 선택 및 버튼 사전 생성"""
        folder = filedialog.askdirectory(title="음악 폴더 선택")
        if folder:
            self.Playlist_folder = folder
            # 1. 기존 버튼들 완전 삭제
            for btn in self.song_buttons.values():
                btn.destroy()
            self.song_buttons.clear()
            
            # 2. 파일 리스트 업데이트
            all_files = os.listdir(self.Playlist_folder)
            self.play_list = [f for f in all_files if f.lower().endswith(".mp3")]
            
            # 3. 버튼들 미리 생성 (나중에 검색 시 생성하면 느림)
            for song in self.play_list:
                btn = ctk.CTkButton(self.list_frame, text=song, anchor="w", 
                                    fg_color="transparent", hover_color="gray30",
                                    command=lambda s=song: self.song_selected(s))
                self.song_buttons[song] = btn
            
            self.update_list_ui() # 최초 1회 표시

    def on_search_change(self, *args):
        """타이핑 시 검색 부하를 줄이는 디바운싱 로직"""
        if self._search_job:
            self.after_cancel(self._search_job)
        # 0.1초 동안 입력이 없으면 검색 실행 (연속 입력 시 대기)
        self._search_job = self.after(100, self.update_list_ui)

    def update_list_ui(self):
        """버튼을 파괴하지 않고 숨기기/보여주기만 수행 (매우 빠름)"""
        query = self.search_var.get().lower()
        
        # 모든 버튼을 일단 숨김
        for song, btn in self.song_buttons.items():
            if query in song.lower():
                btn.pack(fill="x", pady=2) # 검색어 포함 시 표시
            else:
                btn.pack_forget() # 포함 안 되면 숨김

    def song_selected(self, song_name):
        print(f"재생 대기: {song_name}")

    def Play_button_click(self):
        if not self.Playlist_folder:
            print("폴더를 먼저 선택하세요.")
        else:
            print("재생 중...")

    def menu_setting_click(self):
        print("설정")

if __name__ == "__main__":
    app = App()
    app.mainloop()