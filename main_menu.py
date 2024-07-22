import pygame
import pymysql
import time
import sys
import random
import smtplib

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 1920 #1000
screen_height = 1080 #800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Counting-Strike')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)
green = (0, 255, 0)
red = (255, 0, 0)

# Load font
custom_font1 = pygame.font.Font('font/Minecraft.ttf', 40)
custom_font1_small = pygame.font.Font('font/Minecraft.ttf', 37)
custom_font_smallest = pygame.font.Font('font/Minecraft.ttf', 15)
custom_font1_big = pygame.font.Font('font/Minecraft.ttf', 50)
custom_font1_small1 = pygame.font.Font('font/Minecraft.ttf', 32)
about_us_font = pygame.font.Font('font/Minecraft.ttf', 30)
about_us_heading_font = pygame.font.Font('font/Minecraft.ttf', 60)

# Load button images
login_button_image = pygame.image.load(r'jpg/main_menu_button.png')
register_button_image = pygame.image.load(r'jpg/main_menu_button.png')
back_button_path = 'jpg/back_button.png'
quit_button_path = 'jpg/quit_button.png'

# Load input images
input_image_path = 'jpg/input.png'

# Load button image and scale it
button_image_orig = pygame.image.load(input_image_path).convert_alpha()
button_image_size = (700, 100)  # Adjust the size as needed
button_image = pygame.transform.scale(button_image_orig, button_image_size)

# Scale images to fit the buttons
login_button_image = pygame.transform.scale(login_button_image, (200, 200))
register_button_image = pygame.transform.scale(register_button_image, (200, 200))

# Load menu image
menu_image = pygame.image.load(r'jpg\menu2.png').convert_alpha()
menu_image = pygame.transform.scale(menu_image, (screen_width, screen_height))
menu_width = menu_image.get_width()

quit_button_image_orig = pygame.image.load(quit_button_path).convert_alpha()
quit_button_size = (200, 50)
quit_button_image = pygame.transform.scale(quit_button_image_orig, quit_button_size)

# Load back button image
back_button_image_orig = pygame.image.load(back_button_path).convert_alpha()
button_size = (100, 100)  # Adjust size as needed
back_button_image = pygame.transform.scale(back_button_image_orig, button_size)
back_button_rect = back_button_image.get_rect()
back_button_rect.topleft = (40, 40)  # Adjust position as needed

# Database connection
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sdp'
)
my_cursor = conn.cursor()

# Load eye image path
eye_closed_image_path="jpg/password_off.png"
eye_image_path="jpg/password_on.png"

# Scale images to fit the buttons
input_image = pygame.image.load(input_image_path).convert_alpha()
input_image = pygame.transform.scale(input_image, (350, 100))
input_image2 = pygame.transform.scale(input_image, (400, 50))
input_image3 = pygame.transform.scale(input_image, (450, 100))

OTP = random.randint(100000,999999)      #generating a randomm 6-digit OTP

#setting up server
server = smtplib.SMTP('smtp.gmail.com',587)
#server = smtplib.SMTP('64.233.184.108',587)           #IP address of smtp.gmail.com to bypass DNS resolution
server.starttls()


# Function to display message on screen
def message_display(text, font_size, x, y, color):
    font = pygame.font.Font(None, font_size)
    text_surf, text_rect = text_objects(text, font, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.flip()

# Function to display text on screen
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
        # Display login message if any
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
    blink_interval = 500  # Adjust blinking interval as needed
    valid_receiver_email = email_verification(receiver_email)
    password = "pckqciqvdvnrebrk"
    server.login("boonmonopoly4@gmail.com", password)

    body = "Dear " + name_otp + ",\n\nYour OTP is " + str(OTP) + "."
    subject = "OTP Verification by Counting-Strike"
    message = f'Subject: {subject}\n\n{body}'

    server.sendmail("boonmonopoly4@gmail.com", valid_receiver_email, message)

    print("OTP has been sent to " + valid_receiver_email)
    message2 = f"OTP has been sent to {receiver_email}"

    # Display OTP sent message
    if message2:
        message_display(message2, 24, screen_width // 2, 900, green)
        pygame.display.flip()
        time.sleep(1)

    # Define inputs dictionary
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
        
        # Calculate blinking cursor visibility
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time

        scroll += 1.7
        if scroll > screen_width:  # Adjust as needed
            scroll = 0
        # Draw menu background with parallax effect
        draw_menu(scroll)

        # Draw input box
        screen.blit(input_image, (screen_width // 2 - input_image.get_width() // 2, screen_height // 2 - input_image.get_height() // 2))

        # Draw prompt text
        enter_otp_text = custom_font1.render("Enter OTP code:", True, black)
        screen.blit(enter_otp_text, ((screen_width - enter_otp_text.get_width()) // 2, (screen_height - input_image.get_height()) // 2 - 50))

        # Draw user input text
        text_surface = custom_font1_small.render(user_text, True, black)
        text_rect = text_surface.get_rect(center=input_image.get_rect(center=(screen_width // 2, screen_height // 2)).center)
        screen.blit(text_surface, text_rect.topleft)

        # Draw blinking cursor if active box is being typed in
        if blink and input_active:
            cursor_x = text_rect.right + 2  # Adjust cursor position
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
        # Display OTP verification result
        if message2:
            message_display(message2, 24, screen_width // 2, 700, green)
            pygame.display.flip()
            time.sleep(1)
    else:
        print("invalid OTP")
        message2 = "Invalid OTP"
        # Display OTP verification result
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
    
# Function to check login credentials
def check_login(email, password):
    query = "SELECT * FROM USER WHERE email=%s AND password=%s"
    my_cursor.execute(query, (email, password))
    result = my_cursor.fetchone()
    return result is not None

# Function to check login credentials
def check_login_admin(email, password):
    query = "SELECT * FROM ADMIN WHERE email=%s AND password=%s"
    my_cursor.execute(query, (email, password))
    result = my_cursor.fetchone()
    return result is not None

# Function to register new user
def register_user(username, age, email, password):
    try:
        query = "INSERT INTO USER (nickname, age, email, password) VALUES (%s, %s, %s, %s)"
        my_cursor.execute(query, (username, age, email, password))
        conn.commit()
        return True
    except pymysql.Error as e:
        message_display(f"Error: {e}", 24, screen_width // 2, 500, black)
        return False
    
# Function to register new user
def register_admin(username, age, email, password):
    try:
        query = "INSERT INTO ADMIN (nickname, age, email, password) VALUES (%s, %s, %s, %s)"
        my_cursor.execute(query, (username, age, email, password))
        conn.commit()
        return True
    except pymysql.Error as e:
        message_display(f"Error: {e}", 24, screen_width // 2, 500, black)
        return False

# Function to display text on screen
def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# Function to display message on screen
def message_display(text, font_size, x, y, color):
    font = pygame.font.Font(None, font_size)
    text_surf, text_rect = text_objects(text, font, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.flip()

    # Function to handle multiple text inputs
def multi_text_input2(inputs):
    
    # Adjust input box dimensions to match button image size
    input_boxes = {prompt: pygame.Rect((screen_width - button_image_size[0]) // 2, (y + 100 - button_image_size[1]) // 2, button_image_size[0], button_image_size[1]) for prompt, (x, y, width, height, font_size) in inputs.items()}
    
    # Adjust input box dimensions to match button image size
    colors = {prompt: pygame.Color('lightskyblue3') for prompt in inputs}
    active_box = None
    texts = {prompt: '' for prompt in inputs}
    done = False
    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500  # Adjust blinking interval as needed
    scroll = 0
        
    while not done:
        # Handle events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for prompt, box in input_boxes.items():
                    if box.collidepoint(event.pos):
                        active_box = prompt
                        colors[prompt] = pygame.Color('dodgerblue2')
                    else:
                        colors[prompt] = pygame.Color('lightskyblue3')
                        
                    if back_button_rect.collidepoint(event.pos):
                        main_menu() # Return from main_menu() if back button clicked
                        
            if event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        texts[active_box] = texts[active_box][:-1]
                    else:
                        texts[active_box] += event.unicode
        
        # Calculate blinking cursor visibility
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time
        
        scroll += 1.7
        if scroll > screen_width:  # Adjust as needed
            scroll = 0
        # Draw menu background with parallax effect
        draw_menu(scroll)

        # Draw input boxes and text
        for prompt, box in input_boxes.items():
            # Calculate position to center the button image within the input box
            button_x = box.x + (box.width - button_image_size[0]) // 2
            button_y = box.y + (box.height - button_image_size[1]) // 2

            # Draw the button image centered within the input box
            screen.blit(button_image, (button_x, button_y))
            
            # Draw text entered into the input box
            font = pygame.font.Font(None, inputs[prompt][4])
            display_text = texts[prompt]
            
            text_surf = custom_font1.render(prompt + ": " + display_text, True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            text_rect.center = (box.x + box.width // 2, box.y + box.height // 2)
            screen.blit(text_surf, text_rect)

            # Draw blinking cursor if active box is being typed in
            if active_box == prompt and blink:
                cursor_x = text_rect.right + 2  # Adjust cursor position
                cursor_top = text_rect.top + (text_rect.height - font.get_linesize()) // 2
                cursor_bottom = cursor_top + font.get_linesize()
                pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

            # Check if mouse is over any input box to change cursor
            mouse_pos = pygame.mouse.get_pos()
            for box in input_boxes.values():
                if box.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
            else:
                # If not over an input box, check if over any other interactive elements
                if back_button_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        

        screen.blit(back_button_image, back_button_rect)
        pygame.display.flip()

    return texts

# Function to handle multiple text inputs
def multi_text_input(inputs, input_image_path, eye_image_path, eye_closed_image_path):
    
    # Adjust input box dimensions to match button image size
    input_boxes = {prompt: pygame.Rect((screen_width - button_image_size[0]) // 2, (y + 100 - button_image_size[1]) // 2, button_image_size[0], button_image_size[1]) for prompt, (x, y, width, height, font_size) in inputs.items()}
    
    # Adjust input box dimensions to match button image size
    colors = {prompt: pygame.Color('lightskyblue3') for prompt in inputs}
    active_box = None
    texts = {prompt: '' for prompt in inputs}
    done = False
    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500  # Adjust blinking interval as needed
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

    # Toggle button for password visibility (if eye images provided)
    show_password = False if eye_closed_image else True  # Default to show password if no closed eye image
    eye_button_rect = None
    if eye_image and eye_closed_image:
        eye_button_rect = eye_image.get_rect()
        eye_button_rect.center = ( screen_width// 2, input_boxes["Password"].bottom + 30)  # Adjust position
        
    while not done:
        # Handle events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for prompt, box in input_boxes.items():
                    if box.collidepoint(event.pos):
                        active_box = prompt
                        colors[prompt] = pygame.Color('dodgerblue2')
                    else:
                        colors[prompt] = pygame.Color('lightskyblue3')
                        
                    if back_button_rect.collidepoint(event.pos):
                        main_menu() # Return from main_menu() if back button clicked
                    
                    # Check if eye button clicked and adjust position if needed
                    if eye_button_rect and eye_button_rect.collidepoint(event.pos) and prompt == "Password":
                        show_password = not show_password

                    #forget password
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
                        display_text = '*' * len(texts[prompt])  # Display asterisks for password input
        
        # Calculate blinking cursor visibility
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time
        
        scroll += 1.7
        if scroll > screen_width:  # Adjust as needed
            scroll = 0
        # Draw menu background with parallax effect
        draw_menu(scroll)

        # Draw input boxes and text
        for prompt, box in input_boxes.items():
            # Calculate position to center the button image within the input box
            button_x = box.x + (box.width - button_image_size[0]) // 2
            button_y = box.y + (box.height - button_image_size[1]) // 2

            # Draw the button image centered within the input box
            screen.blit(button_image, (button_x, button_y))
            
            # Draw text entered into the input box
            font = pygame.font.Font(None, inputs[prompt][4])
            display_text = texts[prompt]
            if prompt == "Password" and not show_password:
                display_text = '*' * len(texts[prompt])  # Display asterisks for password input
            text_surf = custom_font1.render(prompt + ": " + display_text, True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            text_rect.center = (box.x + box.width // 2, box.y + box.height // 2)
            screen.blit(text_surf, text_rect)

            # Draw blinking cursor if active box is being typed in
            if active_box == prompt and blink:
                cursor_x = text_rect.right + 2  # Adjust cursor position
                cursor_top = text_rect.top + (text_rect.height - font.get_linesize()) // 2
                cursor_bottom = cursor_top + font.get_linesize()
                pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

            #Draw forget password button
            font_small = pygame.font.Font('font/Minecraft.ttf', 18) 
            screen.blit(quit_button_image, (screen_width - 220, screen_height - 60))   
            logout_button_rect = pygame.Rect(screen_width - 200, screen_height - 50, 150, 30)
            draw_text("Forget Password", font_small, black, logout_button_rect.centerx, logout_button_rect.centery)

            # Check if mouse is over any input box to change cursor
            mouse_pos = pygame.mouse.get_pos()
            for box in input_boxes.values():
                if box.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
            else:
                # If not over an input box, check if over any other interactive elements
                if eye_button_rect.collidepoint(mouse_pos) or back_button_rect.collidepoint(mouse_pos) or logout_button_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        # Draw show password button (if eye images provided)
        if eye_image and eye_closed_image:
            screen.blit(eye_closed_image if not show_password else eye_image, eye_button_rect)

        screen.blit(back_button_image, back_button_rect)
        pygame.display.flip()

    return texts

# Function to render text on the screen
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

# Function to validate user input
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

# Function to validate admin input
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

# Function to draw the menu background with parallax scrolling effect
def draw_menu(scroll):
    for x in range(5):
        screen.blit(menu_image, ((x * menu_width) - scroll, 0))

# Define a function to get stage scores for a specific ID
def get_stage_scores(id):

    # Fetch stage scores for the given ID
    query = "SELECT stage1, stage2, stage3, stage4, stage5, stage6, stage7, stage8 FROM stage WHERE ID = %s"
    my_cursor.execute(query, (id,))
    result = my_cursor.fetchone()

    if result:
        # Convert the result to a list of scores
        scores = []
        for score in result:
            # Append score if not None (or NULL in database terms)
            if score is not None:
                scores.append(score)
            else:
                scores.append(None)
        print("Fetched scores from database:", scores)  # Debugging step
        return scores
    else:
        return []

def stage_select_menu(profile,id):
    scroll = 0
    message = ""

    # Load images and scale them
    stage_image_orig = pygame.image.load('jpg/main_menu_button.png').convert_alpha()
    stage_image_size = (150, 150)
    stage_image = pygame.transform.scale(stage_image_orig, stage_image_size)

    stage_image_orig2 = pygame.image.load('jpg/stage_button2.png').convert_alpha()
    stage_image_size2 = (150, 150)
    stage_image2 = pygame.transform.scale(stage_image_orig2, stage_image_size2)

    # Scale images to block size
    block_width = 150
    block_height = 150

    # Define block positions
    blocks = []
    rows = 3
    cols = 3

    # Calculate padding
    padding_x = (screen.get_width() - (cols * block_width)) // (cols + 1)
    padding_y = (screen.get_height() - (rows * block_height)) // (rows + 5)

    for row in range(rows):
        for col in range(cols):
            x = padding_x + col * (block_width + padding_x)
            y = padding_y + row * (block_height + padding_y) + 120
            blocks.append(pygame.Rect(x, y, block_width, block_height))

    # Prepare texts for each stage
    texts = [f'Stage {i+1}' for i in range(8)] + ['Soon']

    # Get stage scores from the database
    scores = get_stage_scores(id)

    print(f"Scores: {scores}")

    # Render text onto each image
    stage_images = []

    for i, text in enumerate(texts):
        img = stage_image.copy()

        # Add score text if scores is not None and there is a corresponding score
        if scores is not None and i < len(scores) and scores[i] is not None:
            score_text = f"Score: {scores[i]}"
            score_surface = custom_font_smallest.render(score_text, True, black)
            score_rect = score_surface.get_rect(center=(block_width // 2, block_height // 2 + 40))
            img.blit(score_surface, score_rect)
        else:
            # Use stage_image2 if scores is None or the score for this stage is None
            img.blit(stage_image2, (0, 0))

        
        text_surface = custom_font1_small1.render(text, True, black)
        text_rect = text_surface.get_rect(center=(block_width // 2, block_height // 2))
        img.blit(text_surface, text_rect)

        stage_images.append(img)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i, block in enumerate(blocks):
                    if block.collidepoint(mouse_pos):
                        if i < len(texts):
                            if texts[i] != 'Soon' and scores is not None and scores[i] is not None:
                                print(f'Stage {i+1}')
                                message = f"Stage {i+1}"
                                message_color = green
                            elif texts[i] == 'Soon':
                                print('Coming Soon')
                                message = "Coming Soon"
                                message_color = red
                            else:
                                print("Haven't Unlocked")
                                message = "Haven't Unlocked"
                                message_color = red   
                            
                    if back_button_rect.collidepoint(event.pos):
                        start_menu(profile,id)

        # Clear screen
        screen.fill(white)

        scroll += 1.1   # Increase scroll speed for faster movement
        if scroll > menu_width:
            scroll = 0 
        draw_menu(scroll)

        screen.blit(back_button_image, back_button_rect)

        # Draw blocks (images)
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

        # Update display
        pygame.display.flip()

def stage_select_menu_admin(profile, id):
    scroll = 0
    message = ""

    # Load images and scale them
    stage_image_orig = pygame.image.load('jpg/main_menu_button.png').convert_alpha()
    stage_image_size = (150, 150)
    stage_image = pygame.transform.scale(stage_image_orig, stage_image_size)

    stage_image_orig2 = pygame.image.load('jpg/stage_button2.png').convert_alpha()
    stage_image_size2 = (150, 150)
    stage_image2 = pygame.transform.scale(stage_image_orig2, stage_image_size2)

    # Scale images to block size
    block_width = 150
    block_height = 150

    # Define block positions
    blocks = []
    rows = 3
    cols = 3

    # Calculate padding
    padding_x = (screen.get_width() - (cols * block_width)) // (cols + 1)
    padding_y = (screen.get_height() - (rows * block_height)) // (rows + 5)

    for row in range(rows):
        for col in range(cols):
            x = padding_x + col * (block_width + padding_x)
            y = padding_y + row * (block_height + padding_y) + 120
            blocks.append(pygame.Rect(x, y, block_width, block_height))

    # Prepare texts for each stage
    texts = [f'Stage {i+1}' for i in range(8)] + ['Soon']

    # Admin: Unlock all stages (bypass score check)
    scores = "" * 8  # Placeholder scores to signify all stages are unlocked

    # Render text onto each image
    stage_images = []

    for i, text in enumerate(texts):
        img = stage_image.copy()

        # Add score text if scores is not None and there is a corresponding score
        if scores is not None and i < len(scores) and scores[i] is not None:
            score_text = f"Score: {scores[i]}"
            score_surface = custom_font_smallest.render(score_text, True, black)
            score_rect = score_surface.get_rect(center=(block_width // 2, block_height // 2 + 40))
            img.blit(score_surface, score_rect)
        else:
            # Use stage_image2 if scores is None or the score for this stage is None
            img.blit(stage_image2, (0, 0))

        text_surface = custom_font1_small1.render(text, True, black)
        text_rect = text_surface.get_rect(center=(block_width // 2, block_height // 2))
        img.blit(text_surface, text_rect)

        stage_images.append(img)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i, block in enumerate(blocks):
                    if block.collidepoint(mouse_pos):
                        if i < len(texts):
                            if texts[i] != 'Soon':
                                print(f'Stage {i+1}')
                                message = f"Stage {i+1}"
                                message_color = green
                            elif texts[i] == 'Soon':
                                print('Coming Soon')
                                message = "Coming Soon"
                                message_color = red
                            else:
                                print("Haven't Unlocked")
                                message = "Haven't Unlocked"
                                message_color = red

                    if back_button_rect.collidepoint(event.pos):
                        start_menu_admin(profile, id)

        # Clear screen
        screen.fill(white)

        scroll += 1.1  # Increase scroll speed for faster movement
        if scroll > menu_width:
            scroll = 0
        draw_menu(scroll)

        screen.blit(back_button_image, back_button_rect)

        # Draw blocks (images)
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

        # Update display
        pygame.display.flip()


def about_us(profile,id):
    # Text
    about_us_text = [
        "Counting-Strikes is a captivating 2D game that combines",
        "the excitement of gameplay with the challenge of math.",
        "Developed by a passionate team, KHOO ZHONG HAO, ",
        "YAP BOON SIONG, KEE WEN FEI, CHEN JUN VOON, IVAN.", #change your name
        "Counting-Strikes offers players an engaging way to improve ",
        "their math skills while enjoying a fun and interactive game.",
        "Join us in making math both entertaining and educational!"
    ]
    scroll = 0

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if back_button_rect.collidepoint(event.pos):
                    start_menu(profile,id)

        screen.fill(white)

        scroll += 1   # Increase scroll speed for faster movement
        if scroll > menu_width:
            scroll = 0 
        draw_menu(scroll)
        
        # Render heading
        heading_text_surface = about_us_heading_font.render("About Us", True, black)
        heading_text_rect = heading_text_surface.get_rect(center=(screen_width // 2, 150))
        screen.blit(heading_text_surface, heading_text_rect)
        
        # Render text
        y_offset = 250  # Start rendering text below the heading
        for line in about_us_text:
            text_surface = about_us_font.render(line, True, black)
            text_rect = text_surface.get_rect(topleft=(550, y_offset)) #50
            screen.blit(text_surface, text_rect)
            y_offset += 50  # Adjust line spacing

        screen.blit(back_button_image, back_button_rect)

        mouse_pos = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()

def start_menu(profile,id):
    
    # Define fonts
    #font_medium = pygame.font.Font(custom_font1_big, 52)
    font_small = pygame.font.Font('font/Minecraft.ttf', 18)

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    scroll = 0
    running = True

    message = ''

    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if buttons are clicked
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
                        # Add code to show about us information
                    elif logout_button_rect.collidepoint(mouse_pos) or (screen_width - 220 < mouse_pos[0] < screen_width - 220 + quit_button_size[0] and screen_height - 60 < mouse_pos[1] < screen_height - 60 + quit_button_size[1]):
                        print("Log Out button clicked")
                        message = "Logging out...."
                        message_color = green
                        if message:
                            message_display(message, 24, screen_width // 2, 900, message_color)
                            pygame.display.flip
                            time.sleep(1)
                        logo_menu() # Exit the menu and return to caller (log out)
                    
        scroll += 1   # Increase scroll speed for faster movement
        if scroll > menu_width:
            scroll = 0 

        draw_menu(scroll)  

        # Draw buttons
        start_button_rect = input_image3.get_rect(center=(screen_width // 2, 270))
        profile_button_rect = input_image3.get_rect(center=(screen_width // 2, 390))
        about_button_rect = input_image3.get_rect(center=(screen_width // 2, 510))
        savequit_button_rect = input_image3.get_rect(center=(screen_width // 2, 630))
        logout_button_rect = pygame.Rect(screen_width - 200, screen_height - 50, 150, 30)
        
        # Blit input images for buttons
        screen.blit(input_image3, start_button_rect.topleft)
        screen.blit(input_image3, profile_button_rect.topleft)
        screen.blit(input_image3, about_button_rect.topleft)
        screen.blit(input_image3, savequit_button_rect.topleft)
        screen.blit(quit_button_image, (screen_width - 220, screen_height - 60))

        # Draw text on buttons
        draw_text("Start", custom_font1_big, black, start_button_rect.centerx, start_button_rect.centery)
        draw_text("Profile", custom_font1_big, black, profile_button_rect.centerx, profile_button_rect.centery)
        draw_text("About Us", custom_font1_big, black, about_button_rect.centerx, about_button_rect.centery)
        draw_text("Save & Quit", custom_font1_big, black, savequit_button_rect.centerx, savequit_button_rect.centery)
        draw_text("Log Out", font_small, black, logout_button_rect.centerx, logout_button_rect.centery)
        
        # Draw profile text with left alignment
        profile_text_x = 20  # Left margin value
        profile_text_y = screen_height - 60  # Bottom-left corner y-coordinate with a slight margin
        screen.blit(input_image2, (profile_text_x, profile_text_y))
        draw_text(f"Logged in as: {profile}", font_small, black, profile_text_x + 30, profile_text_y + 20, align="left")
        
        # Display login message if any
        if message:
            message_display(message, 24, screen_width // 2, 750, message_color)
            
        # Check if mouse is over buttons to change cursor
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos) or profile_button_rect.collidepoint(mouse_pos) or about_button_rect.collidepoint(mouse_pos) or logout_button_rect.collidepoint(mouse_pos) or savequit_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Set custom cursor image
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Set default system arrow cursor            
        
        pygame.display.flip()


def start_menu_admin(profile,id):
    
    # Define fonts
    #font_medium = pygame.font.Font(custom_font1_big, 52)
    font_small = pygame.font.Font('font/Minecraft.ttf', 18)

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    scroll = 0
    running = True

    message = ''

    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if buttons are clicked
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
                        # Add code to show about us information
                    elif logout_button_rect.collidepoint(mouse_pos) or (screen_width - 220 < mouse_pos[0] < screen_width - 220 + quit_button_size[0] and screen_height - 60 < mouse_pos[1] < screen_height - 60 + quit_button_size[1]):
                        print("Log Out button clicked")
                        message = "Logging out...."
                        message_color = green
                        if message:
                            message_display(message, 24, screen_width // 2, 900, message_color)
                            pygame.display.flip
                            time.sleep(1)
                        logo_menu() # Exit the menu and return to caller (log out)
                    
        scroll += 1   # Increase scroll speed for faster movement
        if scroll > menu_width:
            scroll = 0 

        draw_menu(scroll)  

        # Draw buttons
        start_button_rect = input_image3.get_rect(center=(screen_width // 2, 270))
        profile_button_rect = input_image3.get_rect(center=(screen_width // 2, 390))
        savequit_button_rect = input_image3.get_rect(center=(screen_width // 2, 510))
        logout_button_rect = pygame.Rect(screen_width - 200, screen_height - 50, 150, 30)
        
        # Blit input images for buttons
        screen.blit(input_image3, start_button_rect.topleft)
        screen.blit(input_image3, profile_button_rect.topleft)
        screen.blit(input_image3, savequit_button_rect.topleft)
        screen.blit(quit_button_image, (screen_width - 220, screen_height - 60))

        # Draw text on buttons
        draw_text("Stage", custom_font1_big, black, start_button_rect.centerx, start_button_rect.centery)
        draw_text("Profile", custom_font1_big, black, profile_button_rect.centerx, profile_button_rect.centery)
        draw_text("Save & Quit", custom_font1_big, black, savequit_button_rect.centerx, savequit_button_rect.centery)
        draw_text("Log Out", font_small, black, logout_button_rect.centerx, logout_button_rect.centery)
        
        # Draw profile text with left alignment
        profile_text_x = 20  # Left margin value
        profile_text_y = screen_height - 60  # Bottom-left corner y-coordinate with a slight margin
        screen.blit(input_image2, (profile_text_x, profile_text_y))
        draw_text(f"Admin as: {profile}", font_small, black, profile_text_x + 30, profile_text_y + 20, align="left")
        
        # Display login message if any
        if message:
            message_display(message, 24, screen_width // 2, 750, message_color)
            
        # Check if mouse is over buttons to change cursor
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos) or profile_button_rect.collidepoint(mouse_pos) or logout_button_rect.collidepoint(mouse_pos) or savequit_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Set custom cursor image
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Set default system arrow cursor            
        
        pygame.display.flip()



def check_forget_email(email):
    query = "SELECT nickname, password FROM user WHERE email = %s"
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
        
        scroll += 10   # Increase scroll speed for faster movement
        if scroll > menu_width:
            scroll = 0 
        
        screen.fill(white)
        # Draw menu background with parallax effect
        draw_menu(scroll)

# Main menu2 loop
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
                mouse_pos = pygame.mouse.get_pos()
                # Check if quit button clicked
                
                if quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

                # Check if login button clicked
                player_button_rect = login_button_image.get_rect(center=(screen_width // 2, 225))
                
                if player_button_rect.collidepoint(mouse_pos):
                    user = "player"
                    return user
                
                # Inside the main_menu function where registration button is handled
                admin_button_rect = register_button_image.get_rect(center=(screen_width // 2, 525))
                
                if admin_button_rect.collidepoint(mouse_pos):
                    user = "admin"
                    return user

        scroll += 1.7   # Increase scroll speed for faster movement
        if scroll > menu_width:
            scroll = 0 
               
        screen.fill(white)
        # Draw menu background with parallax effect
        draw_menu(scroll)

        # Display buttons with images
        player_button_rect = login_button_image.get_rect(center=(screen_width // 2, 225))
        admin_button_rect = register_button_image.get_rect(center=(screen_width // 2, 525))
        screen.blit(login_button_image, player_button_rect)
        screen.blit(register_button_image, admin_button_rect)

        # Add text on top of the button images
        text_surf, text_rect = text_objects("Player", custom_font1_big, black)
        text_rect.center = player_button_rect.center
        screen.blit(text_surf, text_rect)
        
        text_surf, text_rect = text_objects("Admin", custom_font1_big, black)
        text_rect.center = admin_button_rect.center
        screen.blit(text_surf, text_rect)

        # Display quit button and its text
        quit_button_rect = quit_button_image.get_rect(topleft=(40, 40))
        screen.blit(quit_button_image, quit_button_rect)
        text_surf, text_rect = text_objects("Quit", custom_font1_small, black)
        text_rect.center = quit_button_rect.center
        screen.blit(text_surf, text_rect)
        
        pygame.display.flip()
        
        
# Main menu loop
def main_menu():
    global screen
    
    running = True
    login_mode = False  # Flag to indicate if the login mode is active
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
                mouse_pos = pygame.mouse.get_pos()
                # Check if quit button clicked
                
                if quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

                # Check if login button clicked
                login_button_rect = login_button_image.get_rect(center=(screen_width // 2, 225))
                
                if login_button_rect.collidepoint(mouse_pos):
                    main_menu2()
                    if user == "player":
                        # Show login input boxes
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
                                query = "SELECT id FROM user WHERE email = %s"
                                my_cursor.execute(query, (profile,))
                                result = my_cursor.fetchone()
                                if result:
                                    id = result[0]  # Extracting the first element from the tuple
                                    print(f"Profile ID: {id}")
                                else:
                                    print("No profile found for the given email.")
                                if login_message:
                                    message_display(login_message, 24, screen_width // 2, 750, login_message_color)
                                    pygame.display.flip
                                    time.sleep(0.5)
                                    start_menu(profile,id)
                                    
                            else:
                                login_message = "Login Failed!"
                                login_message_color = red
                        else:
                            login_message = "Please fill in all fields."
                            login_message_color = red
                    
                    elif user == "admin": 
                        # Show login input boxes
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
                                    id = result[0]  # Extracting the first element from the tuple
                                    print(f"Profile ID: {id}")
                                else:
                                    print("No profile found for the given email.")
                                if login_message:
                                    message_display(login_message, 24, screen_width // 2, 750, login_message_color)
                                    pygame.display.flip
                                    time.sleep(0.5)
                                    start_menu_admin(profile,id)
                                    
                            else:
                                login_message = "Login Failed!"
                                login_message_color = red
                        else:
                            login_message = "Please fill in all fields."
                            login_message_color = red


                        
                # Inside the main_menu function where registration button is handled
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
                        
                        # Check if all fields are filled
                        if all(responses.values()):
                            # Validate user input
                            valid, message = validate_user_input(responses["New Username"], responses["Age"], responses["Email"], responses["Password"])
                            
                            if valid:
                                name_otp = responses["New Username"]
                                receiver_email = responses["Email"]
                                otp_code(name_otp, receiver_email)
                                # Proceed with registration in MySQL database
                                if register_user(responses["New Username"], responses["Age"], responses["Email"], responses["Password"]):
                                    
                                    login_message = "Registration Successful! Login your account to play."
                                    login_message_color = green
                                    query = "SELECT id FROM user WHERE email = %s"
                                    my_cursor.execute(query, (receiver_email,))
                                    result = my_cursor.fetchone()
                                    id_2 = result[0]
                                    query_2 = f"INSERT INTO `stage`(`id`, `stage1`) VALUES ('{id_2}', 0)"
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
                        
                        # Check if all fields are filled
                        if all(responses.values()):
                            # Validate user input
                            valid, message = validate_admin_input(responses["New Username"], responses["Age"], responses["Email"], responses["Password"], responses["Admin Code"])
                            
                            if valid:
                                name_otp = responses["New Username"]
                                receiver_email = responses["Email"]
                                otp_code(name_otp, receiver_email)
                                # Proceed with registration in MySQL database
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


        scroll += 10   # Increase scroll speed for faster movement
        if scroll > menu_width:
            scroll = 0 
               
        screen.fill(white)
        # Draw menu background with parallax effect
        draw_menu(scroll)

        # Display buttons with images
        login_button_rect = login_button_image.get_rect(center=(screen_width // 2, 225))
        register_button_rect = register_button_image.get_rect(center=(screen_width // 2, 525))
        screen.blit(login_button_image, login_button_rect)
        screen.blit(register_button_image, register_button_rect)

        # Add text on top of the button images
        text_surf, text_rect = text_objects("Login", custom_font1_big, black)
        text_rect.center = login_button_rect.center
        screen.blit(text_surf, text_rect)
        
        text_surf, text_rect = text_objects("Register", custom_font1_small, black)
        text_rect.center = register_button_rect.center
        screen.blit(text_surf, text_rect)

        # Display quit button and its text
        quit_button_rect = quit_button_image.get_rect(topleft=(40, 40))
        screen.blit(quit_button_image, quit_button_rect)
        text_surf, text_rect = text_objects("Quit", custom_font1_small, black)
        text_rect.center = quit_button_rect.center
        screen.blit(text_surf, text_rect)
        
        # Display login message if any
        if login_message:
            message_display(login_message, 24, screen_width // 2, 750, login_message_color)

        # Check if mouse is over buttons to change cursor
        mouse_pos = pygame.mouse.get_pos()
        if login_button_rect.collidepoint(mouse_pos) or register_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Set custom cursor image
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Set default system arrow cursor
        
        pygame.display.flip()

# Function to draw the logo menu
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
                main_menu()  # Switch to main menu after click
        
        # Update logo position for floating effect
        logo_y += logo_speed
        
        # Adjust logo_speed direction when logo_y reaches top or bottom boundary
        if logo_y <= 100:
            logo_speed = 1  # Move down
        elif logo_y + logo_image.get_height() + 300 >= screen_height:
            logo_speed = -1  # Move up
        
        # Adjust scroll speed
        scroll += 10
        if scroll > menu_width:
            scroll = 0

        # Draw menu background with parallax effect
        draw_menu(scroll)  # Draw menu without scroll in logo menu
        
        # Draw logo
        screen.blit(logo_image, ((screen_width - logo_image.get_width()) // 2, logo_y))

        # Render text using the function
        render_text('font/Minecraft.ttf', "Click Here !", 20, screen_width // 2, screen_height - 50, pygame.Color('white'))
        
        pygame.display.flip()

def profile_management(profile,id):

    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500  # Adjust blinking interval as needed
    scroll = 0
    
    # Define fonts
    font_small = pygame.font.Font('font/Minecraft.ttf', 18)

    # Fetch user data from the database
    query = "SELECT id, nickname, age, password FROM user WHERE email = %s"
    my_cursor.execute(query, (profile,))
    user_data = my_cursor.fetchone()
    if user_data:
        user_id, nickname, age, password = user_data
    else:
        user_id = nickname = age = password = ''

    # Input boxes and initial values
    input_boxes = {
        "id": str(user_id),
        "nickname": nickname,
        "age": str(age),
        "password": password
    }

    # Adjust input box positions and sizes based on image dimensions
    input_rects = {
        "id": button_image.get_rect(topleft=(screen_width//3, 170)), #150
        "nickname": button_image.get_rect(topleft=(screen_width//3, 300)), #150
        "age": button_image.get_rect(topleft=(screen_width//3, 430)), #150
        "password": button_image.get_rect(topleft=(screen_width//3, 560)) #150
    }

    # Define margins for each input box
    margins = {
        "id": 100,
        "nickname": 250,
        "age": 120,
        "password": 240
    }

    active_box = None
    
    # Assuming quit_button_image has a specific size (replace with actual dimensions if known)
    button_width = quit_button_image.get_width()
    button_height = quit_button_image.get_height()

    # Create save_button_rect with the same dimensions as quit_button_image
    save_button_rect = pygame.Rect(screen_width - 220, screen_height - 60, button_width, button_height)
    logged_in_rect = pygame.Rect(20, screen_height - 60, 200, 50)  # Bottom left for "Logged in as" text

    running = True
    message = ''
    cursor_length = 35
    label_spacing = -30
    while running:
        cursor_over_input = False  # Flag to check if the cursor is over an input box or button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if save_button_rect.collidepoint(mouse_pos):
                    # Save the updated user data to the database
                    new_data = (
                        input_boxes["nickname"],
                        int(input_boxes["age"]),
                        input_boxes["password"],
                        profile
                    )
                    query = "UPDATE user SET nickname = %s, age = %s, password = %s WHERE email = %s"
                    my_cursor.execute(query, new_data)
                    conn.commit()
                    message = "Profile Updated Successfully!"
                    # Display login message if any
                    if message:
                        message_display(message, 24, screen_width // 2, 700, green)
                        pygame.display.flip
                    time.sleep(1)
                    start_menu(profile,id)
                elif back_button_rect.collidepoint(mouse_pos):
                    start_menu(profile,id)
                for key, rect in input_rects.items():
                    if key != "id" and rect.collidepoint(mouse_pos):  # ID box is not editable
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
        if scroll > screen_width:  # Adjust as needed
            scroll = 0
        # Draw menu background with parallax effect
        draw_menu(scroll) 

        # Inside the rendering loop:
        for key, rect in input_rects.items():
            # Draw label text
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
            # Draw input box image
            screen.blit(button_image, rect)

            label_surface = custom_font1.render(label_text, True, black)
            label_rect = label_surface.get_rect(midleft=(rect.x - label_spacing, rect.centery))
            screen.blit(label_surface, label_rect)

            # Get margin for current key, default to 50 if not specified
            margin_left = margins.get(key, 50)

            # Draw text inside input box, aligned left with a specified margin
            text_surface = custom_font1.render(input_boxes[key], True, black)
            text_rect = text_surface.get_rect(left=rect.x + margin_left, centery=rect.centery)
            screen.blit(text_surface, text_rect)

            if active_box == key and blink:
                cursor_x = text_rect.right + 2  # Position cursor to the right of text
                cursor_center = text_rect.centery
                cursor_top = cursor_center - cursor_length // 2
                cursor_bottom = cursor_center + cursor_length // 2
                pygame.draw.line(screen, black, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

            # Check if cursor is over an input box
            if rect.collidepoint(pygame.mouse.get_pos()):
                cursor_over_input = True
        
        # Check if cursor is over back button or save button
        if back_button_rect.collidepoint(pygame.mouse.get_pos()) or save_button_rect.collidepoint(pygame.mouse.get_pos()):
            cursor_over_input = True

        # Set cursor to hand if over input box or button, else set to arrow
        if cursor_over_input:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Draw "Logged in as" text and image at the bottom left
        screen.blit(input_image2, (logged_in_rect.x, logged_in_rect.y))
        draw_text(f"Logged in as: {profile}", font_small, black, logged_in_rect.x + 30, logged_in_rect.y + 20, align="left")

        # Draw buttons
        screen.blit(quit_button_image, save_button_rect)  # Use the logout button image for the save button
        screen.blit(back_button_image, back_button_rect)
        draw_text("Save", font_small, black, save_button_rect.centerx, save_button_rect.centery)

        # Draw profile label
        draw_text("Profile Management", custom_font1_big, black, screen_width // 2, 85)

        # Calculate blinking cursor visibility
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time

        pygame.display.flip()

def profile_management_admin(profile,id):

    blink = True
    blink_timer = pygame.time.get_ticks()
    blink_interval = 500  # Adjust blinking interval as needed
    scroll = 0
    
    # Define fonts
    font_small = pygame.font.Font('font/Minecraft.ttf', 18)

    # Fetch user data from the database
    query = "SELECT id, nickname, age, password FROM admin WHERE email = %s"
    my_cursor.execute(query, (profile,))
    user_data = my_cursor.fetchone()
    if user_data:
        user_id, nickname, age, password = user_data
    else:
        user_id = nickname = age = password = ''

    # Input boxes and initial values
    input_boxes = {
        "id": str(user_id),
        "nickname": nickname,
        "age": str(age),
        "password": password
    }

    # Adjust input box positions and sizes based on image dimensions
    input_rects = {
        "id": button_image.get_rect(topleft=(screen_width//3, 170)), #150
        "nickname": button_image.get_rect(topleft=(screen_width//3, 300)), #150
        "age": button_image.get_rect(topleft=(screen_width//3, 430)), #150
        "password": button_image.get_rect(topleft=(screen_width//3, 560)) #150
    }

    # Define margins for each input box
    margins = {
        "id": 100,
        "nickname": 250,
        "age": 120,
        "password": 240
    }

    active_box = None
    
    # Assuming quit_button_image has a specific size (replace with actual dimensions if known)
    button_width = quit_button_image.get_width()
    button_height = quit_button_image.get_height()

    # Create save_button_rect with the same dimensions as quit_button_image
    save_button_rect = pygame.Rect(screen_width - 220, screen_height - 60, button_width, button_height)
    logged_in_rect = pygame.Rect(20, screen_height - 60, 200, 50)  # Bottom left for "Logged in as" text

    running = True
    message = ''
    cursor_length = 35
    label_spacing = -30
    while running:
        cursor_over_input = False  # Flag to check if the cursor is over an input box or button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if save_button_rect.collidepoint(mouse_pos):
                    # Save the updated user data to the database
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
                    # Display login message if any
                    if message:
                        message_display(message, 24, screen_width // 2, 700, green)
                        pygame.display.flip
                    time.sleep(1)
                    start_menu_admin(profile,id)
                elif back_button_rect.collidepoint(mouse_pos):
                    start_menu_admin(profile,id)
                for key, rect in input_rects.items():
                    if key != "id" and rect.collidepoint(mouse_pos):  # ID box is not editable
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
        if scroll > screen_width:  # Adjust as needed
            scroll = 0
        # Draw menu background with parallax effect
        draw_menu(scroll) 

        # Inside the rendering loop:
        for key, rect in input_rects.items():
            # Draw label text
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
            # Draw input box image
            screen.blit(button_image, rect)

            label_surface = custom_font1.render(label_text, True, black)
            label_rect = label_surface.get_rect(midleft=(rect.x - label_spacing, rect.centery))
            screen.blit(label_surface, label_rect)

            # Get margin for current key, default to 50 if not specified
            margin_left = margins.get(key, 50)

            # Draw text inside input box, aligned left with a specified margin
            text_surface = custom_font1.render(input_boxes[key], True, black)
            text_rect = text_surface.get_rect(left=rect.x + margin_left, centery=rect.centery)
            screen.blit(text_surface, text_rect)

            if active_box == key and blink:
                cursor_x = text_rect.right + 2  # Position cursor to the right of text
                cursor_center = text_rect.centery
                cursor_top = cursor_center - cursor_length // 2
                cursor_bottom = cursor_center + cursor_length // 2
                pygame.draw.line(screen, black, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)

            # Check if cursor is over an input box
            if rect.collidepoint(pygame.mouse.get_pos()):
                cursor_over_input = True
        
        # Check if cursor is over back button or save button
        if back_button_rect.collidepoint(pygame.mouse.get_pos()) or save_button_rect.collidepoint(pygame.mouse.get_pos()):
            cursor_over_input = True

        # Set cursor to hand if over input box or button, else set to arrow
        if cursor_over_input:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Draw "Logged in as" text and image at the bottom left
        screen.blit(input_image2, (logged_in_rect.x, logged_in_rect.y))
        draw_text(f"Admin as: {profile}", font_small, black, logged_in_rect.x + 30, logged_in_rect.y + 20, align="left")

        # Draw buttons
        screen.blit(quit_button_image, save_button_rect)  # Use the logout button image for the save button
        screen.blit(back_button_image, back_button_rect)
        draw_text("Save", font_small, black, save_button_rect.centerx, save_button_rect.centery)

        # Draw profile label
        draw_text("Admin Profile Management", custom_font1_big, black, screen_width // 2, 85)

        # Calculate blinking cursor visibility
        current_time = pygame.time.get_ticks()
        if current_time - blink_timer > blink_interval:
            blink = not blink
            blink_timer = current_time

        pygame.display.flip()

# Start the logo menu loop
logo_image = pygame.image.load('jpg/logo2.png').convert_alpha()
logo_menu()

# Close cursor and connection
my_cursor.close()
conn.close()
print("Connection closed")

# Quit pygame
pygame.quit()
