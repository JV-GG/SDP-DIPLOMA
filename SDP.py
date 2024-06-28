import pygame
import pymysql
import time

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Counting-Strike')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
green = (0, 255, 0)
red = (255, 0, 0)

# Fonts
font_large = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Database connection
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sdp'
)
my_cursor = conn.cursor()

# Function to check login credentials
def check_login(username, password):
    query = "SELECT * FROM USER WHERE nickname=%s AND password=%s"
    my_cursor.execute(query, (username, password))
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
def multi_text_input(inputs):
    input_boxes = {prompt: pygame.Rect(x, y, width, height) for prompt, (x, y, width, height, font_size) in inputs.items()}
    colors = {prompt: pygame.Color('lightskyblue3') for prompt in inputs}
    active_box = None
    texts = {prompt: '' for prompt in inputs}
    done = False
    while not done:
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
            if event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        texts[active_box] = texts[active_box][:-1]
                    else:
                        texts[active_box] += event.unicode

        screen.fill(white)
        for prompt, box in input_boxes.items():
            pygame.draw.rect(screen, colors[prompt], box, 2)
            font = pygame.font.Font(None, inputs[prompt][4])
            text_surf = font.render(prompt + ": " + texts[prompt], True, (0, 0, 0))
            screen.blit(text_surf, (box.x + 5, box.y + 5))

        pygame.display.flip()
    return texts

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

# Main menu loop
def main_menu():
    running = True
    login_mode = False  # Flag to indicate if the login mode is active
    username = ''
    password = ''
    login_message = ''
    
    while running:
        screen.fill(white)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if login button clicked
                login_button = pygame.Rect(screen_width // 2 - 100, 200, 200, 50)
                if login_button.collidepoint(mouse_pos):
                    # Show login input boxes
                    inputs = {
                        "Username": (250, 200, 300, 30, 32),
                        "Password": (250, 250, 300, 30, 32)
                    }
                    responses = multi_text_input(inputs)
                    username = responses["Username"]
                    password = responses["Password"]
                    if username and password:
                        if check_login(username, password):
                            login_message = "Login Successful!"
                            login_message_color = green
                            # Implement what happens after successful login
                        else:
                            login_message = "Login Failed!"
                            login_message_color = red
                        
                # Inside the main_menu function where registration button is handled
                if register_button.collidepoint(mouse_pos):
                    register_inputs = {
                        "New Username": (150, 200, 500, 30, 32),
                        "Age": (150, 250, 100, 30, 32),
                        "Email": (150, 300, 500, 30, 32),
                        "New Password": (150, 350, 500, 30, 32)
                    }
                    responses = multi_text_input(register_inputs)
                    
                    # Check if all fields are filled
                    if all(responses.values()):
                        # Validate user input
                        valid, message = validate_user_input(responses["New Username"], responses["Age"], responses["Email"], responses["New Password"])
                        
                        if valid:
                            # Proceed with registration in MySQL database
                            if register_user(responses["New Username"], responses["Age"], responses["Email"], responses["New Password"]):
                                login_message = "Registration Successful!"
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

        # Create buttons
        login_button = pygame.Rect(screen_width // 2 - 100, 200, 200, 50)
        pygame.draw.rect(screen, gray, login_button)
        text_surf, text_rect = text_objects("Login", font_small, black)
        text_rect.center = (screen_width // 2, 225)
        screen.blit(text_surf, text_rect)
        
        register_button = pygame.Rect(screen_width // 2 - 100, 300, 200, 50)
        pygame.draw.rect(screen, gray, register_button)
        text_surf, text_rect = text_objects("Register", font_small, black)
        text_rect.center = (screen_width // 2, 325)
        screen.blit(text_surf, text_rect)
        
        # Display login message if any
        if login_message:
            message_display(login_message, 24, screen_width // 2, 500, login_message_color)
        
        pygame.display.flip()

# Start the main menu loop
main_menu()

# Close cursor and connection
my_cursor.close()
conn.close()
print("Connection closed")

# Quit pygame
pygame.quit()