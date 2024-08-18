import tkinter as tk
from tkinter import filedialog,messagebox
from PIL import Image, ImageTk
import requests
import pygame
import pyttsx3
from base64 import b64decode

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAiChat")

        # 设置背景图片
        self.bg_image = ImageTk.PhotoImage(Image.open("bgpic.jpg"))
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 登录界面
        self.login_frame = tk.Frame(root)
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_entry = tk.Entry(self.login_frame, textvariable=self.username_var)
        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_entry = tk.Entry(self.login_frame, textvariable=self.password_var, show="*")

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.check_login)
        
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()

        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 创建 Text-to-speech 引擎对象
        self.engine = pyttsx3.init()
        
        # 设置文本朗读速度
        self.engine.setProperty('rate', 150)  # 可以根据实际需要调整速度
        
        # 设置音量
        self.engine.setProperty('volume', 0.7)  # 可以根据实际需要调整音量
        
        # 设置朗读声音
        voices = self.engine.getProperty('voices')  # 获取语音列表
        self.engine.setProperty('voice', voices[0].id)  # 选择其中一种语音

        icon_img = b'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'
        icon_img = b64decode(icon_img)
        icon_img = ImageTk.PhotoImage(data=icon_img)
        self.root.tk.call('wm', 'iconphoto', self.root._w, icon_img)


    def check_login(self):
        # 这里可以添加登录逻辑
        get_name = self.username_var.get()
        get_password = self.password_var.get()
        with open('users.txt','r',encoding='utf-8') as f:
            names_list = f.read().split('\n')
            password_dict = {}
            for i in range(len(names_list)):
                names_list[i] = names_list[i].split('#')
                password_dict[names_list[i][0]] = names_list[i][1]
                
        if get_name in password_dict.keys():
            if password_dict[get_name]==get_password:
                messagebox.showinfo('Login','Login successfully')
                self.show_chat_interface()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        elif get_name == '' or get_password == '':
            messagebox.showerror("Error", "Invalid username or password")
        else:
            choice = messagebox.askyesno('New User','Create a new username?')
            if choice:
                with open('users.txt','a',encoding='utf-8') as f:
                    f.write(f'\n{get_name}#{get_password}')
                messagebox.showinfo('Login','Login successfully')
                self.show_chat_interface()
            else:
                pass

    def show_chat_interface(self):
        # 显示聊天界面
        self.login_frame.pack_forget()
        
        # 设置窗口大小
        self.root.geometry("800x600")

        # 配置网格布局
        self.root.columnconfigure(0, weight=1)  # 所有列的权重设置为1
        self.root.rowconfigure(0, weight=1)    # 所有行的权重设置为1

        # 创建聊天界面控件
        self.chat_history = tk.Text(self.root, height=15, wrap="word",bd=2,relief='sunken')
        self.chat_history.grid(row=0, column=0, sticky="nsew")  

        self.is_volumn = False
        self.volumn_button = tk.Button(self.root,text='👂',command=self.change_volumn,bd=2,relief='sunken')
        self.volumn_button.grid(row=0,column=1,sticky='ns')

        self.chat_entry = tk.Entry(self.root, width=50,bd=2,relief='sunken')
        self.chat_entry.grid(row=1, column=0, sticky="ew")

        self.send_button = tk.Button(self.root, text="✈", command=self.add_to_chat_history,bd=2,relief='sunken')
        self.send_button.grid(row=1, column=1, sticky="ns")

    def add_to_chat_history(self):
        message = self.chat_entry.get()
        if message:
            sound_effect = pygame.mixer.Sound('sound.mp3')
            sound_effect.play()
            self.chat_history.insert(tk.END, f"\nUser: {message}\n")
            url='https://api.ownthink.com/bot?appid=9ffcb5785ad9617bf4e64178ac64f7b1&spoken=%s'%message
            te=requests.get(url).json()
            data=te['data']['info']['text']
            self.chat_history.insert(tk.END,f'AI:{data}\n')
            self.chat_entry.delete(0, tk.END)
            if self.is_volumn:
                self.engine.say(data)
                # 播放语音
                self.engine.runAndWait()

    def change_volumn(self):
        sound_effect = pygame.mixer.Sound('sound.mp3')
        sound_effect.play()
        self.is_volumn = not(self.is_volumn)

if __name__ == "__main__":
    pygame.mixer.init()
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()