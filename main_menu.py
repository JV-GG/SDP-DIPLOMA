import pygame
import pymysql
import time
import sys
import random
import smtplib
import os

pygame.init()

if not pygame.mixer.music.get_busy():
    pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  

screen_width = 1920 
screen_height = 1080 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Counting-Strike')  

white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)
green = (0, 0, 139) 
red = (255, 0, 0)

click_sound = pygame.mixer.Sound(os.path.join("sound", "click.wav"))

font_small = pygame.font.Font('font/Minecraft.ttf', 18)
custom_font1 = pygame.font.Font('font/Minecraft.ttf', 40)
custom_font1_small = pygame.font.Font('font/Minecraft.ttf', 37)
custom_font_smallest = pygame.font.Font('font/Minecraft.ttf', 15)
custom_font1_big = pygame.font.Font('font/Minecraft.ttf', 50)
custom_font1_small1 = pygame.font.Font('font/Minecraft.ttf', 32)
about_us_font = pygame.font.Font('font/Minecraft.ttf', 30)
about_us_heading_font = pygame.font.Font('font/Minecraft.ttf', 60)
stage_font = pygame.font.Font('font/Minecraft.ttf', 27)
input_font = pygame.font.Font('font/Minecraft.ttf', 20)

login_button_image = pygame.image.load(r'jpg/main_menu_button.png')
register_button_image = pygame.image.load(r'jpg/main_menu_button.png')
back_button_path = 'jpg/back_button.png'
quit_button_path = 'jpg/quit_button.png'

input_image_path = 'jpg/input.png'

button_image_orig = pygame.image.load(input_image_path).convert_alpha()
button_image_size = (700, 100)  
button_image = pygame.transform.scale(button_image_orig, button_image_size)

login_button_image = pygame.transform.scale(login_button_image, (200, 200))
register_button_image = pygame.transform.scale(register_button_image, (200, 200))

menu_image = pygame.image.load(r'jpg\mainbackground.png').convert_alpha()
menu_image = pygame.transform.scale(menu_image, (screen_width, screen_height))
menu_width = menu_image.get_width()

quit_button_image_orig = pygame.image.load(quit_button_path).convert_alpha()
quit_button_size = (200, 50)
quit_button_image = pygame.transform.scale(quit_button_image_orig, quit_button_size)

back_button_image_orig = pygame.image.load(back_button_path).convert_alpha()
button_size = (100, 100)  
back_button_image = pygame.transform.scale(back_button_image_orig, button_size)
back_button_rect = back_button_image.get_rect()
back_button_rect.topleft = (40, 40) 

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sdp'
)
my_cursor = conn.cursor()

eye_closed_image_path="jpg/password_off.png"
eye_image_path="jpg/password_on.png"

input_image = pygame.image.load(input_image_path).convert_alpha()
input_image = pygame.transform.scale(input_image, (350, 100))
input_image2 = pygame.transform.scale(input_image, (400, 50))
input_image3 = pygame.transform.scale(input_image, (450, 100))

OTP = random.randint(100000,999999)

server = smtplib.SMTP('smtp.gmail.com',587)      
server.starttls()


def message_display(text, font_size, x, y, color):
    font = pygame.font.Font(None, font_size)
    text_surf, text_rect = text_objects(text, font, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.flip()

def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def email_verification(receiver_email):
    message = ""
    email_check1 = ["gmail", "hotmail", "yahoo", "outlook"]
    email_check2 = [".com", ".in", ".org", ".edu", ".co.in"]
    count = 0

    for domain in email_check1:
        if domain in receiver_email:
            count += 1
    for site in email_check2:
        if site in receiver_email:
            count += 1

    if "@" not in receiver_email or count != 2:
        print("invalid email id")
        message = "invalid email id"
        if message:
            message_display(message, 24, screen_width // 2, 700, green)
            pygame.display.flip()
            time.sleep(1)

    return receiver_email

def otp_code(name_otp, receiver_email):

    message2 = ""
    scroll = 0
    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500
    valid_receiver_email = email_verification(receiver_email)
    password = "pckqciqvdvnrebrk"
    server.login("boonmonopoly4@gmail.com", password)

    body = "Dear " + name_otp + ",\n\nYour OTP is " + str(OTP) + "."
    subject = "OTP Verification by Counting-Strike"
    message = f'Subject: {subject}\n\n{body}'

    server.sendmail("boonmonopoly4@gmail.com", valid_receiver_email, message)

    print("OTP has been sent to " + valid_receiver_email)
    message2 = f"OTP has been sent to {receiver_email}"

    if message2:
        message_display(message2, 24, screen_width // 2, 900, green)
        pygame.display.flip()
        time.sleep(1)

    inputs = {
        "Enter OTP code:": (0, 400, 350, 100, 24),
    }

    user_text = ''
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill(white)
        
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time

        scroll += 1.7
        if scroll > screen_width: 
            scroll = 0
        draw_menu(scroll)

        screen.blit(input_image, (screen_width // 2 - input_image.get_width() // 2, screen_height // 2 - input_image.get_height() // 2))

        enter_otp_text = custom_font1.render("Enter OTP code:", True, black)
        screen.blit(enter_otp_text, ((screen_width - enter_otp_text.get_width()) // 2, (screen_height - input_image.get_height()) // 2 - 50))

        text_surface = custom_font1_small.render(user_text, True, black)
        text_rect = text_surface.get_rect(center=input_image.get_rect(center=(screen_width // 2, screen_height // 2)).center)
        screen.blit(text_surface, text_rect.topleft)

        if blink and input_active:
            cursor_x = text_rect.right + 2  
            cursor_top = text_rect.top + (text_rect.height - custom_font1_small.get_linesize()) // 2
            cursor_bottom = cursor_top + custom_font1_small.get_linesize()
            pygame.draw.line(screen, black, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

        pygame.display.flip()

    try:
        received_OTP = int(user_text)
    except ValueError:
        received_OTP = None

    if received_OTP == OTP:
        print("OTP verified")
        message2 = "OTP Verified"
        if message2:
            message_display(message2, 24, screen_width // 2, 700, green)
            pygame.display.flip()
            time.sleep(1)
    else:
        print("invalid OTP")
        message2 = "Invalid OTP"
        if message2:
            message_display(message2, 24, screen_width // 2, 700, red)
            pygame.display.flip()
            time.sleep(1)
            logo_menu()
    

def send_password_email(name_otp, password_otp, receiver_email):
    valid_receiver_email = email_verification(receiver_email)
    sender_email = "boonmonopoly4@gmail.com"
    sender_password = "pckqciqvdvnrebrk"
    
    body = f"Dear {name_otp},\n\nYour password is: {password_otp}."
    subject = "Password Recovery by Counting-Strike"
    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, valid_receiver_email, message)
    
def check_login(email, password):
    query = "SELECT * FROM player WHERE email=%s AND password=%s"
    my_cursor.execute(query, (email, password))
    result = my_cursor.fetchone()
    return result is not None

def check_login_admin(email, password):
    query = "SELECT * FROM ADMIN WHERE email=%s AND password=%s"
    my_cursor.execute(query, (email, password))
    result = my_cursor.fetchone()
    return result is not None

def register_user(username, age, email, password):
    try:
        query = "INSERT INTO player (nickname, age, email, password) VALUES (%s, %s, %s, %s)"
        my_cursor.execute(query, (username, age, email, password))
        conn.commit()
        return True
    except pymysql.Error as e:
        message_display(f"Error: {e}", 24, screen_width // 2, 500, black)
        return False
    
def register_admin(username, age, email, password):
    try:
        query = "INSERT INTO ADMIN (nickname, age, email, password) VALUES (%s, %s, %s, %s)"
        my_cursor.execute(query, (username, age, email, password))
        conn.commit()
        return True
    except pymysql.Error as e:
        message_display(f"Error: {e}", 24, screen_width // 2, 500, black)
        return False

def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_display(text, font_size, x, y, color):
    font = pygame.font.Font(None, font_size)
    text_surf, text_rect = text_objects(text, font, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.flip()

def multi_text_input2(inputs):
    
    input_boxes = {prompt: pygame.Rect((screen_width - button_image_size[0]) // 2, (y + 100 - button_image_size[1]) // 2, button_image_size[0], button_image_size[1]) for prompt, (x, y, width, height, font_size) in inputs.items()}
    
    colors = {prompt: pygame.Color('lightskyblue3') for prompt in inputs}
    active_box = None
    texts = {prompt: '' for prompt in inputs}
    done = False
    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500  
    scroll = 0
        
    while not done:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                for prompt, box in input_boxes.items():
                    if box.collidepoint(event.pos):
                        active_box = prompt
                        colors[prompt] = pygame.Color('dodgerblue2')
                    else:
                        colors[prompt] = pygame.Color('lightskyblue3')
                        
                    if back_button_rect.collidepoint(event.pos):
                        main_menu() 
                        
            if event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        texts[active_box] = texts[active_box][:-1]
                    else:
                        texts[active_box] += event.unicode
        
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time
        
        scroll += 1.7
        if scroll > screen_width:  
            scroll = 0
        draw_menu(scroll)

        for prompt, box in input_boxes.items():
            button_x = box.x + (box.width - button_image_size[0]) // 2
            button_y = box.y + (box.height - button_image_size[1]) // 2

            screen.blit(button_image, (button_x, button_y))
            
            font = pygame.font.Font(None, inputs[prompt][4])
            display_text = texts[prompt]
            
            text_surf = custom_font1.render(prompt + ": " + display_text, True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            text_rect.center = (box.x + box.width // 2, box.y + box.height // 2)
            screen.blit(text_surf, text_rect)

            if active_box == prompt and blink:
                cursor_x = text_rect.right + 2  
                cursor_top = text_rect.top + (text_rect.height - font.get_linesize()) // 2
                cursor_bottom = cursor_top + font.get_linesize()
                pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

            mouse_pos = pygame.mouse.get_pos()
            for box in input_boxes.values():
                if box.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
            else:
                if back_button_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        

        screen.blit(back_button_image, back_button_rect)
        pygame.display.flip()

    return texts

def multi_text_input(inputs, input_image_path, eye_image_path, eye_closed_image_path):
    
    input_boxes = {prompt: pygame.Rect((screen_width - button_image_size[0]) // 2, (y + 100 - button_image_size[1]) // 2, button_image_size[0], button_image_size[1]) for prompt, (x, y, width, height, font_size) in inputs.items()}
    
    colors = {prompt: pygame.Color('lightskyblue3') for prompt in inputs}
    active_box = None
    texts = {prompt: '' for prompt in inputs}
    done = False
    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500  
    scroll = 0
    
    eye_image = None
    eye_closed_image = None
    eye_size = (40, 40)

    if eye_image_path:
        eye_image_orig = pygame.image.load(eye_image_path).convert_alpha()
        eye_image = pygame.transform.scale(eye_image_orig, eye_size)

    if eye_closed_image_path:
        eye_closed_image_orig = pygame.image.load(eye_closed_image_path).convert_alpha()
        eye_closed_image = pygame.transform.scale(eye_closed_image_orig, eye_size)

    show_password = False if eye_closed_image else True  
    eye_button_rect = None
    if eye_image and eye_closed_image:
        eye_button_rect = eye_image.get_rect()
        eye_button_rect.center = ( screen_width// 2, input_boxes["Password"].bottom + 30)  
        
    while not done:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                for prompt, box in input_boxes.items():
                    if box.collidepoint(event.pos):
                        active_box = prompt
                        colors[prompt] = pygame.Color('dodgerblue2')
                    else:
                        colors[prompt] = pygame.Color('lightskyblue3')
                        
                    if back_button_rect.collidepoint(event.pos):
                        main_menu() 
                    
                    if eye_button_rect and eye_button_rect.collidepoint(event.pos) and prompt == "Password":
                        show_password = not show_password
                    elif logout_button_rect.collidepoint(mouse_pos) or (screen_width - 220 < mouse_pos[0] < screen_width - 220 + quit_button_size[0] and screen_height - 60 < mouse_pos[1] < screen_height - 60 + quit_button_size[1]):
                        forget_password()
                        
            if event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        texts[active_box] = texts[active_box][:-1]
                    else:
                        texts[active_box] += event.unicode

                    if prompt == "Password" and not show_password:
                        display_text = '*' * len(texts[prompt]) 
        
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time
        
        scroll += 1.7
        if scroll > screen_width:  
            scroll = 0
        draw_menu(scroll)

        for prompt, box in input_boxes.items():
            button_x = box.x + (box.width - button_image_size[0]) // 2
            button_y = box.y + (box.height - button_image_size[1]) // 2

            screen.blit(button_image, (button_x, button_y))
            
            font = pygame.font.Font(None, inputs[prompt][4])
            display_text = texts[prompt]
            if prompt == "Password" and not show_password:
                display_text = '*' * len(texts[prompt]) 
            text_surf = custom_font1.render(prompt + ": " + display_text, True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            text_rect.center = (box.x + box.width // 2, box.y + box.height // 2)
            screen.blit(text_surf, text_rect)

            if active_box == prompt and blink:
                cursor_x = text_rect.right + 2 
                cursor_top = text_rect.top + (text_rect.height - font.get_linesize()) // 2
                cursor_bottom = cursor_top + font.get_linesize()
                pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

            font_small = pygame.font.Font('font/Minecraft.ttf', 18) 
            screen.blit(quit_button_image, (screen_width - 220, screen_height - 60))   
            logout_button_rect = pygame.Rect(screen_width - 200, screen_height - 50, 150, 30)
            draw_text("Forget Password", font_small, black, logout_button_rect.centerx, logout_button_rect.centery)

            mouse_pos = pygame.mouse.get_pos()
            for box in input_boxes.values():
                if box.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
            else:
                if eye_button_rect.collidepoint(mouse_pos) or back_button_rect.collidepoint(mouse_pos) or logout_button_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if eye_image and eye_closed_image:
            screen.blit(eye_closed_image if not show_password else eye_image, eye_button_rect)

        screen.blit(back_button_image, back_button_rect)
        pygame.display.flip()

    return texts

def render_text(font_path, text, font_size, x, y, color):
    font = pygame.font.Font(font_path, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_text(text, font, color, x, y, align="center"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "left":
        text_rect.topleft = (x, y)
    else:
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def validate_user_input(username, age, email, password):
    if not username or len(username) > 50:
        return False, "Username is required and must be less than or equal to 50 characters."
    
    try:
        age = int(age)
        if age <= 0 or age > 99:
            return False, "Age must be a positive integer between 1 and 99."
    except ValueError:
        return False, "Invalid age."
    
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or len(email) > 100:
        return False, "Invalid email format."
    
    if not password or len(password) > 50:
        return False, "Password is required and must be less than or equal to 50 characters."
    
    return True, "Input validated successfully."

def validate_admin_input(username, age, email, password, admin_code):
    if not username or len(username) > 50:
        return False, "Username is required and must be less than or equal to 50 characters."
    
    try:
        age = int(age)
        if age <= 0 or age > 99:
            return False, "Age must be a positive integer between 1 and 99."
    except ValueError:
        return False, "Invalid age."
    
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or len(email) > 100:
        return False, "Invalid email format."
    
    if not password or len(password) > 50:
        return False, "Password is required and must be less than or equal to 50 characters."
    
    if admin_code != "sdp2024":
        return False, "Wrong admin code."
    
    return True, "Input validated successfully."

def draw_menu(scroll):
    for x in range(5):
        screen.blit(menu_image, ((x * menu_width) - scroll, 0))

def get_stage_scores(id):

    conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sdp'
    )
    my_cursor = conn.cursor()

    my_cursor.execute("SHOW COLUMNS FROM `score`")
    columns = [column[0] for column in my_cursor.fetchall() if column[0] != 'id']
    
    columns_to_select = ', '.join(columns)
    query = f"SELECT {columns_to_select} FROM `score` WHERE id = %s"
    
    my_cursor.execute(query, (id,))
    result = my_cursor.fetchone()

    if result:
        scores = []
        for score in result:
            if score is not None:
                scores.append(score)
            else:
                scores.append(None)
        print("Fetched scores from database:", scores) 
        return scores
    else:
        return []

def stage_select_menu(profile,id):
    scroll = 0
    message = ""

    stage_image_orig = pygame.image.load('jpg/main_menu_button.png').convert_alpha()
    stage_image_size = (150, 150)
    stage_image = pygame.transform.scale(stage_image_orig, stage_image_size)

    stage_image_orig2 = pygame.image.load('jpg/stage_button2.png').convert_alpha()
    stage_image_size2 = (150, 150)
    stage_image2 = pygame.transform.scale(stage_image_orig2, stage_image_size2)

    block_width = 150
    block_height = 150

    check_and_update_stage(id)
    scores = get_stage_scores(id)
            
    query = "SHOW COLUMNS FROM `score` WHERE Field != 'id'"
    my_cursor.execute(query)
    columns = my_cursor.fetchall()
    stage_names = [col[0] for col in columns] + ['Soon']

    num_stages = len(stage_names)
    rows = (num_stages // 3) + (1 if num_stages % 3 != 0 else 0)  
    cols = 3

    padding_x = (screen.get_width() - (cols * block_width)) // (cols + 1)
    padding_y = (screen.get_height() - (rows * block_height)) // (rows + 5)

    blocks = []
    for row in range(rows):
        for col in range(cols):
            x = padding_x + col * (block_width + padding_x)
            y = padding_y + row * (block_height + padding_y) + 120
            if len(blocks) < num_stages:  
                blocks.append(pygame.Rect(x, y, block_width, block_height))

    stage_images = []
    for i in range(num_stages):
        text = stage_names[i]
        img = stage_image.copy()

        if scores is not None and i < len(scores) and scores[i] is not None:
            score_text = f"Score: {scores[i]}"
            score_surface = custom_font_smallest.render(score_text, True, black)
            score_rect = score_surface.get_rect(center=(block_width // 2, block_height // 2 + 40))
            img.blit(score_surface, score_rect)
        else:
            img.blit(stage_image2, (0, 0))

        text_surface = stage_font.render(text, True, black)
        text_rect = text_surface.get_rect(center=(block_width // 2, block_height // 2))
        img.blit(text_surface, text_rect)

        stage_images.append(img)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound.play()
                mouse_pos = event.pos
                for i, block in enumerate(blocks):
                    if block.collidepoint(mouse_pos):
                        if i < len(stage_names):
                            if stage_names[i] != 'Soon' and scores is not None and scores[i] is not None:
                                print(stage_names[i])
                                message = stage_names[i]
                                message_color = green
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                                from stage1 import start_game
                                start_game(stage_names[i], id)
                                return
                            elif stage_names[i] == 'Soon':
                                print('Coming Soon')
                                message = "Coming Soon"
                                message_color = red
                            else:
                                print("Haven't Unlocked")
                                message = "Haven't Unlocked"
                                message_color = red   
                            
                    if back_button_rect.collidepoint(event.pos):
                        start_menu(profile,id)

        screen.fill(white)

        scroll += 1.1  
        if scroll > menu_width:
            scroll = 0 
        draw_menu(scroll)

        screen.blit(back_button_image, back_button_rect)

        for i, block in enumerate(blocks):
            screen.blit(stage_images[i], block)

        if message:
            message_display(message, 24, screen_width // 2, 850, message_color)
            
        mouse_pos = pygame.mouse.get_pos()
        cursor_set = False
        for block in blocks:
            if block.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                cursor_set = True
                break
        if back_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_set = True
        if not cursor_set:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()

def check_and_update_stage(id):
    
    conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sdp'
)
    my_cursor = conn.cursor()

    query = "SELECT * FROM `score` WHERE `id` = %s"
    my_cursor.execute(query, (id,))
    result = my_cursor.fetchone()

    if result:
        columns = my_cursor.description
        
        for i in range(1, len(result)):
            if result[i] == 0:
                return
        
        for i in range(1, len(result)):
            if result[i] is None:
                column_name = columns[i][0]
                update_query = f"UPDATE `score` SET `{column_name}` = 0 WHERE `id` = %s"
                my_cursor.execute(update_query, (id,))
                conn.commit()
                return

def stage_select_menu_admin(profile, id):
    scroll = 0
    message = ""

    stage_image_orig = pygame.image.load('jpg/main_menu_button.png').convert_alpha()
    stage_image_size = (150, 150)
    stage_image = pygame.transform.scale(stage_image_orig, stage_image_size)

    stage_image_orig2 = pygame.image.load('jpg/stage_button2.png').convert_alpha()
    stage_image_size2 = (150, 150)
    stage_image2 = pygame.transform.scale(stage_image_orig2, stage_image_size2)

    block_width = 150
    block_height = 150

    query = "SHOW COLUMNS FROM `score` WHERE Field != 'id'"
    my_cursor.execute(query)
    columns = my_cursor.fetchall()
    stage_names = [col[0] for col in columns] + ['Edit']  

    num_stages = len(stage_names)
    rows = (num_stages // 3) + (1 if num_stages % 3 != 0 else 0) 
    cols = 3

    padding_x = (screen.get_width() - (cols * block_width)) // (cols + 1)
    padding_y = (screen.get_height() - (rows * block_height)) // (rows + 5)

    blocks = []
    for row in range(rows):
        for col in range(cols):
            x = padding_x + col * (block_width + padding_x)
            y = padding_y + row * (block_height + padding_y) + 120
            if len(blocks) < num_stages:  
                blocks.append(pygame.Rect(x, y, block_width, block_height))

    stage_images = []
    for i in range(num_stages):
        text = stage_names[i]
        img = stage_image.copy()

        img.blit(stage_image, (0, 0))

        text_surface = stage_font.render(text, True, black)
        text_rect = text_surface.get_rect(center=(block_width // 2, block_height // 2))
        img.blit(text_surface, text_rect)

        stage_images.append(img)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound.play()
                mouse_pos = event.pos
                for i, block in enumerate(blocks):
                    if block.collidepoint(mouse_pos):
                        if i < len(stage_names):
                            if stage_names[i] == 'Edit':
                                print('Edit Stage button clicked.')
                                message = "Edit stage"
                                message_color = red
                                if message:
                                    message_display(message, 24, screen_width // 2, 900, message_color)
                                    time.sleep(0.5)
                                admin_stage_menu(profile, id)
                            else:
                                print(stage_names[i])
                                message = stage_names[i]
                                message_color = green
                                selected_stage = stage_names[i]
                                if message:
                                    message_display(message, 24, screen_width // 2, 900, message_color)
                                    time.sleep(0.5)
                                add_questions_to_stage(profile, id, selected_stage)

                if back_button_rect.collidepoint(event.pos):
                    print('Back button clicked.')
                    start_menu_admin(profile, id)

        screen.fill(white)

        scroll += 1.1 
        if scroll > menu_width:
            scroll = 0
        draw_menu(scroll)

        screen.blit(back_button_image, back_button_rect)

        for i in range(len(stage_images)):
            if i < len(blocks):
                screen.blit(stage_images[i], blocks[i])

        

        mouse_pos = pygame.mouse.get_pos()
        cursor_set = False
        for block in blocks:
            if block.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                cursor_set = True
                break
        if back_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_set = True
        if not cursor_set:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        

def admin_stage_menu(profile, id):
    scroll = 0
    font_small = pygame.font.Font('font/Minecraft.ttf', 25)

    input_box_image = pygame.image.load(input_image_path).convert_alpha()
    input_box_image = pygame.transform.scale(input_box_image, (300, 60))

    my_cursor.execute("SHOW COLUMNS FROM score")
    columns = my_cursor.fetchall()
    stages = [col[0] for col in columns if col[0] != 'id']

    stage_buttons = {name: pygame.Rect(100, 250 + i * 40, 200, 30) for i, name in enumerate(stages)}
    new_stage_input_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 20, 300, 60)
    add_stage_button_rect = pygame.Rect(screen_width // 2 - 125, screen_height // 2 + 40 + 30, 250, 50)
    remove_stage_button_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 100 + 100, 300, 50)

    screen.blit(back_button_image, back_button_rect)

    selected_stage = None
    new_stage_name = ''
    action = None
    active_input = False  

    def scale_image(image, width, height):
        return pygame.transform.scale(image, (width, height))

    quit_button_image = scale_image(pygame.image.load(quit_button_path).convert_alpha(), 250, 50)
    
    running = True
    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500

    while running:
        cursor_over_input = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                mouse_pos = event.pos
                if add_stage_button_rect.collidepoint(mouse_pos):
                    if new_stage_name:
                        try:
                            query = f"ALTER TABLE score ADD COLUMN `{new_stage_name}` INT DEFAULT NULL"
                            my_cursor.execute(query)

                            query_insert_null = f"""
                            INSERT INTO `stage` (stage_name, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10)
                            VALUES ("{new_stage_name}","", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
                            """
                            my_cursor.execute(query_insert_null)

                            conn.commit()
                            
                            message = f"Stage '{new_stage_name}' added!"
                            message_color = green
                            stages.append(new_stage_name)
                            stage_buttons = {name: pygame.Rect(100, 250 + i * 40, 200, 30) for i, name in enumerate(stages)}
                            new_stage_name = ''
                        except Exception as e:
                            message = f"Error adding stage: Duplicate stage name "+new_stage_name
                            message_color = red
                elif remove_stage_button_rect.collidepoint(mouse_pos):
                    if selected_stage:
                        try:
                            query = f"ALTER TABLE score DROP COLUMN `{selected_stage}`"
                            my_cursor.execute(query)

                            query_delete_row = f"DELETE FROM `stage` WHERE `stage_name` = %s"
                            my_cursor.execute(query_delete_row, (selected_stage,))
                            conn.commit()
                            
                            message = f"Stage '{selected_stage}' removed!"
                            message_color = red
                            stages.remove(selected_stage)
                            stage_buttons = {name: pygame.Rect(100, 250 + i * 40, 200, 30) for i, name in enumerate(stages)}
                            selected_stage = None
                        except Exception as e:
                            message = f"Error removing stage: {str(e)}"
                            message_color = red
                elif back_button_rect.collidepoint(mouse_pos):
                    start_menu_admin(profile, id)

                for key, rect in stage_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        selected_stage = key
                        break
                else:
                    selected_stage = None
                
                if new_stage_input_rect.collidepoint(mouse_pos):
                    active_input = True  
                    cursor_over_input = False
                else:
                    active_input = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    new_stage_name = new_stage_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if new_stage_name:
                        try:
                            query = f"ALTER TABLE score ADD COLUMN `{new_stage_name}` INT DEFAULT NULL"
                            my_cursor.execute(query)
                            conn.commit()
                            message = f"Stage '{new_stage_name}' added!"
                            message_color = green
                            stages.append(new_stage_name)
                            stage_buttons = {name: pygame.Rect(100, 250 + i * 40, 200, 30) for i, name in enumerate(stages)}
                            new_stage_name = ''
                        except Exception as e:
                            message = f"Error adding stage: {str(e)}"
                            message_color = red
                else:
                    new_stage_name += event.unicode

        scroll += 1.1
        if scroll > menu_width:
            scroll = 0
        draw_menu(scroll)

        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time

        selected_image = pygame.image.load('jpg\input_2.png')
        unselected_image = pygame.image.load('jpg\input.png')

        for key, rect in stage_buttons.items():
            button_image = selected_image if selected_stage == key else unselected_image
            scaled_image = pygame.transform.scale(button_image, (rect.width, rect.height))
            
            screen.blit(scaled_image, rect.topleft)

            label_surface = font_small.render(key, True, black)
            label_rect = label_surface.get_rect(center=rect.center)
            screen.blit(label_surface, label_rect)

        screen.blit(input_box_image, new_stage_input_rect.topleft)
        text_surface = font_small.render(new_stage_name, True, black)
        text_rect = text_surface.get_rect(center=new_stage_input_rect.center)
        text_rect.y = new_stage_input_rect.y + (new_stage_input_rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, text_rect)

        if selected_stage:
            pygame.draw.rect(screen, (255, 0, 0), remove_stage_button_rect)

        screen.blit(quit_button_image, add_stage_button_rect)
        screen.blit(back_button_image, back_button_rect)
        draw_text("Add Stage", font_small, black, add_stage_button_rect.centerx, add_stage_button_rect.centery)
        draw_text("Remove Stage", font_small, black, remove_stage_button_rect.centerx, remove_stage_button_rect.centery)
        draw_text("Admin Stage Menu", custom_font1_big, black, screen_width // 2, 200)

        if 'message' in locals():
            message_display(message, 24, screen_width // 2, 850, message_color)
        

        if active_input == cursor_over_input and blink:
            cursor_x = text_rect.right + 5
            cursor_center = new_stage_input_rect.centery
            cursor_top = cursor_center - 10
            cursor_bottom = cursor_center + 10
            pygame.draw.line(screen, black, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)
            
        cursor_over_input = any(
            rect.collidepoint(pygame.mouse.get_pos()) for rect in stage_buttons.values()
        ) or add_stage_button_rect.collidepoint(pygame.mouse.get_pos()) \
           or remove_stage_button_rect.collidepoint(pygame.mouse.get_pos()) \
           or back_button_rect.collidepoint(pygame.mouse.get_pos())
        
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if cursor_over_input else pygame.SYSTEM_CURSOR_ARROW)
        
        pygame.display.flip()

def add_questions_to_stage(profile, id, selected_stage):
    scroll = 0
    message = ""

    input_box_image = pygame.image.load(input_image_path).convert_alpha()
    input_box_image = pygame.transform.scale(input_box_image, (880, 60))  

    question_input_rects = [pygame.Rect(50 + (i % 2) * (880 + 50), 150 + (i // 2) * 70, 880, 60) for i in range(10)]
    answer_input_rects = [pygame.Rect(50 + (i % 2) * (880 + 50), 600 + (i // 2) * 70, 880, 60) for i in range(10)]

    questions = [''] * 10
    answers = [''] * 10

    active_input = None

    button_width = quit_button_image.get_width()
    button_height = quit_button_image.get_height()

    save_button_rect = pygame.Rect(screen_width - 220, screen_height - 60, button_width, button_height)

    existing_data = fetch_existing_data(selected_stage)
    if existing_data:
        questions = list(existing_data[:10])  
        answers = list(existing_data[10:])    

    running = True

    while running: 
        cursor_over_input = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                mouse_pos = event.pos
                if save_button_rect.collidepoint(mouse_pos):
                    message = "Questions and Answers saved"
                    message_color = green
                    message_display(message, 24, screen_width // 2, 950, message_color)
                    time.sleep(0.5)
                    save_questions_to_database(selected_stage, questions, answers)
                    running = False
                elif back_button_rect.collidepoint(mouse_pos):
                    running = False
                    stage_select_menu_admin(profile, id)
                else:
                    for i, rect in enumerate(question_input_rects + answer_input_rects):
                        if rect.collidepoint(mouse_pos):
                            active_input = i
                            break
                    else:
                        active_input = None

            elif event.type == pygame.KEYDOWN and active_input is not None:
                index = active_input
                if event.key == pygame.K_BACKSPACE:
                    if index < 10:
                        questions[index] = questions[index][:-1]
                    else:
                        answers[index - 10] = answers[index - 10][:-1]
                elif event.key == pygame.K_RETURN:
                    if index < 10:
                        questions[index] = questions[index]
                    else:
                        answers[index - 10] = answers[index - 10]
                else:
                    if index < 10:
                        questions[index] += event.unicode
                    else:
                        answers[index - 10] += event.unicode

        scroll += 1.1
        if scroll > menu_width:
            scroll = 0
        draw_menu(scroll)


        for i, rect in enumerate(question_input_rects):
            screen.blit(input_box_image, rect.topleft)
            label_surface = stage_font.render(f'Q{i+1}: {questions[i]}', True, black)
            label_rect = label_surface.get_rect(center=rect.center)
            screen.blit(label_surface, label_rect)
        
        for i, rect in enumerate(answer_input_rects):
            screen.blit(input_box_image, rect.topleft)
            label_surface = stage_font.render(f'A{i+1}: {answers[i]}', True, black)
            label_rect = label_surface.get_rect(center=rect.center)
            screen.blit(label_surface, label_rect)

        screen.blit(quit_button_image, save_button_rect)
        screen.blit(back_button_image, back_button_rect)
        draw_text("Save", font_small, black, save_button_rect.centerx, save_button_rect.centery)
        
        cursor_pos = pygame.mouse.get_pos()
        cursor_over_input = any(
            rect.collidepoint(cursor_pos) for rect in question_input_rects
        ) or any(
            rect.collidepoint(cursor_pos) for rect in answer_input_rects
        ) or save_button_rect.collidepoint(cursor_pos) \
        or back_button_rect.collidepoint(cursor_pos)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if cursor_over_input else pygame.SYSTEM_CURSOR_ARROW)
        
        pygame.display.flip()

def fetch_existing_data(stage_name):
    query = f"""
        SELECT q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, 
               a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 
        FROM `stage` 
        WHERE `stage_name` = %s
        LIMIT 1
    """
    my_cursor.execute(query, (stage_name,))
    result = my_cursor.fetchone()
    if result:
        return result
    return None

def save_questions_to_database(selected_stage, questions, answers):
    query_update_stage = f"""
    UPDATE `stage` 
    SET q1 = %s, q2 = %s, q3 = %s, q4 = %s, q5 = %s, q6 = %s, q7 = %s, q8 = %s, q9 = %s, q10 = %s, 
        a1 = %s, a2 = %s, a3 = %s, a4 = %s, a5 = %s, a6 = %s, a7 = %s, a8 = %s, a9 = %s, a10 = %s
    WHERE stage_name = %s
    """
    data_update_stage = tuple(questions + answers) + (selected_stage,)
    my_cursor.execute(query_update_stage, data_update_stage)
    conn.commit()

def about_us(profile,id):
    about_us_text = [
        "Counting-Strikes is a captivating 2D game that combines",
        "the excitement of gameplay with the challenge of math.",
        "Developed by a passionate team, KHOO ZHONG HAO, ",
        "YAP BOON SIONG, KEE WEN FEI, CHEN JUN VOON, IVAN LAU KAI JUN.",
        "Counting-Strikes offers players an engaging way to improve ",
        "their math skills while enjoying a fun and interactive game.",
        "Join us in making math both entertaining and educational!"
    ]
    scroll = 0

    running = True
            
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound.play()
                mouse_pos = event.pos
                if back_button_rect.collidepoint(event.pos):
                    start_menu(profile,id)

        screen.fill(white)

        scroll += 1   
        if scroll > menu_width:
            scroll = 0 
        draw_menu(scroll)

        heading_text_surface = about_us_heading_font.render("About Us", True, black)
        heading_text_rect = heading_text_surface.get_rect(center=(screen_width // 2, 150))
        screen.blit(heading_text_surface, heading_text_rect)

        y_offset = 250  
        for line in about_us_text:
            text_surface = about_us_font.render(line, True, black)
            text_rect = text_surface.get_rect(topleft=(550, y_offset)) 
            screen.blit(text_surface, text_rect)
            y_offset += 50  

        screen.blit(back_button_image, back_button_rect)

        mouse_pos = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()

def start_menu(profile,id):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    scroll = 0
    running = True

    message = ''

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        print("Start button clicked")
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        
                        stage_select_menu(profile,id)
                    elif profile_button_rect.collidepoint(mouse_pos):
                        print("Profile button clicked")
                        profile_management(profile,id)
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    elif about_button_rect.collidepoint(mouse_pos):
                        print("About Us button clicked")
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        about_us(profile,id)
                    elif savequit_button_rect.collidepoint(mouse_pos):
                        print("Save & Quit button clicked")
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        message = "Progress Saved, Ready to Quit the Game!!"
                        message_color = green
                        if message:
                            message_display(message, 24, screen_width // 2, 900, message_color)
                            pygame.display.flip
                            time.sleep(1)
                            
                        pygame.quit()
                        sys.exit()
                    elif logout_button_rect.collidepoint(mouse_pos) or (screen_width - 220 < mouse_pos[0] < screen_width - 220 + quit_button_size[0] and screen_height - 60 < mouse_pos[1] < screen_height - 60 + quit_button_size[1]):
                        print("Log Out button clicked")
                        message = "Logging out...."
                        message_color = green
                        if message:
                            message_display(message, 24, screen_width // 2, 900, message_color)
                            pygame.display.flip
                            time.sleep(1)
                        logo_menu() 
                    
        scroll += 1  
        if scroll > menu_width:
            scroll = 0 

        draw_menu(scroll)  

        start_button_rect = input_image3.get_rect(center=(screen_width // 2, 270))
        profile_button_rect = input_image3.get_rect(center=(screen_width // 2, 390))
        about_button_rect = input_image3.get_rect(center=(screen_width // 2, 510))
        savequit_button_rect = input_image3.get_rect(center=(screen_width // 2, 630))
        logout_button_rect = pygame.Rect(screen_width - 200, screen_height - 50, 150, 30)

        screen.blit(input_image3, start_button_rect.topleft)
        screen.blit(input_image3, profile_button_rect.topleft)
        screen.blit(input_image3, about_button_rect.topleft)
        screen.blit(input_image3, savequit_button_rect.topleft)
        screen.blit(quit_button_image, (screen_width - 220, screen_height - 60))

        draw_text("Start", custom_font1_big, black, start_button_rect.centerx, start_button_rect.centery)
        draw_text("Profile", custom_font1_big, black, profile_button_rect.centerx, profile_button_rect.centery)
        draw_text("About Us", custom_font1_big, black, about_button_rect.centerx, about_button_rect.centery)
        draw_text("Save & Quit", custom_font1_big, black, savequit_button_rect.centerx, savequit_button_rect.centery)
        draw_text("Log Out", font_small, black, logout_button_rect.centerx, logout_button_rect.centery)

        profile_text_x = 20  
        profile_text_y = screen_height - 60  
        screen.blit(input_image2, (profile_text_x, profile_text_y))
        draw_text(f"Logged in as: {profile}", font_small, black, profile_text_x + 30, profile_text_y + 20, align="left")
        

        if message:
            message_display(message, 24, screen_width // 2, 750, message_color)
            

        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos) or profile_button_rect.collidepoint(mouse_pos) or about_button_rect.collidepoint(mouse_pos) or logout_button_rect.collidepoint(mouse_pos) or savequit_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)             
        
        pygame.display.flip()


def start_menu_admin(profile,id):
    
    font_small = pygame.font.Font('font/Minecraft.ttf', 18)

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    scroll = 0
    running = True

    message = ''

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        print("Stage button clicked")
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        stage_select_menu_admin(profile,id)
                    elif profile_button_rect.collidepoint(mouse_pos):
                        print("Profile button clicked")
                        profile_management_admin(profile,id)
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    elif savequit_button_rect.collidepoint(mouse_pos):
                        print("Save & Quit button clicked")
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        message = "Progress Saved, Ready to Quit the Game!!"
                        message_color = green
                        if message:
                            message_display(message, 24, screen_width // 2, 900, message_color)
                            pygame.display.flip
                            time.sleep(1)
                            
                        pygame.quit()
                        sys.exit()
                    elif logout_button_rect.collidepoint(mouse_pos) or (screen_width - 220 < mouse_pos[0] < screen_width - 220 + quit_button_size[0] and screen_height - 60 < mouse_pos[1] < screen_height - 60 + quit_button_size[1]):
                        print("Log Out button clicked")
                        message = "Logging out...."
                        message_color = green
                        if message:
                            message_display(message, 24, screen_width // 2, 900, message_color)
                            pygame.display.flip
                            time.sleep(1)
                        logo_menu() 
                    
        scroll += 1  
        if scroll > menu_width:
            scroll = 0 

        draw_menu(scroll)  

        start_button_rect = input_image3.get_rect(center=(screen_width // 2, 270))
        profile_button_rect = input_image3.get_rect(center=(screen_width // 2, 390))
        savequit_button_rect = input_image3.get_rect(center=(screen_width // 2, 510))
        logout_button_rect = pygame.Rect(screen_width - 200, screen_height - 50, 150, 30)

        screen.blit(input_image3, start_button_rect.topleft)
        screen.blit(input_image3, profile_button_rect.topleft)
        screen.blit(input_image3, savequit_button_rect.topleft)
        screen.blit(quit_button_image, (screen_width - 220, screen_height - 60))

        draw_text("Stage", custom_font1_big, black, start_button_rect.centerx, start_button_rect.centery)
        draw_text("Profile", custom_font1_big, black, profile_button_rect.centerx, profile_button_rect.centery)
        draw_text("Save & Quit", custom_font1_big, black, savequit_button_rect.centerx, savequit_button_rect.centery)
        draw_text("Log Out", font_small, black, logout_button_rect.centerx, logout_button_rect.centery)

        profile_text_x = 20  
        profile_text_y = screen_height - 60 
        screen.blit(input_image2, (profile_text_x, profile_text_y))
        draw_text(f"Admin as: {profile}", font_small, black, profile_text_x + 30, profile_text_y + 20, align="left")

        if message:
            message_display(message, 24, screen_width // 2, 750, message_color)

        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos) or profile_button_rect.collidepoint(mouse_pos) or logout_button_rect.collidepoint(mouse_pos) or savequit_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)         
        
        pygame.display.flip()



def check_forget_email(email):
    query = "SELECT nickname, password FROM player WHERE email = %s"
    my_cursor.execute(query, (email,))
    result = my_cursor.fetchone()
    if result:
        name_otp, password_otp = result
        return name_otp, password_otp
    return None

def check_forget_email_admin(email):
    query = "SELECT nickname, password FROM admin WHERE email = %s"
    my_cursor.execute(query, (email,))
    result = my_cursor.fetchone()
    if result:
        name_otp, password_otp = result
        return name_otp, password_otp
    return None

def forget_password():
    running = True
    email = ''
    login_message = ''
    scroll = 0

    while running:
        clock = pygame.time.Clock()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        if user == "player":
            inputs = {
                "Email": (350, 780, 500, 30, 32),
            }             
            responses = multi_text_input2(inputs)
            email = responses["Email"]  


            if email:
                user_data = check_forget_email(email)
                if user_data:
                    name_otp, password_otp = user_data
                    receiver_email = email
                    otp_code(name_otp, receiver_email)
                    send_password_email(name_otp, password_otp, receiver_email)
                    login_message = f"Password has been sent to {receiver_email}, login to play."
                    login_message_color = green
                    if login_message:
                        message_display(login_message, 24, screen_width // 2, 900, login_message_color)
                        pygame.display.flip()
                        time.sleep(1)
                    main_menu()
                else:
                    login_message = "Email not found"
                    login_message_color = red
                    if login_message:
                        message_display(login_message, 24, screen_width // 2, 900, login_message_color)
                        pygame.display.flip()
                        time.sleep(1)
                    logo_menu()

        elif user == "admin":
            inputs = {
                "Email": (350, 780, 500, 30, 32),
            }             
            responses = multi_text_input2(inputs)
            email = responses["Email"]  


            if email:
                user_data = check_forget_email_admin(email)
                if user_data:
                    name_otp, password_otp = user_data
                    receiver_email = email
                    otp_code(name_otp, receiver_email)
                    send_password_email(name_otp, password_otp, receiver_email)
                    login_message = f"Password has been sent to {receiver_email}, login to play."
                    login_message_color = green
                    if login_message:
                        message_display(login_message, 24, screen_width // 2, 900, login_message_color)
                        pygame.display.flip()
                        time.sleep(1)
                    main_menu()
                else:
                    login_message = "Email not found"
                    login_message_color = red
                    if login_message:
                        message_display(login_message, 24, screen_width // 2, 900, login_message_color)
                        pygame.display.flip()
                        time.sleep(1)
                    logo_menu()
        
        scroll += 10   
        if scroll > menu_width:
            scroll = 0 
        
        screen.fill(white)
        draw_menu(scroll)

def main_menu2():
    global screen
    global user
    running = True
    user = ""
    scroll = 0
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                mouse_pos = pygame.mouse.get_pos()
                
                if quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

                player_button_rect = login_button_image.get_rect(center=(screen_width // 2, 225))
                
                if player_button_rect.collidepoint(mouse_pos):
                    user = "player"
                    return user

                admin_button_rect = register_button_image.get_rect(center=(screen_width // 2, 525))
                
                if admin_button_rect.collidepoint(mouse_pos):
                    user = "admin"
                    return user

        scroll += 1.7  
        if scroll > menu_width:
            scroll = 0 
               
        screen.fill(white)
        draw_menu(scroll)

        player_button_rect = login_button_image.get_rect(center=(screen_width // 2, 225))
        admin_button_rect = register_button_image.get_rect(center=(screen_width // 2, 525))
        screen.blit(login_button_image, player_button_rect)
        screen.blit(register_button_image, admin_button_rect)

        text_surf, text_rect = text_objects("Player", custom_font1_big, black)
        text_rect.center = player_button_rect.center
        screen.blit(text_surf, text_rect)
        
        text_surf, text_rect = text_objects("Admin", custom_font1_big, black)
        text_rect.center = admin_button_rect.center
        screen.blit(text_surf, text_rect)

        quit_button_rect = quit_button_image.get_rect(topleft=(40, 40))
        screen.blit(quit_button_image, quit_button_rect)
        text_surf, text_rect = text_objects("Quit", custom_font1_small, black)
        text_rect.center = quit_button_rect.center
        screen.blit(text_surf, text_rect)

        mouse_pos = pygame.mouse.get_pos()
        if player_button_rect.collidepoint(mouse_pos) or admin_button_rect.collidepoint(mouse_pos) or quit_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        pygame.display.flip()
        
        pygame.display.flip()
        

def main_menu():
    global screen
    
    running = True
    login_mode = False 
    email = ''
    password = ''
    login_message = ''
    scroll = 0
    profile= ''
    

    while running:
        clock = pygame.time.Clock()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                mouse_pos = pygame.mouse.get_pos()
                
                if quit_button_rect.collidepoint(mouse_pos):
                    time.sleep(0.5)
                    pygame.quit()
                    sys.exit()

                login_button_rect = login_button_image.get_rect(center=(screen_width // 2, 225))
                
                if login_button_rect.collidepoint(mouse_pos):
                    main_menu2()
                    if user == "player":
                        inputs = {
                            "Email": (350, 450, 300, 30, 32),
                            "Password": (350, 850, 300, 30, 32)
                        }
                        responses = multi_text_input(inputs, input_image_path, eye_image_path, eye_closed_image_path)
                        email = responses["Email"]
                        password = responses["Password"]
                        if email and password:
                            if check_login(email, password ):
                                login_message = "Login Successful!"
                                login_message_color = green
                                profile = email
                                query = "SELECT id FROM player WHERE email = %s"
                                my_cursor.execute(query, (profile,))
                                result = my_cursor.fetchone()
                                if result:
                                    id = result[0]  
                                    print(f"Profile ID: {id}")
                                else:
                                    print("No profile found for the given email.")
                                if login_message:
                                    message_display(login_message, 24, screen_width // 2, 750, login_message_color)
                                    pygame.display.flip
                                    time.sleep(1)
                                    start_menu(profile,id)
                                    
                            else:
                                login_message = "Login Failed!"
                                login_message_color = red
                        else:
                            login_message = "Please fill in all fields."
                            login_message_color = red
                    
                    elif user == "admin": 
                        inputs = {
                            "Email": (350, 450, 300, 30, 32),
                            "Password": (350, 850, 300, 30, 32)
                        }
                        responses = multi_text_input(inputs, input_image_path, eye_image_path, eye_closed_image_path)
                        email = responses["Email"]
                        password = responses["Password"]
                        if email and password:
                            if check_login_admin(email, password ):
                                login_message = "Login Successful!"
                                login_message_color = green
                                profile = email
                                query = "SELECT id FROM ADMIN WHERE email = %s"
                                my_cursor.execute(query, (profile,))
                                result = my_cursor.fetchone()
                                if result:
                                    id = result[0] 
                                    print(f"Profile ID: {id}")
                                else:
                                    print("No profile found for the given email.")
                                if login_message:
                                    message_display(login_message, 24, screen_width // 2, 750, login_message_color)
                                    pygame.display.flip
                                    time.sleep(1)
                                    start_menu_admin(profile,id)
                                    
                            else:
                                login_message = "Login Failed!"
                                login_message_color = red
                        else:
                            login_message = "Please fill in all fields."
                            login_message_color = red

                register_button_rect = register_button_image.get_rect(center=(screen_width // 2, 525))
                
                if register_button_rect.collidepoint(mouse_pos):
                    main_menu2()
                    if user == "player":
                        register_inputs = {
                            "New Username": (150, 300, 500, 30, 32),
                            "Age": (150, 550, 100, 30, 32),
                            "Email": (150, 800, 500, 30, 32),
                            "Password": (150, 1050, 500, 30, 32)
                        }
                        responses = multi_text_input(register_inputs, input_image_path, eye_image_path, eye_closed_image_path)

                        if all(responses.values()):
                            valid, message = validate_user_input(responses["New Username"], responses["Age"], responses["Email"], responses["Password"])
                            
                            if valid:
                                name_otp = responses["New Username"]
                                receiver_email = responses["Email"]
                                otp_code(name_otp, receiver_email)
                                if register_user(responses["New Username"], responses["Age"], responses["Email"], responses["Password"]):
                                    
                                    login_message = "Registration Successful! Login your account to play."
                                    login_message_color = green
                                    query = "SELECT id FROM player WHERE email = %s"
                                    my_cursor.execute(query, (receiver_email,))
                                    result = my_cursor.fetchone()
                                    id_2 = result[0]
                                    my_cursor.execute("SHOW COLUMNS FROM score")
                                    columns = my_cursor.fetchall()

                                    second_column_name = columns[1][0]

                                    query_2 = f"INSERT INTO `score` (`id`, `{second_column_name}`) VALUES ('{id_2}', null)"
                                    my_cursor.execute(query_2)
                                    conn.commit()
                                else:
                                    login_message = "Email exist! Please try again."
                                    login_message_color = red
                            else:
                                login_message = f"Registration Failed: {message}"
                                login_message_color = red
                        else:
                            login_message = "Please fill in all fields."
                            login_message_color = red

                    elif user == "admin": 
                        register_inputs = {
                            "New Username": (150, 300, 500, 30, 32),
                            "Age": (150, 550, 100, 30, 32),
                            "Admin Code": (150, 800, 100, 30, 32),
                            "Email": (150, 1050, 500, 30, 32),
                            "Password": (150, 1300, 500, 30, 32)
                        }
                        responses = multi_text_input(register_inputs, input_image_path, eye_image_path, eye_closed_image_path)
                        
                        if all(responses.values()):
                            valid, message = validate_admin_input(responses["New Username"], responses["Age"], responses["Email"], responses["Password"], responses["Admin Code"])
                            
                            if valid:
                                name_otp = responses["New Username"]
                                receiver_email = responses["Email"]
                                otp_code(name_otp, receiver_email)
                                if register_admin(responses["New Username"], responses["Age"], responses["Email"], responses["Password"]):
                                    
                                    login_message = "Registration Successful! Login your account to play."
                                    login_message_color = green
                                    
                                else:
                                    login_message = "Email exist! Please try again."
                                    login_message_color = red
                            else:
                                login_message = f"Registration Failed: {message}"
                                login_message_color = red
                        else:
                            login_message = "Please fill in all fields."
                            login_message_color = red


        scroll += 10  
        if scroll > menu_width:
            scroll = 0 
               
        screen.fill(white)
        draw_menu(scroll)

        login_button_rect = login_button_image.get_rect(center=(screen_width // 2, 225))
        register_button_rect = register_button_image.get_rect(center=(screen_width // 2, 525))
        screen.blit(login_button_image, login_button_rect)
        screen.blit(register_button_image, register_button_rect)

        text_surf, text_rect = text_objects("Login", custom_font1_big, black)
        text_rect.center = login_button_rect.center
        screen.blit(text_surf, text_rect)
        
        text_surf, text_rect = text_objects("Register", custom_font1_small, black)
        text_rect.center = register_button_rect.center
        screen.blit(text_surf, text_rect)

        quit_button_rect = quit_button_image.get_rect(topleft=(40, 40))
        screen.blit(quit_button_image, quit_button_rect)
        text_surf, text_rect = text_objects("Quit", custom_font1_small, black)
        text_rect.center = quit_button_rect.center
        screen.blit(text_surf, text_rect)

        if login_message:
            message_display(login_message, 24, screen_width // 2, 750, login_message_color)

        mouse_pos = pygame.mouse.get_pos()
        if login_button_rect.collidepoint(mouse_pos) or register_button_rect.collidepoint(mouse_pos) or quit_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        pygame.display.flip()

def logo_menu():
    global screen
    
    running = True
    logo_y = screen_height // 2
    logo_speed = 1
    scroll = 0

    while running:
        clock = pygame.time.Clock()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                main_menu() 

        logo_y += logo_speed

        if logo_y <= 100:
            logo_speed = 1 
        elif logo_y + logo_image.get_height() + 300 >= screen_height:
            logo_speed = -1  

        scroll += 10
        if scroll > menu_width:
            scroll = 0

        draw_menu(scroll)  

        screen.blit(logo_image, ((screen_width - logo_image.get_width()) // 2, logo_y))

        render_text('font/Minecraft.ttf', "Click Here !", 20, screen_width // 2, screen_height - 50, pygame.Color('white'))
        
        pygame.display.flip()

def profile_management(profile,id):

    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500
    scroll = 0
    
    font_small = pygame.font.Font('font/Minecraft.ttf', 18)

    query = "SELECT id, nickname, age, password FROM player WHERE email = %s"
    my_cursor.execute(query, (profile,))
    user_data = my_cursor.fetchone()
    if user_data:
        user_id, nickname, age, password = user_data
    else:
        user_id = nickname = age = password = ''

    input_boxes = {
        "id": str(user_id),
        "nickname": nickname,
        "age": str(age),
        "password": password
    }

    input_rects = {
        "id": button_image.get_rect(topleft=(screen_width//3, 170)), 
        "nickname": button_image.get_rect(topleft=(screen_width//3, 300)), 
        "age": button_image.get_rect(topleft=(screen_width//3, 430)), 
        "password": button_image.get_rect(topleft=(screen_width//3, 560)) 
    }

    margins = {
        "id": 100,
        "nickname": 250,
        "age": 120,
        "password": 240
    }

    active_box = None

    button_width = quit_button_image.get_width()
    button_height = quit_button_image.get_height()

    save_button_rect = pygame.Rect(screen_width - 220, screen_height - 60, button_width, button_height)
    logged_in_rect = pygame.Rect(20, screen_height - 60, 200, 50)  

    running = True
    message = ''
    cursor_length = 35
    label_spacing = -30

    while running:
        cursor_over_input = False  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                mouse_pos = event.pos
                if save_button_rect.collidepoint(mouse_pos):
                    new_data = (
                        input_boxes["nickname"],
                        int(input_boxes["age"]),
                        input_boxes["password"],
                        profile
                    )
                    query = "UPDATE player SET nickname = %s, age = %s, password = %s WHERE email = %s"
                    my_cursor.execute(query, new_data)
                    conn.commit()
                    message = "Profile Updated Successfully!"
                    if message:
                        message_display(message, 24, screen_width // 2, 700, green)
                        pygame.display.flip
                    time.sleep(1)
                    start_menu(profile,id)
                elif back_button_rect.collidepoint(mouse_pos):
                    start_menu(profile,id)
                for key, rect in input_rects.items():
                    if key != "id" and rect.collidepoint(mouse_pos):
                        active_box = key
                        break
                else:
                    active_box = None
            elif event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_RETURN:
                    active_box = None
                elif event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box] = input_boxes[active_box][:-1]
                else:
                    input_boxes[active_box] += event.unicode

        scroll += 1.2
        if scroll > screen_width:  
            scroll = 0
        draw_menu(scroll) 

        for key, rect in input_rects.items():
            if key == "id":
                label_text = "ID: "
            elif key == "nickname":
                label_text = "Nickname: "
            elif key == "age":
                label_text = "Age: "
            elif key == "password":
                label_text = "Password: "
            else:
                label_text = ""
            screen.blit(button_image, rect)

            label_surface = custom_font1.render(label_text, True, black)
            label_rect = label_surface.get_rect(midleft=(rect.x - label_spacing, rect.centery))
            screen.blit(label_surface, label_rect)

            margin_left = margins.get(key, 50)

            text_surface = custom_font1.render(input_boxes[key], True, black)
            text_rect = text_surface.get_rect(left=rect.x + margin_left, centery=rect.centery)
            screen.blit(text_surface, text_rect)

            if active_box == key and blink:
                cursor_x = text_rect.right + 2 
                cursor_center = text_rect.centery
                cursor_top = cursor_center - cursor_length // 2
                cursor_bottom = cursor_center + cursor_length // 2
                pygame.draw.line(screen, black, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

            if rect.collidepoint(pygame.mouse.get_pos()):
                cursor_over_input = True

        if back_button_rect.collidepoint(pygame.mouse.get_pos()) or save_button_rect.collidepoint(pygame.mouse.get_pos()):
            cursor_over_input = True

        if cursor_over_input:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        screen.blit(input_image2, (logged_in_rect.x, logged_in_rect.y))
        draw_text(f"Logged in as: {profile}", font_small, black, logged_in_rect.x + 30, logged_in_rect.y + 20, align="left")

        screen.blit(quit_button_image, save_button_rect) 
        screen.blit(back_button_image, back_button_rect)
        draw_text("Save", font_small, black, save_button_rect.centerx, save_button_rect.centery)

        draw_text("Profile Management", custom_font1_big, black, screen_width // 2, 85)

        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time

        pygame.display.flip()

def profile_management_admin(profile,id):

    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500
    scroll = 0

    font_small = pygame.font.Font('font/Minecraft.ttf', 18)

    query = "SELECT id, nickname, age, password FROM admin WHERE email = %s"
    my_cursor.execute(query, (profile,))
    user_data = my_cursor.fetchone()
    if user_data:
        user_id, nickname, age, password = user_data
    else:
        user_id = nickname = age = password = ''

    input_boxes = {
        "id": str(user_id),
        "nickname": nickname,
        "age": str(age),
        "password": password
    }

    input_rects = {
        "id": button_image.get_rect(topleft=(screen_width//3, 170)), 
        "nickname": button_image.get_rect(topleft=(screen_width//3, 300)), 
        "age": button_image.get_rect(topleft=(screen_width//3, 430)), 
        "password": button_image.get_rect(topleft=(screen_width//3, 560)) 
    }

    margins = {
        "id": 100,
        "nickname": 250,
        "age": 120,
        "password": 240
    }

    active_box = None

    button_width = quit_button_image.get_width()
    button_height = quit_button_image.get_height()

    save_button_rect = pygame.Rect(screen_width - 220, screen_height - 60, button_width, button_height)
    logged_in_rect = pygame.Rect(20, screen_height - 60, 200, 50)  

    running = True
    message = ''
    cursor_length = 35
    label_spacing = -30
    pygame.mixer.music.play(-1)

    while running: 
        cursor_over_input = False  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                mouse_pos = event.pos
                if save_button_rect.collidepoint(mouse_pos):
                    new_data = (
                        input_boxes["nickname"],
                        int(input_boxes["age"]),
                        input_boxes["password"],
                        profile
                    )
                    query = "UPDATE admin SET nickname = %s, age = %s, password = %s WHERE email = %s"
                    my_cursor.execute(query, new_data)
                    conn.commit()
                    message = "Profile Updated Successfully!"
                    if message:
                        message_display(message, 24, screen_width // 2, 700, green)
                        pygame.display.flip
                    time.sleep(1)
                    start_menu_admin(profile,id)
                elif back_button_rect.collidepoint(mouse_pos):
                    start_menu_admin(profile,id)
                for key, rect in input_rects.items():
                    if key != "id" and rect.collidepoint(mouse_pos): 
                        active_box = key
                        break
                else:
                    active_box = None
            elif event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_RETURN:
                    active_box = None
                elif event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box] = input_boxes[active_box][:-1]
                else:
                    input_boxes[active_box] += event.unicode

        scroll += 1.2
        if scroll > screen_width:  
            scroll = 0
        draw_menu(scroll) 

        for key, rect in input_rects.items():
            if key == "id":
                label_text = "ID: "
            elif key == "nickname":
                label_text = "Nickname: "
            elif key == "age":
                label_text = "Age: "
            elif key == "password":
                label_text = "Password: "
            else:
                label_text = ""
            screen.blit(button_image, rect)

            label_surface = custom_font1.render(label_text, True, black)
            label_rect = label_surface.get_rect(midleft=(rect.x - label_spacing, rect.centery))
            screen.blit(label_surface, label_rect)

            margin_left = margins.get(key, 50)

            text_surface = custom_font1.render(input_boxes[key], True, black)
            text_rect = text_surface.get_rect(left=rect.x + margin_left, centery=rect.centery)
            screen.blit(text_surface, text_rect)

            if active_box == key and blink:
                cursor_x = text_rect.right + 2 
                cursor_center = text_rect.centery
                cursor_top = cursor_center - cursor_length // 2
                cursor_bottom = cursor_center + cursor_length // 2
                pygame.draw.line(screen, black, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

            if rect.collidepoint(pygame.mouse.get_pos()):
                cursor_over_input = True

        if back_button_rect.collidepoint(pygame.mouse.get_pos()) or save_button_rect.collidepoint(pygame.mouse.get_pos()):
            cursor_over_input = True

        if cursor_over_input:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        screen.blit(input_image2, (logged_in_rect.x, logged_in_rect.y))
        draw_text(f"Admin as: {profile}", font_small, black, logged_in_rect.x + 30, logged_in_rect.y + 20, align="left")

        screen.blit(quit_button_image, save_button_rect)
        screen.blit(back_button_image, back_button_rect)
        draw_text("Save", font_small, black, save_button_rect.centerx, save_button_rect.centery)

        draw_text("Admin Profile Management", custom_font1_big, black, screen_width // 2, 85)

        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time

        pygame.display.flip()

logo_image = pygame.image.load('jpg/logo2.png').convert_alpha()
logo_menu()

my_cursor.close()
conn.close()
print("Connection closed")

pygame.quit()