import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import pygame  # 음악 재생용 라이브러리

# 1. 테마 설정
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- 오디오 초기화 ---
        pygame.mixer.init()
        
        # --- 변수 초기화 ---
        self.Playlist_folder = None
        self.play_list = []       # 전체 파일명 리스트
        self.song_buttons = {}    # {파일명: 버튼객체}
        self.current_song_index = -1
        self.is_playing = False
        self._search_job = None
        
        # --- UI 설정 ---
        self.geometry("1080x540")
        self.title("MeloniMP3player - Music On")
        self.resizable(False, False)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 2. 메뉴 바
        self.menu_bar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="gray10")
        self.menu_bar.grid(row=0, column=0, sticky="ew")

        self.btn_file = ctk.CTkButton(self.menu_bar, text="폴더 열기", width=80, height=30, 
                                     fg_color="transparent", hover_color="gray30",
                                     command=self.select_playlist_folder)
        self.btn_file.grid(row=0, column=0, padx=5, pady=5)

        # 3. 메인 컨테이너
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(1, weight=1)

        # --- 왼쪽: 재생 컨트롤 영역 ---
        self.play_frame = ctk.CTkFrame(self.main_container, width=320, height=450, fg_color="gray20")
        self.play_frame.grid(row=0, column=0, sticky="nsw")
        self.play_frame.grid_propagate(False)
        self.play_frame.columnconfigure(0, weight=1)
        
        # 곡 제목 표시 라벨
        self.now_playing_label = ctk.CTkLabel(self.play_frame, text="곡을 선택하세요", 
                                             font=("Pretendard", 16, "bold"), wraplength=250)
        self.now_playing_label.grid(row=0, column=0, pady=(20, 10))

        # 앨범 이미지 영역 (Placeholder)
        self.music_img_frame = ctk.CTkFrame(self.play_frame, width=220, height=220, fg_color="gray30")
        self.music_img_frame.grid(row=1, column=0, pady=10)
        
        # 컨트롤 버튼 영역
        self.ctrl_frame = ctk.CTkFrame(self.play_frame, fg_color="transparent")
        self.ctrl_frame.grid(row=2, column=0, pady=20)
        
        # 버튼들 (이전, 재생/일시정지, 다음)
        self.btn_prev = ctk.CTkButton(self.ctrl_frame, text="◀◀", width=50, command=self.play_prev)
        self.btn_prev.grid(row=0, column=0, padx=10)

        self.play_bt = ctk.CTkButton(self.ctrl_frame, text="▶", width=70, height=50, 
                                    font=("bold", 20), command=self.toggle_play)
        self.play_bt.grid(row=0, column=1, padx=10)

        self.btn_next = ctk.CTkButton(self.ctrl_frame, text="▶▶", width=50, command=self.play_next)
        self.btn_next.grid(row=0, column=2, padx=10)

        # 볼륨 슬라이더
        self.volume_slider = ctk.CTkSlider(self.play_frame, from_=0, to=1, width=200, command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.grid(row=3, column=0, pady=10)
        pygame.mixer.music.set_volume(0.5)

        # --- 오른쪽: 검색 및 곡 목록 영역 ---
        self.right_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_container.grid(row=0, column=1, padx=(20, 0), sticky="nsew")
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search_change)
        
        self.search_entry = ctk.CTkEntry(self.right_container, placeholder_text="노래 제목 검색...", 
                                         textvariable=self.search_var, height=35)
        self.search_entry.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.list_frame = ctk.CTkScrollableFrame(self.right_container, fg_color="gray15")
        self.list_frame.grid(row=1, column=0, sticky="nsew")

    # --- 음악 제어 로직 ---
    
    def select_playlist_folder(self):
        folder = filedialog.askdirectory(title="음악 폴더 선택")
        if folder:
            self.Playlist_folder = folder
            # 기존 목록 초기화
            for btn in self.song_buttons.values():
                btn.destroy()
            self.song_buttons.clear()
            
            try:
                all_files = os.listdir(self.Playlist_folder)
                self.play_list = sorted([f for f in all_files if f.lower().endswith(".mp3")])
                
                for song in self.play_list:
                    btn = ctk.CTkButton(self.list_frame, text=song, anchor="w", 
                                        fg_color="transparent", hover_color="gray30",
                                        command=lambda s=song: self.load_and_play(s))
                    self.song_buttons[song] = btn
                
                self.update_list_ui()
            except Exception as e:
                print(f"폴더 읽기 오류: {e}")

    def load_and_play(self, song_name):
        """특정 곡을 로드하고 재생"""
        if not self.Playlist_folder: return
        
        path = os.path.join(self.Playlist_folder, song_name)
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.current_song_index = self.play_list.index(song_name)
            self.now_playing_label.configure(text=song_name)
            self.play_bt.configure(text="⏸") # 일시정지 아이콘으로 변경
            
            # 리스트 하이라이트 효과 (선택된 곡 색상 변경)
            for s, btn in self.song_buttons.items():
                if s == song_name:
                    btn.configure(fg_color="gray30", text_color="#1f6aa5")
                else:
                    btn.configure(fg_color="transparent", text_color="white")
                    
        except Exception as e:
            print(f"재생 오류: {e}")

    def toggle_play(self):
        """재생/일시정지 토글"""
        if not self.play_list: return
        
        if not pygame.mixer.music.get_busy() and self.current_song_index == -1:
            # 처음 시작할 때 첫 번째 곡 재생
            self.load_and_play(self.play_list[0])
        elif self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_bt.configure(text="▶")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_bt.configure(text="⏸")

    def play_next(self):
        if not self.play_list: return
        self.current_song_index = (self.current_song_index + 1) % len(self.play_list)
        self.load_and_play(self.play_list[self.current_song_index])

    def play_prev(self):
        if not self.play_list: return
        self.current_song_index = (self.current_song_index - 1) % len(self.play_list)
        self.load_and_play(self.play_list[self.current_song_index])

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value))

    # --- UI 업데이트 로직 ---

    def on_search_change(self, *args):
        if self._search_job:
            self.after_cancel(self._search_job)
        self._search_job = self.after(100, self.update_list_ui)

    def update_list_ui(self):
        self._search_job = None
        query = self.search_var.get().lower()
        
        for song, btn in self.song_buttons.items():
            if query in song.lower():
                btn.pack(fill="x", pady=2, padx=5)
            else:
                btn.pack_forget()

if __name__ == "__main__":
    app = App()
    app.mainloop()