import pygame
pygame.init()


w=pygame.display.set_mode((1200,750))
fps=60
saat=pygame.time.Clock()

class Oyun():
    def __init__(self,oyuncu1,oyuncu2,top_grup):
        self.oyuncu1=oyuncu1
        self.oyuncu2=oyuncu2
        self.top_grup=top_grup
        self.arkaplan=pygame.image.load('arka_plan.jpg')
        self.oyunbitti=pygame.image.load('oyun_bitti.jpg')

        self.oyuncu1_puan=0
        self.oyuncu2_puan=0
        self.puan=5
        self.fps_say=0
        self.sayac=50

        self.oyun_font=pygame.font.Font('oyun_font.ttf',40)

        self.kenar_ses=pygame.mixer.Sound('../oyun_ateritenis/puan_gitti.wav')
        self.carpisma_ses=pygame.mixer.Sound('../oyun_ateritenis/temas.wav')
        pygame.mixer.music.load('oyun_sarki.wav')
        pygame.mixer.music.play(-1)
    def update(self):
        if self.fps_say==fps:
            self.sayac-=1
            self.fps_say =0
        self.fps_say+=1
        if self.sayac==0:
            self.bitir()


    def cizdir(self):
        w.blit(self.arkaplan,(0,0))

        puan1=self.oyun_font.render('oyuncu1 puan:'+str(self.oyuncu1_puan),True,(0,50,100))
        puan1_konum=puan1.get_rect()
        puan1_konum.topleft=(30,50)

        puan2=self.oyun_font.render('oyuncu2 puan:'+str(self.oyuncu2_puan),True,(0,50,100))
        puan2_konum=puan2.get_rect()
        puan2_konum.topleft=(1200-340,50)

        sayac_yazi=self.oyun_font.render('kalan süre:'+str(self.sayac),True,(0,50,100))
        sayac_yazi_konum=sayac_yazi.get_rect()
        sayac_yazi_konum.topleft=(500,40 )

        w.blit(puan1,puan1_konum)
        w.blit(puan2, puan2_konum)
        w.blit(sayac_yazi, sayac_yazi_konum)

    def temas(self):
        if pygame.sprite.spritecollide(self.oyuncu1,self.top_grup,False):
            self.carpisma_ses.play()
            for top in self.top_grup.sprites():
                top.xkor*=-1

        if pygame.sprite.spritecollide(self.oyuncu2,self.top_grup,False):
            self.carpisma_ses.play()
            for top in self.top_grup.sprites():
                top.xkor*=-1

    def oyun_durum(self):
        for top in self.top_grup.sprites():
            if top.rect.left<=0:
                self.oyuncu2_puan+=5
                top.rect.centerx=600
                top.rect.centery=300
            if top.rect.right>=1200:
                self.oyuncu1_puan+=5
                top.rect.centerx=600
                top.rect.centery=300

    def bitir(self):
        global d
        etkinlik=True

        if self.oyuncu1_puan>self.oyuncu2_puan:
            kazanan_yazi=self.oyun_font.render('oyuncu1 kazandı',True,(0,50,100))
            kazanan_yazi_konum=kazanan_yazi.get_rect()
            kazanan_yazi_konum.topleft=(450,750//2)
        if self.oyuncu1_puan<self.oyuncu2_puan:
            kazanan_yazi=self.oyun_font.render('oyuncu2 kazandı',True,(0,50,100))
            kazanan_yazi_konum=kazanan_yazi.get_rect()
            kazanan_yazi_konum.topleft=(450,750//2)
        if self.oyuncu1_puan==self.oyuncu2_puan:
            kazanan_yazi=self.oyun_font.render('berabere',True,(0,50,100))
            kazanan_yazi_konum=kazanan_yazi.get_rect()
            kazanan_yazi_konum.topleft=(450,750//2)
        w.blit(self.oyunbitti, (0, 0))
        w.blit(kazanan_yazi,kazanan_yazi_konum)
        pygame.display.update()

        while etkinlik:
            for z in pygame.event.get():
                if z.type==pygame.KEYDOWN:
                    if z.key==pygame.K_SPACE:
                        etkinlik=False
                        self.oyun_reset()

                if z.type==pygame.QUIT:
                    self.sayac=50
                    etkinlik=False

        pygame.display.update()
    def oyun_reset(self):
        self.sayac=50
        self.oyuncu2_puan=0
        self.oyuncu1_puan=0


class Oyuncu1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('1_oyuncu.png')
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.hiz=15
    def update(self):
        tus=pygame.key.get_pressed()
        if tus[pygame.K_w] and self.rect.top>5:
            self.rect.y-=self.hiz
        if tus[pygame.K_s] and self.rect.bottom<745:
            self.rect.y+=self.hiz

class Oyuncu2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('2_oyuncu.png')
        self.rect=self.image.get_rect()
        self.rect.x=1130
        self.hiz=15

    def update(self):
        tus=pygame.key.get_pressed()
        if tus[pygame.K_UP] and self.rect.top>0:
            self.rect.y-=self.hiz
        if tus[pygame.K_DOWN] and self.rect.bottom<750:
            self.rect.y+=self.hiz

class Top(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('top.png')
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.hiz=10
        self.xkor=1
        self.ykor=1
    def update(self):
        self.rect.centerx+=self.hiz*self.xkor
        self.rect.centery+= self.hiz*self.ykor
        if self.rect.left<=0 or self.rect.right>=1200:
            self.xkor*=-1
        if self.rect.top<=0 or self.rect.bottom>=750:
            self.ykor*=-1

oyuncu1_grup=pygame.sprite.Group()
oyuncu1=Oyuncu1()
oyuncu1_grup.add(oyuncu1)

oyuncu2_grup=pygame.sprite.Group()
oyuncu2=Oyuncu2()
oyuncu2_grup.add(oyuncu2)

top_grup=pygame.sprite.Group()
top=Top(600,350)
top_grup.add(top)

oyun=Oyun(oyuncu1,oyuncu2,top_grup)

d=True
while d:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            d=False
    oyun.cizdir()
    oyuncu1_grup.update()
    oyuncu1_grup.draw(w)
    oyuncu2_grup.update()
    oyuncu2_grup.draw(w)
    oyun.update()
    top_grup.update()
    top_grup.draw(w)
    oyun.temas()
    oyun.oyun_durum()
    pygame.display.update()
    saat.tick(fps)



pygame.quit()
