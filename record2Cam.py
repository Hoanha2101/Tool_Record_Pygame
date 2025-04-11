import numpy as np
import os
import pygame
import cv2

pygame.init()

folder_path = "collect_data"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Kích thước cửa sổ hiển thị
screen_width = 1200
screen_height = 700
camera_width = 640
camera_height = 480

def get_next_filename(cam_id):
    index = 1
    while os.path.exists(f"{folder_path}/cam{cam_id}_{index}.mp4"):
        index += 1
    return f"{folder_path}/cam{cam_id}_{index}.mp4"

# Khởi tạo 2 camera
camera1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
camera2 = cv2.VideoCapture(0, cv2.CAP_DSHOW)

for cam in [camera1, camera2]:
    cam.set(3, camera_width)
    cam.set(4, camera_height)

# Font chữ
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dual Camera Recorder")

recording = False
out1 = None
out2 = None
blink = False
frame_count = 0

def draw_button(text, pos, color, active=False):
    rect = pygame.Rect(pos[0], pos[1], 150, 50)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    if active:
        pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)
    text_surf = font.render(text, True, (255, 255, 255))
    screen.blit(text_surf, (pos[0] + 30, pos[1] + 10))
    return rect

running = True
while running:
    screen.fill((192, 192, 192))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if start_button.collidepoint(x, y) and not recording:
                filename1 = get_next_filename(1)
                filename2 = get_next_filename(2)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out1 = cv2.VideoWriter(filename1, fourcc, 25, (camera_width, camera_height))
                out2 = cv2.VideoWriter(filename2, fourcc, 25, (camera_width, camera_height))
                recording = True
            elif stop_button.collidepoint(x, y) and recording:
                recording = False
                out1.release()
                out2.release()
                out1 = None
                out2 = None
    
    # Đọc frame từ 2 camera
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()
    
    if ret1:
        
        if recording:
            out1.write(frame1)
        frame1 = cv2.flip(frame1, 1)
        frame1_disp = cv2.resize(frame1, (400, 300))
        frame1_disp = cv2.cvtColor(frame1_disp, cv2.COLOR_BGR2RGB)
        frame1_disp = pygame.surfarray.make_surface(cv2.rotate(frame1_disp, cv2.ROTATE_90_COUNTERCLOCKWISE))
        screen.blit(frame1_disp, (50, 50))

    if ret2:
        
        if recording:
            out2.write(frame2)
        frame2 = cv2.flip(frame2, 1)
        frame2_disp = cv2.resize(frame2, (400, 300))
        frame2_disp = cv2.cvtColor(frame2_disp, cv2.COLOR_BGR2RGB)
        frame2_disp = pygame.surfarray.make_surface(cv2.rotate(frame2_disp, cv2.ROTATE_90_COUNTERCLOCKWISE))
        screen.blit(frame2_disp, (500, 50))

    # Nút RECORD / STOP
    start_button = draw_button("RECORD", (950, 400), (0, 200, 0), recording)
    stop_button = draw_button("STOP", (950, 470), (200, 0, 0))

    # Hiệu ứng nhấp nháy khi đang quay
    if recording:
        frame_count += 1
        if frame_count % 30 < 15:
            blink = not blink
        status_color = (255, 0, 0) if blink else (200, 0, 0)
        pygame.draw.circle(screen, status_color, (screen_width - 50, 50), 15)
        status_text = font.render("Recording...", True, (255, 0, 0))
        screen.blit(status_text, (screen_width - 220, 40))

    pygame.display.flip()

# Giải phóng tài nguyên
if recording:
    out1.release()
    out2.release()
camera1.release()
camera2.release()
pygame.quit()
