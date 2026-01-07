import tkinter as tk
from tkinter import font
import cv2
from PIL import Image, ImageTk
import numpy as np
import os

class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection Pro")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")  # Modern dark gray

        # --- Variables ---
        self.cap = None
        self.running = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.video_width = 700
        self.video_height = 450

        # --- UI Layout ---
        self.create_widgets()
        
        # Initialize black screen
        self.show_black_screen()

    def create_widgets(self):
        # 1. Header Section
        header_frame = tk.Frame(self.root, bg="#1e1e1e")
        header_frame.pack(pady=20)
        
        title_label = tk.Label(
            header_frame, 
            text="AI Face Detection System", 
            font=("Roboto", 24, "bold"), 
            bg="#1e1e1e", 
            fg="#00d2ff" # Cyan accent
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Real-time Computer Vision",
            font=("Roboto", 10),
            bg="#1e1e1e",
            fg="#888888"
        )
        subtitle_label.pack()

        # 2. Video Display Area (with a border/frame)
        self.video_frame = tk.Frame(self.root, bg="#000000", bd=2, relief="flat")
        self.video_frame.pack(pady=10)
        
        self.video_label = tk.Label(self.video_frame, bg="#000000")
        self.video_label.pack()

        # 3. Control Section
        control_frame = tk.Frame(self.root, bg="#1e1e1e")
        control_frame.pack(pady=20)

        # Custom Button Styling
        btn_font = ("Roboto", 12, "bold")
        
        self.start_btn = tk.Button(
            control_frame, text="INITIATE CAMERA", font=btn_font,
            bg="#00c853", fg="white", activebackground="#009624", activeforeground="white",
            relief="flat", width=18, height=2, cursor="hand2",
            command=self.start_camera
        )
        self.start_btn.grid(row=0, column=0, padx=15)

        self.stop_btn = tk.Button(
            control_frame, text="TERMINATE", font=btn_font,
            bg="#d50000", fg="white", activebackground="#9b0000", activeforeground="white",
            relief="flat", width=18, height=2, cursor="hand2",
            command=self.stop_camera, state="disabled"
        )
        self.stop_btn.grid(row=0, column=1, padx=15)

        # 4. Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("System Standby")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", bg="#2d2d2d", fg="#aaaaaa")
        status_bar.pack(side="bottom", fill="x")

    def show_black_screen(self):
        # Create a black image using numpy
        black_frame = np.zeros((self.video_height, self.video_width, 3), dtype=np.uint8)
        img = Image.fromarray(black_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open camera.")
                return
            
            self.running = True
            self.start_btn.config(state="disabled", bg="#444444")
            self.stop_btn.config(state="normal", bg="#d50000")
            self.status_var.set("Camera Active - Detecting Faces...")
            self.update_frame()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        
        self.start_btn.config(state="normal", bg="#00c853")
        self.stop_btn.config(state="disabled", bg="#444444")
        self.status_var.set("System Standby")
        self.show_black_screen()

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # 1. Face Detection Logic
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangles
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Optional: Add Label above face
            cv2.putText(frame, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # 2. Convert for Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((self.video_width, self.video_height))
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.root.after(10, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()