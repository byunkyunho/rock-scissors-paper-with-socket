import pygame as pg
import socket
import time

screen = pg.display.set_mode((500, 700))
pg.display.set_caption("가위바위보 온라인(서버)")
pg.init()
pg.key.set_repeat(1,1)

rsp_image = pg.transform.scale(pg.image.load("image/가위바위보.png"), (350, 150))
logo_image = pg.transform.scale(pg.image.load("image/로고.png"), (300, 90))
small_logo_image = pg.transform.scale(pg.image.load("image/로고.png"), (150, 45))
replay_image = pg.transform.scale(pg.image.load("image/다시하기.png"), (55, 80))
s_replay_image = pg.transform.scale(pg.image.load("image/다시하기.png"), (50, 75))
back_image =  pg.transform.scale(pg.image.load("image/back.png"), (50, 73))
s_back_image =  pg.transform.scale(pg.image.load("image/back.png"), (45, 65))

rsp_image_list = [ pg.transform.scale(pg.image.load("image/주먹.png"), (100, 100)),  pg.transform.scale(pg.image.load("image/가위.png"), (100, 100)),pg.transform.scale(pg.image.load("image/보자기.png"), (100, 100))]
b_rsp_image_list = [ pg.transform.scale(pg.image.load("image/주먹.png"), (110, 110)),pg.transform.scale(pg.image.load("image/가위.png"), (110, 110)),  pg.transform.scale(pg.image.load("image/보자기.png"), (110, 110)) ]

image_list = [pg.transform.scale(pg.image.load("image/주먹.png"), (300, 300)), pg.transform.scale(pg.image.load("image/가위.png"), (300, 300)), pg.transform.scale(pg.image.load("image/보자기.png"), (300, 300))]
s_image_list = [pg.transform.scale(pg.image.load("image/주먹.png"), (200, 200)), pg.transform.scale(pg.image.load("image/가위.png"), (200, 200)),  pg.transform.scale(pg.image.load("image/보자기.png"), (200, 200))]
s_image_list2 = [pg.transform.rotate(pg.transform.scale(pg.image.load("image/주먹.png"), (200, 200)), 180), pg.transform.rotate(pg.transform.scale(pg.image.load("image/가위.png"),  (200, 200)), 180),  pg.transform.rotate(pg.transform.scale(pg.image.load("image/보자기.png"), (200, 200)) , 180)]


HOST = '172.30.1.20'
port = 5000

running = True

connect = False

game = True

intro = True

def set_game():
    global start_game_om, connect_error, connect_socket, connect_socket_sleep, connect, mouse_x, mouse_y, my_rsp, left_time, end, replay_om, back_om

    connect = False

    connect_socket_sleep = False

    connect_socket = False

    connect_error = False

    end = True

    mouse_x = 0
    
    mouse_y = 0

    my_rsp = 0

    left_time = 0

    replay_om = False

    back_om = False

def draw_text(text, font_size, x, y):
    screen.blit(pg.font.SysFont("malgungothic", font_size).render(text ,True, (0,0,0)), (x,y))

def check_on(x,y,start_x, start_y, height, width):
    if x > start_x and x < start_x + width and y > start_y and y < start_y + height:
        return True
    else:
        return False 

def d_background():
    screen.fill((195, 203, 245))
    screen.blit(small_logo_image, (175, 635))

def d_intro():
    global start_game_om
    if check_on(mouse_x, mouse_y, 145, 485, 50, 200):
        draw_text("게임시작", 50, 150, 490)
        start_game_om = True
    else:
        draw_text("게임시작", 55, 145, 485)
        start_game_om = False
    screen.blit(logo_image, (100, 85))
    screen.blit(rsp_image, (75, 240))

def d_rsp():
    for xy in enumerate([(60, 485), (200, 485), (340, 485)]):
        if check_on(mouse_x, mouse_y, xy[1][0], xy[1][1], 100, 100):
            screen.blit(b_rsp_image_list[xy[0]],(xy[1][0] - 5, xy[1][1] - 5) )
        else:
            screen.blit(rsp_image_list[xy[0]], (xy[1][0], xy[1][1]))

def d_result():
    global replay_om, back_om
    screen.blit(s_image_list2[your_rsp], (150, 40))
    screen.blit(s_image_list[my_rsp], (150, 370))
    if your_rsp == my_rsp:
        draw_text("무승부!", 60, 150,  265)
    elif your_rsp == 2 and my_rsp == 1 or your_rsp == 1 and my_rsp == 0 or your_rsp == 0 and my_rsp == 2:
        draw_text("승리!", 60, 182,  265)
    elif my_rsp == 2 and your_rsp == 1 or my_rsp == 1 and your_rsp == 0 or my_rsp == 0 and your_rsp == 2:
        draw_text("패배..", 60, 182, 265)
    if check_on(mouse_x, mouse_y, 408, 611, 70,50):
        screen.blit(s_replay_image, (410, 613))
        replay_om = True
    else:
        screen.blit(replay_image, (408, 611))
        replay_om = False
    if check_on(mouse_x, mouse_y, 54, 617, 50, 73):
        screen.blit(s_back_image, (57, 620))
        back_om = True
    else:
        screen.blit(back_image, (54, 614))
        back_om = False

def connect_():
    global connect_socket, connect_socket_sleep, client_socket, server_socket, start_time
    if connect_socket_sleep:
        time.sleep(0.5)
        connect_socket_sleep = False
        start_time = time.time()

    if not connect_socket:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((HOST, port))
            server_socket.listen(1)
            client_socket,b = server_socket.accept()
            connect_socket = True
            connect_socket_sleep = True
        except:
            pass

set_game()

while running:
    while intro and running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and start_game_om:
                intro = False
        mouse_x, mouse_y = pg.mouse.get_pos()
        d_background()
        d_intro()
        pg.display.update()
    if game:
        set_game()

    while game and running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in enumerate([(60, 470), (200, 470), (340, 470)]):
                    if check_on(mouse_x, mouse_y, button[1][0], button[1][1], 100, 100):
                        my_rsp = button[0]

        mouse_x, mouse_y = pg.mouse.get_pos()
        
        d_background()
        d_rsp()

        if connect:
            left_time = int(time.time() - start_time)
            screen.blit(image_list[my_rsp], (100, 130))
            draw_text("{}".format(5 - left_time),90, 230, -6)
        if not connect:
            if  connect_socket:
                draw_text("연결완료", 100, 50, 100)
                connect = True
            else:
                draw_text("연결중", 100, 100, 100)

        pg.display.update()

        connect_()
        if left_time > 5:
            game = False

    your_rsp =  int(client_socket.recv(1024).decode())
    client_socket.sendall("{}".format(my_rsp).encode())

    while end and running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and replay_om:
                end = False
                intro = False
                game = True
            if event.type == pg.MOUSEBUTTONDOWN and back_om:
                end = False
                intro = True
                game = True

        mouse_x, mouse_y = pg.mouse.get_pos()

        d_background()
        d_result()
        
        pg.display.update()

        server_socket.close()
        client_socket.close()
        

