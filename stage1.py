import pygame
import random
import os
import pymysql


FPS = 60
WIDTH = 1920
HEIGHT = 1080

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def start_game(stage_names, id):  # Accept user_id as an argument
    # Database connection
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='sdp'
    )
    my_cursor = conn.cursor()

    # Initialize the game and create window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Counting Strike")
    clock = pygame.time.Clock()

    # Load images
    background_img = pygame.image.load(os.path.join("img", "background.jpeg")).convert()
    player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
    player_mini_img = pygame.transform.scale(player_img, (25, 19))
    player_mini_img.set_colorkey(BLACK)
    pygame.display.set_icon(player_mini_img)
    bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
    rock_imgs = [pygame.image.load(os.path.join("img", f"rock{i}.png")).convert() for i in range(7)]
    expl_anim = {'lg': [], 'sm': [], 'player': []}
    for i in range(9):
        expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
        expl_img.set_colorkey(BLACK)
        expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
        expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
        player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
        player_expl_img.set_colorkey(BLACK)
        expl_anim['player'].append(player_expl_img)
    power_imgs = {
        'shield': pygame.image.load(os.path.join("img", "shield.png")).convert(),
        'gun': pygame.image.load(os.path.join("img", "gun.png")).convert()
    }
    rock_images = {
        'tiny': pygame.image.load(os.path.join("img", "rock0.png")),
        'small': [pygame.image.load(os.path.join("img", "rock1.png")), pygame.image.load(os.path.join("img", "rock2.png"))],
        'medium': [pygame.image.load(os.path.join("img", "rock3.png")), pygame.image.load(os.path.join("img", "rock4.png"))],
        'large': [pygame.image.load(os.path.join("img", "rock5.png")), pygame.image.load(os.path.join("img", "rock6.png"))]
    }

    # Load sounds
    shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
    gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
    shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
    die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
    expl_sounds = [pygame.mixer.Sound(os.path.join("sound", "expl0.wav")), pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))]
    pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
    pygame.mixer.music.set_volume(0.4)

    font_name = os.path.join("font/Minecraft.ttf")

    def draw_text(surf, text, size, x, y, color=BLACK):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

    def new_rock():
        size_category = random.choice(['tiny', 'small', 'medium', 'large'])  # Randomly choose the size
        r = Rock(size_category)  # Pass size_category to Rock
        all_sprites.add(r)
        rocks.add(r)


    def draw_health(surf, hp, x, y):
        if hp < 0:
            hp = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (hp / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, GREEN, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_lives(surf, lives, img, x, y):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 32 * i
            img_rect.y = y
            surf.blit(img, img_rect)

    def draw_init():
        screen.blit(background_img, (0, 0))
        draw_text(screen, stage_names, 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, '← →to move and spacebar to shoot~', 22, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, 'Start the game by pressing any key', 18, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    return False

    def ask_question():
        query = f"""
            SELECT q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, 
                a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 
            FROM `stage` 
            WHERE `stage_name` = %s
            ORDER BY RAND() 
            LIMIT 1
        """        
        my_cursor.execute(query,({stage_names}))

        result = my_cursor.fetchone()

        if result:
            questions = result[:10]
            answers = result[10:]
            question = random.choice(questions)
            answer = answers[questions.index(question)]
            
        else:
            return False, False
        
        draw_text(screen, question, 24, WIDTH / 2, HEIGHT / 2 - 50)
        
        input_box = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 32)  # Define the text box area
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        user_answer = ""
        
        pygame.display.update()
        
        waiting_for_answer = True
        while waiting_for_answer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False, ""
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicks on the input_box, activate it.
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            waiting_for_answer = False
                        elif event.key == pygame.K_BACKSPACE:
                            user_answer = user_answer[:-1]
                        else:
                            user_answer += event.unicode
            
            screen.blit(background_img, (0, 0))
            draw_text(screen, question, 24, WIDTH / 2, HEIGHT / 2 - 50)

            # Render the current text.
            txt_surface = pygame.font.Font(None, 24).render(user_answer, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            
            pygame.display.update()

        if not user_answer.lower().strip() == answer.lower().strip():
            draw_text(screen, "Wrong!, The Correct Answer is " + answer, 24, WIDTH / 2, HEIGHT / 2 + 50, RED)
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds to display the error message

        return True, user_answer.lower().strip() == answer.lower().strip()

    def draw_score_page(score):
        screen.blit(background_img, (0, 0))
        draw_text(screen, f'Score: {score}', 48, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, 'Game Over', 64, WIDTH / 2, HEIGHT / 3)
        draw_text(screen, 'Press R to Restart or Q back to home page', 22, WIDTH / 2, HEIGHT / 2)
        pygame.display.update()

        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'quit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return 'restart'
                    elif event.key == pygame.K_q:
                        return 'quit'

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(player_img, (150, 88))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = 30
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speedx = 8
            self.health = 100
            self.lives = 3
            self.hidden = False
            self.hide_time = 0
            self.gun = 1
            self.gun_time = 0

        def update(self):
            now = pygame.time.get_ticks()
            if self.gun > 1 and now - self.gun_time > 5000:
                self.gun -= 1
                self.gun_time = now

            if self.hidden and now - self.hide_time > 1000:
                self.hidden = False
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10

            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RIGHT]:
                self.rect.x += self.speedx
            if key_pressed[pygame.K_LEFT]:
                self.rect.x -= self.speedx

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        def shoot(self):
            if not self.hidden:
                if self.gun == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
                elif self.gun >= 2:
                    bullet1 = Bullet(self.rect.left, self.rect.centery)
                    bullet2 = Bullet(self.rect.right, self.rect.centery)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    shoot_sound.play()

        def hide(self):
            self.hidden = True
            self.hide_time = pygame.time.get_ticks()
            self.rect.center = (WIDTH / 2, HEIGHT + 500)

        def gunup(self):
            self.gun += 1
            self.gun_time = pygame.time.get_ticks()

    class Rock(pygame.sprite.Sprite):
        def __init__(self, size_category):
            super().__init__()
            self.size_category = size_category

            if size_category == 'tiny':
                self.image = rock_images['tiny']
                self.hit_points = 1
                self.speedy = random.randint(7, 9)
            elif size_category == 'small':
                self.image = random.choice(rock_images['small'])
                self.hit_points = 2
                self.speedy = random.randint(5, 7)
            elif size_category == 'medium':
                self.image = random.choice(rock_images['medium'])
                self.hit_points = 3
                self.speedy = random.randint(3, 5)
            elif size_category == 'large':
                self.image = random.choice(rock_images['large'])
                self.hit_points = 5
                self.speedy = random.randint(1, 3)

            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-150, -100)
            self.speedx = random.randint(-2, 2)

        def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx

            # Destroy the rock if it goes off-screen
            if self.rect.top > HEIGHT:
                self.kill()
                new_rock()  # Replace the rock that went off-screen
            
        def hit(self):
            self.hit_points -= 1
            if self.hit_points <= 0:
                self.kill()
                new_rock()  # Replace the rock that was destroyed


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = bullet_img
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center, size):
            pygame.sprite.Sprite.__init__(self)
            self.size = size
            self.image = expl_anim[self.size][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(expl_anim[self.size]):
                    self.kill()
                else:
                    self.image = expl_anim[self.size][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center

    class Power(pygame.sprite.Sprite):
        def __init__(self, center):
            pygame.sprite.Sprite.__init__(self)
            self.type = random.choice(['shield', 'gun'])
            self.image = power_imgs[self.type]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.speedy = 3

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:
                self.kill()

    pygame.mixer.music.play(-1)

    # Main game loop
    show_init = True
    running = True
    death_expl = None  # Initialize the variable here
    while running:
        if show_init:
            close = draw_init()
            if close:
                break
            show_init = False
            all_sprites = pygame.sprite.Group()
            rocks = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powers = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for i in range(15):
                new_rock()
            score = 0

        clock.tick(FPS)
        # Get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update game
        all_sprites.update()

        # Check for collisions between rocks and bullets
        hits = pygame.sprite.groupcollide(rocks, bullets, False, True)
        for rock, bullets_hit in hits.items():
            for bullet in bullets_hit:
                rock.hit()
                if rock.hit_points <= 0:
                    random.choice(expl_sounds).play()
                    score += int(rock.radius)
                    expl = Explosion(rock.rect.center, 'lg' if rock.size_category == 'large' else 'sm')
                    all_sprites.add(expl)
                    if random.random() > 0.9:
                        pow = Power(rock.rect.center)
                        all_sprites.add(pow)
                        powers.add(pow)

        #Check if the score have reach the limit
        if score >= 9999:
            screen.blit(background_img, (0, 0))
            draw_text(screen, "Congratulations! You've reached 9999 points!", 48, WIDTH / 2, HEIGHT / 4)
            draw_text(screen, "Press C to Continue or Q to Return to Homepage", 22, WIDTH / 2, HEIGHT / 2)
            pygame.display.update()

            waiting = True
            while waiting:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        running = False
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            show_init = True
                            death_expl = None  # Reset death_expl for a new game
                            waiting = False
                        elif event.key == pygame.K_q:
                            return

        hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
        for hit in hits:
            new_rock()
            
            # Initial health reduction when hit by meteorite
            health_loss = 20
            player.health -= health_loss
            
            # Trigger the question
            question_asked, correct_answer = ask_question()
            if question_asked:
                if not correct_answer:
                    # Double the health loss if the answer is wrong
                    player.health -= health_loss * 1.5
                    
                # Check if player health is still above zero
                if player.health <= 0:
                    player.lives -= 1
                    if player.lives > 0:
                        player.health = 100  # Reset health after losing a life
                        player.hide()
                    else:
                        # Player has lost all lives, trigger game over
                        if not death_expl:
                            death_expl = Explosion(player.rect.center, 'player')
                            all_sprites.add(death_expl)
                            die_sound.play()
                            player.hide()
                            # Insert score into the database
                            sql = f"UPDATE `score` SET `{stage_names}` = %s WHERE `id` = %s"
                            values = (score, id)  # Include the id in the values tuple
                            my_cursor.execute(sql, values)
                            conn.commit()
                            print("Score saved to database.")
                            result = draw_score_page(score)
                            if result == 'quit':
                                conn.close()
                                pygame.quit()
                                return
                            elif result == 'restart':
                                show_init = True
                                death_expl = None
                                break
                else:
                    # Ensure health is capped at a minimum of 0
                    player.health = max(player.health, 0)

            # Check if health drops to 0
            if player.health <= 0:
                if not death_expl:  # Prevent the death_expl from being created multiple times
                    death_expl = Explosion(player.rect.center, 'player')
                    all_sprites.add(death_expl)
                    die_sound.play()
                    player.lives -= 1
                    player.health = 100
                    player.hide()
                    if player.lives <= 0:
                        # Insert score into the database
                        sql = f"UPDATE `score` SET `{stage_names}` = %s WHERE `id` = %s"
                        values = (score, id)
                        my_cursor.execute(sql, values)
                        conn.commit()
                        print("Score saved to database.")
                        result = draw_score_page(score)
                        if result == 'quit':
                            conn.close()
                            pygame.quit()
                            return
                        elif result == 'restart':
                            show_init = True
                            death_expl = None
                            break

        hits = pygame.sprite.spritecollide(player, powers, True)
        for hit in hits:
            if hit.type == 'shield':
                player.health += 20
                if player.health > 100:
                    player.health = 100
                shield_sound.play()
            elif hit.type == 'gun':
                player.gunup()
                gun_sound.play()

        if player.lives == 0 and not (death_expl and death_expl.alive()):
            result = draw_score_page(score)

            # Insert score into the database
            sql = f"UPDATE `score` SET `{stage_names}` = %s WHERE `id` = %s"
            values = (score, id)  # Include the id in the values tuple
            
            my_cursor.execute(sql, values)
            conn.commit()
            print("Score saved to database.")
            

            if result == 'quit':
                # Close the connection
                conn.close()
                return
            elif result == 'restart':
                show_init = True
                death_expl = None  # Reset death_expl for a new game

            

        # Draw/display
        screen.fill(BLACK)
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_health(screen, player.health, 5, 15)
        draw_lives(screen, player.lives, player_mini_img, WIDTH - 250, 15)
        pygame.display.update()

    my_cursor.close()
    conn.close()
    pygame.quit()
