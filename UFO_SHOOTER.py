import pygame
import math
import random
import shelve
#from pygame import mixer


#Initialize the pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

#create a screen
screen=pygame.display.set_mode((600,400))

#background
backgroundImg=pygame.image.load('background.jpg')

#background music
#mixer.music.load()
#mixer.music.play(-1)

#Caption and Icon
pygame.display.set_caption("UFO Shooter")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Fonts
over_font=pygame.font.Font('freesansbold.ttf',64)
info=pygame.font.Font('freesansbold.ttf',20)

#ANJ Logo
AImg=pygame.image.load('a.png')
NImg=pygame.image.load('n.png')
JImg=pygame.image.load('j.png')

def anj():
    screen.blit(AImg,  (520,15))
    screen.blit(NImg,  (547,15))
    screen.blit(JImg,  (570,15))
    

#for intro screen
def intro():
    screen.blit(backgroundImg,  (0,0))
        
    screen.blit(pygame.image.load('ufo_boss.png'), (40,50))
   
    Game_name=over_font.render("UFO Shooter", True, (249,224,117))
    screen.blit(Game_name, (120,50))

    information1=info.render("**Don't let the UFOs or the bombs touch your spaceship.**",True, (255,255,255))
    information2=info.render("*Use the arrow keys to control your spaceship.",True, (255,255,255))
    information3=info.render("*Use spacebar to shoot the UFOs.",True, (255,255,255)) 
    information4=info.render("*Press 'P' to pause, 'Q' to quit and 'R' to restart the game.",True, (255,255,255))
    information5=info.render("[Press ENTER to begin.]",True, (255,255,255))
        
    screen.blit(information1,(30,150))
    screen.blit(information2,(30,180))
    screen.blit(information3,(30,210))
    screen.blit(information4,(30,240))
    screen.blit(information5,(165,350))


    
start=False
while not start:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            play=False
            game=False
            break
            
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                start=True
            elif event.key==pygame.K_q:
                pygame.quit()
                play=False
                game=False
                break
        
    intro()
    anj()
       
    pygame.display.update()


#few constants
speed_en=0
speed_bomb=0
score_value=0
previous_score=0

def get_highscore():
    with open("HI.txt","r") as f:
        return f.read()
    f.close()
        
high_score=int(get_highscore())

    
#play loop
play=True
while play:
    
    
    #background objects
    sat1=pygame.image.load('planet.png')
    sat1y=0

    sat2=pygame.image.load('planet2.png')
    sat2y=-80*3

    jup=pygame.image.load('jupiter.png')
    jupy=-80*2

    nep=pygame.image.load('neptune.png')
    nepy=-80*5

    sta1=pygame.image.load('favourite.png')
    star1y=-80

    sta2=pygame.image.load('favourite2.png')
    star2y=-80*4

    move=0.3


    #player
    playerImg=pygame.image.load('spaceship.png')
    plx=252
    ply=330

    plx_change=0
    ply_change=0

    
    #enemys
    speed_en+=0.3
    
    enemyImg=[pygame.image.load('ufo_1.png'),pygame.image.load('ufo_2.png'),pygame.image.load('ufo_boss.png')]
    enx=[540,10,275]
    eny=[23,10,23]
    enx_change=[0.1+speed_en,0.1+speed_en,0.4+speed_en]
    eny_change=[40,40,40]
    en_hit=[0,0,0]
    
    lives=[5,5,10]
    lifeImg=pygame.image.load('heart.png')
    
    #Bullet
    bulletImg=pygame.image.load('bullet.png')
    bulletx=252
    bullety=330
    bulletx_change=0
    bullety_change=3
    bullet_state="ready" #ready-> can't see the bullet on the screen|| fire-> bullet is moving


    #bomb
    speed_bomb+=0.5
    
    bombImg=[pygame.image.load('dynamite.png'), pygame.image.load('explosive.png'), pygame.image.load('nucleobomb.png')] 
    bombx=[enx[0],enx[1], enx[2]]
    bomby=[eny[0],eny[1], eny[2]]
    bomby_change=[0.5+speed_bomb,0.5+speed_bomb,1.5+speed_bomb]
    fire=[0,0,0]
    bomb_state=["ready","ready", "ready"]


    #score
    font=pygame.font.Font('freesansbold.ttf',28)

    textx=10
    texty=10


    #background objects
    def saturn1(y):
        screen.blit(sat1, (20, y))
    def saturn2(y):
        screen.blit(sat2, (520, y))
    def jupiter(y):
        screen.blit(jup, (205, y))
    def neptune(y):
        screen.blit(nep, (300, y))
    def star1(y):
        screen.blit(sta1, (395, y))
    def star2(y):
        screen.blit(sta2, (105, y))
        

    def player(x, y):
        screen.blit(playerImg, (x, y))

        
    def enemies(a, b, c, d):
        screen.blit(enemyImg[0], (a,b))
        screen.blit(enemyImg[1], (c,d))


    def boss(x,y):
        screen.blit(enemyImg[2], (x, y))


    def life(x,y):
        screen.blit(lifeImg, (x, y))


    def fire_bullet(x,y):
        global bullet_state
        bullet_state="fire"
        screen.blit(bulletImg,(x+16,y+10))


    def fire_bomb(i,x,y):
        screen.blit(bombImg[i], (x+16,y+10))


    def isCollision(x1,y1,x2,y2):
        distance=math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
        if distance<20:
            return True
        else:
            return False
        

    def showScore(x,y):
        score=font.render("Score: " + str(score_value), True, (255,255,255))
        screen.blit(score,(x,y))
 
        
    def game_over_text():
        game_over=over_font.render("GAME OVER",  True, (249,224,117))
        screen.blit(game_over,(115,150))


    def you_won_text():
        you_won=over_font.render("YOU WON", True, (68,214,44))
        screen.blit(you_won, (130,100))
        

    def pause():
        paused=True
        while paused:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    game=False
                    play=False
                    paused=False
                    
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_c:
                        paused=False
                    elif event.key==pygame.K_q:
                        pygame.quit()
                        game=False
                        play=False
                        paused=False
                        
            screen.blit(over_font.render("PAUSED", True, (249,224,117)),(170,150))
            screen.blit(info.render("[Press C to continue]", True,(255,255,255)),(200,350))

            pygame.display.update()
            anj()
            clock.tick(5)

    
    #Game Loop
    game=True
    while game:
        
        #backgroud
        screen.blit(backgroundImg,  (0,0))

        #ANJ
        anj()

        #Main events
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                play=False
                game=False
                pygame.quit()
                break
      
            #player's movement
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    play=False
                    game=False
                    pygame.quit()
                    break
                    
                #for player
                if event.key==pygame.K_DOWN:
                    ply_change+=0.45
                   
                elif event.key==pygame.K_UP:
                    ply_change-=0.45
        
                elif event.key==pygame.K_RIGHT:
                    plx_change+=0.45
                    
                elif event.key==pygame.K_LEFT:
                    plx_change-=0.45

                #to pause
                elif event.key==pygame.K_p:
                    pause()
                
                #for bullet
                if event.key==pygame.K_SPACE:
                    if bullet_state=="ready":
                        
                        #bullet_sound=mixer.sound()
                        #bullet_sound.play
                        
                        bulletx=plx
                        fire_bullet(bulletx,bullety)
                    
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_DOWN or event.key==pygame.K_UP:
                    ply_change=0

                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    plx_change=0
                    
        #background objects movement
        sat1y+=move
        if sat1y>=340+(80*5):
            sat1y=0

        star1y+=move
        if star1y>=340+(80*4):
            star1y=-80

        jupy+=move
        if jupy>=340+(80*3):
            jupy=-80*2

        sat2y+=move
        if sat2y>=340+(80*2):
            sat2y=-80*3

        star2y+=move
        if star2y>=340+80:
            star2y=-80*4

        nepy+=move
        if nepy>=360:
            nepy=-80*5


        #player movement            
        plx+=plx_change
        ply+=ply_change

        if plx>=540:
            plx=540
            
        if plx<=0:
            plx=0
            
        if ply>=340:
            ply=340

        if ply<=0:
            ply=0


        #enemies' movement
        for i in range(2):
            enx[i]+=enx_change[i]
            if enx[i]>=540:
                enx_change[i]=-(0.1+speed_en)
                eny[i]+=eny_change[i]
            
            if enx[i]<=0:
                enx_change[i]=(0.1+speed_en)
                eny[i]+=eny_change[i]

            if eny[i]>=320:
                eny_change[i]=-40

            if eny[i]<=0:
                eny_change[i]=40


            #collision
            collision=isCollision(enx[i],eny[i],bulletx,bullety)
        
            if collision:
                en_hit[i]+=1
                bullety=ply
                bullet_state="ready"
                score_value+=10
                lives[i]-=1
            
                #explosion_sound=mixer.sound()
                #explosion_sound.play()
            
            if en_hit[i]==5:
                eny[i]=-2000
                enx[i]=0

        #boss movement
        if eny[0]<0 and eny[1]<0:

            lives3=font.render(str(lives[2]), True, (255,255,255))
            screen.blit(lives3,(enx[2]+10,eny[2]-25))
            life(enx[2]+45,eny[2]-25)
            
            enx[2]+=enx_change[2]
            if enx[2]>=540:
                enx_change[2]=-(0.4+speed_en)
                eny[2]+=eny_change[2]
            
            if enx[2]<=0:
                enx_change[2]=(0.4+speed_en)
                eny[2]+=eny_change[2]

            if eny[2]>=320:
                eny_change[2]=-40

            if eny[2]<=0:
                eny_change[2]=40

            #collision
            collision_boss=isCollision(enx[2],eny[2],bulletx,bullety)
        
            if collision_boss:
                en_hit[2]+=1
                bullety=ply
                bullet_state="ready"
                score_value+=20
                lives[2]-=1
                #explosion_sound=mixer.sound()
                #explosion_sound.play()
            
            if en_hit[2]==10:
                eny[2]=-2000
                enx[2]=0

                break
                    
            boss(enx[2],eny[2])
        #bullet movement
        if bullety<=0:
            bullety=ply
            bullet_state="ready"
            
        if bullet_state=="fire":
            fire_bullet(bulletx,bullety)
            bullety-=bullety_change

        #bomb movement
        for i in range(3):
            fire[i]=random.randint(0,1)
            if fire[i] == 1:
                if bomb_state[i]=="ready":
                    bombx[i]=enx[i]
                    bomb_state[i]="fire"
                    screen.blit(bombImg[i], (bombx[i]+16,bomby[i]+10))
                    
                if bomb_state[i]=="fire":
                    fire_bomb(i,bombx[i],bomby[i])
                    bomby[i]+=bomby_change[i]
       
                    
            if bomby[i]>=400:
                bomby[i]=eny[i]
                bomb_state[i]="ready"
            
        
        #Game over
        for i in range(3):
            player_dead=isCollision(enx[i],eny[i],plx,ply)
            player_dead2=isCollision(bombx[i],bomby[i],plx,ply)
            
            if player_dead or player_dead2:
                break
            
        if player_dead or player_dead2:
            enx[1]=-100
            eny[1]=-100
            enx[0]=-100
            eny[0]=-100
            eny[2]=-100
            enx[2]=-100
            
            restart=False
            while not restart:
                anj()
                
                game_over_text()
                showScore(225,240)
                previous_score=score_value

                if (high_score<score_value):
                    high_score=score_value
                    
                with open("HI.txt","w") as f:
                    f.write(str(high_score))
                f.close()
                
                highscore=font.render("High Score: " + str(high_score), True, (255,255,255))
                screen.blit(highscore,(10,60))
                
                previousscore=font.render("Previous Score: " + str(previous_score), True, (255,255,255))
                screen.blit(previousscore,(10,35))
                
                
                
                pygame.display.update()
                
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                            play=False
                            game=False
                            restart=True
                            pygame.quit()
                            break

                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_r:
                            score_value=0
                            speed_en=0
                            speed_bomb=0
                            restart=True
                            game=False
                        elif event.key==pygame.K_q:
                            game=False
                            play=False
                            restart=True
                            pygame.quit()
                            break
                            
                
                clock.tick(8)
                #game_over_sound=mixer.sound()
                #game_over_sound.play()   

        #calling background objects
        saturn1(sat1y)
        star1(star1y)
        jupiter(jupy)
        saturn2(sat2y)
        star2(star2y)
        neptune(nepy)          
        
        player(plx,ply)
        enemies(enx[0], eny[0], enx[1], eny[1])
        
        #lives
        lives1=font.render(str(lives[0]), True, (255,255,255))
        screen.blit(lives1,(enx[0]+20,eny[0]-10))
        life(enx[0]+35,eny[0]-10)
        
        lives2=font.render(str(lives[1]), True, (255,255,255))
        screen.blit(lives2,(enx[1]+20,eny[1]-10))
        life(enx[1]+35,eny[1]-10)
        
        showScore(textx,texty)
        
        #high score
        previousscore=font.render("Previous Score: " + str(previous_score), True, (255,255,255))
        screen.blit(previousscore,(10,35))

        highscore=font.render("High Score: " + str(high_score), True, (255,255,255))
        screen.blit(highscore,(10,60))
            
        pygame.display.update()
        

    

