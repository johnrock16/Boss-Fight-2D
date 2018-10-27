import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, FULLSCREEN, K_f, K_r,K_z,K_x,K_c,K_j,K_SPACE,Rect
from random import randint

pygame.init()
width=800
height=600
screen=pygame.display.set_mode((width,height))
clock=pygame.time.Clock()
pygame.font.init()
fonte=pygame.font.get_default_font()
fontevitoria=pygame.font.SysFont(fonte, 70, bold=True, italic=False)


class Cenario(object):
    def __init__(self):
        self.cenario=pygame.image.load("./imagens/praca.jpeg")
        self.pl = Player(screen, (0,255,0), [150, 240, 75, 150], 0)
        self.sa = Enemy(screen, (0,255,0), [530, 350, 270, 270], 0)
        self.velx = 6
        self.count = 0
        self.rect=Rect((0,598),(800,1))


    def atualizarcenario(self):
        screen.blit(self.cenario,(0,0))
        self.pl.draw()
        self.sa.draw()
        self.pl.update()
        self.sa.update()




class Player(object):
    def __init__(self,screen, cor, rect ,vely):
        self.screen=screen
        self.rect=Rect(rect)
        self.x=0
        self.y=0
        self.pulo=0
        self.velx=0
        self.vely=vely
        self.width=20
        self.height=20
        self.playercor=cor
        self.playeralive=True
        self.fantasia=1
        self.dano=0
        self.ataque=False
        self.fliph=False
        self.vida=3
        self.espera=0




    def draw(self):
        if self.vida<0:
            self.vida=0
        vidastr=str(self.vida)
        vidastr="Player: "+vidastr
        textovida=fontevitoria.render(vidastr,1,(255,255,255))
        self.screen.blit(textovida,(50,50))
        if self.playeralive:
            #pygame.draw.rect(self.screen, self.playercor, self.rect, self.width)

            if self.fantasia==1:
                self.playerimagem=pygame.image.load("./imagens/natan1.png")
                self.playerimagem=pygame.transform.scale(self.playerimagem,(75,150))

            elif self.fantasia==2:
                self.playerimagem=pygame.image.load("./imagens/natan2.png")
                self.playerimagem=pygame.transform.scale(self.playerimagem,(75,150))

            elif self.fantasia==3:
                self.playerimagem=pygame.image.load("./imagens/natan3.png")
                self.playerimagem=pygame.transform.scale(self.playerimagem,(75,150))

            if self.fliph:
                self.playerimagem=pygame.transform.flip(self.playerimagem,True,False)

            self.screen.blit(self.playerimagem, (self.rect[0], self.rect[1]))

        else:
            texto=fontevitoria.render('Você foi matado mano',1,(255,0,00))
            self.screen.blit(texto,(150,300))



    def update(self):
        if self.playeralive:
            if self.rect[1] + self.vely > 450:
                self.vely = 0
            if self.rect[0] + self.velx > 800:
                self.velx = 0
            if self.rect[0] + self.velx < 0:
                self.velx=0

            if self.dano>0:
                self.ataque=True

            if self.vida<=0:
                self.vida=0
                self.playeralive=False
                self.ataque=False


            self.rect[1] += self.vely
            self.vely += 0.15
            self.rect[0] += self.velx



class Enemy(object):
    def __init__(self,screen,cor,rect,vely):
        self.screen=screen
        self.cor=cor
        self.rect=Rect(rect)
        self.x=500
        self.y=400
        self.imagem=pygame.image.load("./imagens/sauva.png")
        self.imagem=pygame.transform.scale(self.imagem,(rect[2],rect[3]))
        self.velx=0
        self.vely=vely
        self.width=20
        self.height=30
        self.sauvaalive=True
        self.vida=100
        self.atacar=False
        self.golpe=""
        self.invencibilidade=False
        self.tempo=0
        self.ataques=0


        self.disparo=self.rect[0]+100
        self.disparos=0
        self.disparoy=self.rect[1]+100
        self.disparorect=Rect(self.disparo,rect[1]+100,20,20)
        self.disparoimagem=pygame.image.load("./imagens/bola.png")
        self.disparoimagem2=pygame.image.load("./imagens/bola2.png")



        self.disparoimagem=pygame.transform.scale(self.disparoimagem,(20,20))
        self.disparoimagem2=pygame.transform.scale(self.disparoimagem2,(20,20))


        self.sauvas=list(range(20))
        self.sauvasvelx=0
        self.sauvasimg=pygame.image.load("./imagens/sauva.png")
        self.sauvasimg=pygame.transform.scale(self.sauvasimg,(120,120))
        self.vezes=0
        self.sauvasrect=list(range(20))


        self.pulo=False
        self.pulodevolta=False
        self.cairdevolta=False
        self.esperapulo=0




    def draw(self):
        #pygame.draw.rect(self.screen, self.cor, self.rect, self.width)
        if self.vida<=0:
            self.vida=0
        vidastring=str(self.vida)
        vidastring="sauva: "+vidastring
        textovida=fontevitoria.render(vidastring,1,(255,255,255))
        self.screen.blit(textovida,(500,50))


        if self.sauvaalive:
            self.screen.blit(self.imagem, (self.rect[0], self.rect[1]))

            

        else:
            texto=fontevitoria.render('Você matou mano',1,(255,0,00))
            self.screen.blit(texto,(150,300))


    def update(self):
        if self.sauvaalive:
            if self.rect[1] + self.vely > 300:
                self.vely = 0
            if self.rect[0] + self.velx > 800:
                self.velx = 0
            if self.rect[0] + self.velx < -350:
                self.velx=0
            if self.vida<=0:
                self.sauvaalive=False
                self.vida=0
                self.atacar=False

            self.disparorect=Rect(self.disparo-12,self.rect[1]+100,20,20)
            self.rect[1] += self.vely
            self.vely += 0.15
            self.rect[0] += self.velx


    def ataque(self):
        if self.sauvaalive:
            r=randint(1,4)
            if(r==1 and self.golpe=="" or self.golpe=="investida"):

                self.velx=0
                self.golpe="investida"
                self.invencibilidade=True
                if (self.rect[0]>=-350):
                    self.velx-=3
                    self.rect[0]+=self.velx


                else:
                    self.invencibilidade=False
                    self.rect[0]=600
                    self.golpe=""
                    self.ataques+=1


            elif(r==2 and self.golpe=="" or self.golpe=="disparo"):
                self.atacar=True
                self.golpe="disparo"
                self.invencibilidade=False
                if(self.disparo>=-0):
                    self.disparo-=6
                    self.screen.blit(self.disparoimagem, (self.disparo, self.rect[1]+100))
                else:
                    self.disparo=self.rect[0]+75
                    self.golpe=""
                    self.ataques+=1


            elif(r==3 and self.golpe=="" or self.golpe=="sauvas"):

                self.velx=0
                self.golpe="sauvas"
                self.invencibilidade=False
                self.vezes=0


                x=self.rect[0]

                self.sauvasvelx-=5
                for i in range(7):
                    self.sauvas[i]=(i*360)+self.sauvasvelx
                    if(self.sauvas[i]>=-2000):
                        self.screen.blit(self.sauvasimg, (self.sauvas[i]-800+2000+0,500))
                        self.sauvasrect[i]=Rect(self.sauvas[i]-800+2020+0,500+50,80,40)

                    if(self.sauvas[6]<=-1600):
                        self.golpe=""
                        self.ataques+=1
                        self.sauvasvelx=0
                        for i in range(7):
                            self.sauvas[i]=0

            elif(r==4 and self.golpe=="" or self.golpe=="pulo"):
                self.vely=0
                self.velx=0
                self.atacar=False
                self.golpe="pulo"
                self.invencibilidade=True

                if (self.rect[1]>=0 and ((self.pulo==False or self.pulodevolta) and self.cairdevolta==False)and self.esperapulo<=150):
                    self.vely-=4
                    if(self.pulodevolta==False):
                        self.velx-=1.5
                    elif(self.pulodevolta):
                        self.velx+=2.1
                    self.rect[1]+=self.vely
                    self.rect[0]+=self.velx


                elif(self.rect[1]<=0 and (self.pulo==False or self.pulodevolta)):
                    self.pulo=True
                    if(self.pulodevolta):
                        self.cairdevolta=True
                        self.pulodevolta=False
                        print(self.cairdevolta)
                        print(self.rect[1])





                elif((self.pulo or self.cairdevolta) and self.rect[1]<=350 ):
                    self.vely+=2
                    if(self.rect[0]>=0):
                        if(self.cairdevolta==False):
                            self.velx-=1.5
                        elif(self.cairdevolta):
                            if(self.rect[0]<=530):
                                self.velx+=2
                    self.rect[1]+=self.vely
                    self.rect[0]+=self.velx



                elif(self.esperapulo<=150 and self.pulodevolta==False):
                    self.invencibilidade=False
                    self.esperapulo+=1

                elif(self.esperapulo>150 and self.pulodevolta==False):
                    self.pulodevolta=True
                    self.pulo=False
                    self.invencibilidade=True
                    self.esperapulo=0










                else:
                    self.invencibilidade=False
                    self.esperapulo=0
                    self.pulo=False
                    self.pulodevolta=False
                    self.cairdevolta=False
                    self.rect[1]=350
                    self.rect[0]=530
                    self.golpe=""
                    self.ataques+=1










            if(self.ataques>=5 and self.golpe=="" or self.golpe=="disparos"):
                self.atacar=True
                self.golpe="disparos"
                self.invencibilidade=False
                if(self.disparos<=3):
                    if(self.disparos%2==0):
                        if(self.disparo>=-0):
                            self.disparo-=8
                            self.screen.blit(self.disparoimagem2, (self.disparo, self.rect[1]+100))
                        else:
                            self.disparos+=1
                    elif(self.disparos%2!=0):
                        if(self.disparo<=800):
                            self.disparo+=8
                            self.screen.blit(self.disparoimagem2, (self.disparo, self.rect[1]+100))
                        else:
                            self.disparos+=1
                else:
                    self.disparo=self.rect[0]+75
                    self.golpe=""
                    self.ataques=0
                    self.disparos=0


            '''if(self.ataques==5 and self.golpe=="" or self.golpe=="espera"):
               self.golpe="espera"
                self.invencibilidade=False
                self.atacar=False

                if(self.tempo<=300):
                    self.tempo+=1
                else:
                    tempo=0
                    self.golpe=""
                    self.ataques=0
                 self.tempo=0 '''














__init__="__main__"

rodar=True
cenario=Cenario()

espera=0
acertado=False
falas=False
esperafalas=0
musica=True
sompausado=0


while rodar:
    cenario.atualizarcenario()
    clock.tick(120)

    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_f:
                exit()

            if e.key == K_UP:
                #pulo = 1
                if(cenario.pl.pulo<1):
                    cenario.pl.vely = -7.9
                    cenario.pl.pulo+=1

            if e.key == K_RIGHT:
                cenario.pl.velx = 3
                cenario.pl.fliph=False

            if e.key == K_LEFT:
                cenario.pl.velx = -6
                cenario.pl.fliph=True
            if e.key==K_z:
                if cenario.pl.espera==0:
                    cenario.pl.espera+=10
                    cenario.pl.fantasia=2
                    cenario.pl.dano=1


                    if cenario.pl.ataque:
                        if cenario.pl.rect.colliderect(cenario.sa.rect):
                            cenario.sa.vida+=-cenario.pl.dano

            if e.key==K_x:
                if cenario.pl.espera==0:
                    cenario.pl.espera+=30
                    cenario.pl.fantasia=3
                    cenario.pl.dano=2

                    if cenario.pl.ataque:
                        if cenario.pl.rect.colliderect(cenario.sa.rect):
                            cenario.sa.vida+=-cenario.pl.dano

            if e.key==K_c:
                if cenario.pl.espera==0:
                    cenario.pl.espera+=50
                    cenario.pl.fantasia=3
                    if cenario.pl.pulo<=2:
                        cenario.pl.vely = -3
                        cenario.pl.pulo+=1
                    cenario.pl.dano=3
                    if cenario.pl.ataque:
                        if cenario.pl.rect.colliderect(cenario.sa.rect) and cenario.pl.ataque:
                            cenario.sa.vida+=-cenario.pl.dano


            if(e.key==K_SPACE):
                if(cenario.pl.fliph==False):
                    cenario.pl.rect[0]+=100
                    print("buenos dias chiquitos")
                elif(cenario.pl.fliph):
                    cenario.pl.rect[0]-=100






        if e.type == KEYUP:
            if e.key == K_RIGHT and cenario.pl.velx > 0:
                cenario.pl.velx = 0
            if e.key == K_LEFT and cenario.pl.velx < 0:
                cenario.pl.velx = 0

            if e.key==K_z:
                cenario.pl.fantasia=1

            if e.key==K_x:
                cenario.pl.fantasia=1

            if e.key==K_c:
                cenario.pl.fantasia=1

    if(cenario.pl.rect.colliderect(cenario.rect)):
        cenario.pl.pulo=0

    if cenario.sa.rect.colliderect(cenario.pl.rect) and espera==0 and cenario.sa.invencibilidade:

        cenario.pl.vida-=1
        acertado=True


    elif cenario.sa.golpe=="sauvas":
        for i in range(7):
            if cenario.sa.sauvasrect[i].colliderect(cenario.pl.rect) and espera==0:
                cenario.pl.vida-=1
                acertado=True

    elif cenario.sa.disparorect.colliderect(cenario.pl.rect) and cenario.sa.atacar and espera==0:

        cenario.pl.vida-=1
        acertado=True

    if acertado:
        espera+=1
        if(espera>=150):
            espera=0
            acertado=False

    if falas:
        esperafalas+=1
        if(esperafalas>=350):
            esperafalas=0
            falas=False
            musica=True
            sompausado=0





    if cenario.pl.espera>0:
        cenario.pl.espera-=1
    else:
        cenario.pl.espera=0


    cenario.sa.ataque()
    print(esperafalas)
    print(falas)
    print(musica)
    pygame.display.update()
