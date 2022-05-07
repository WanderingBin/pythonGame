import random
from telnetlib import GA
import time
import pygame;

# 飞机类
class Player(object):
    def __init__(self,screen):
            # 创建飞机图片
        self.player=pygame.image.load("pythonGame/images/me1.png")  
        self.x=480/2-100/2
        self.y=550
        self.speed=5
        self.screen=screen
        
        # 装子弹的列表
        self.bullets=[]
    def key_control(self):
        # 监听键盘事件
            key_pressed=pygame.key.get_pressed()
            
            if key_pressed[pygame.K_w] and self.y>0:
                self.y-=self.speed
            if key_pressed[pygame.K_s] and self.y<600:
                self.y+=self.speed
            if key_pressed[pygame.K_a] and self.x>-50:
                self.x-=self.speed
            if key_pressed[pygame.K_d] and self.x<420:
                self.x+=self.speed
            if key_pressed[pygame.K_SPACE]:
                #按下空格键发射子弹
                bullet=Bullet(self.screen,self.x,self.y)
                # 把子弹加入列表中
                self.bullets.append(bullet)
    def display(self):
               # 把飞机加入到窗口
        self.screen.blit(self.player,(self.x,self.y))
        # 遍历所有子弹显示在窗口
        for bullet in self.bullets:
            bullet.auto_move()
            bullet.display()
            
            
# 敌方飞机类    
class Enemy(object):
    def __init__(self,screen):
            # 创建飞机图片
        self.player=pygame.image.load("pythonGame/images/enemy1.png")  
        self.x=0
        self.y=0
        self.speed=5
        self.screen=screen
        # 敌机方向属性
        self.direction='right'
        # 装子弹的列表
        self.bullets=[]
    def display(self):
               # 把飞机加入到窗口
        self.screen.blit(self.player,(self.x,self.y))

    def auto_move(self):
        if self.direction=='right':
            self.x+=self.speed
            if self.x>420:
                self.direction='left'
        elif self.direction=='left' and self.x>0:
            self.x-=self.speed
            if self.x<1:
                self.direction='right'
    def auto_fire(self):
        random_num=random.randint(1,50) 
        if random_num==8:
        # 自动开火
            bullet=EnemyBullet(self.screen,self.x,self.y)
            self.bullets.append(bullet)
            # 遍历所有子弹显示在窗口
        for bullet in self.bullets:
            bullet.auto_move()
            bullet.display()  

# 子弹类
class Bullet(object):
    def __init__(self,screen,x,y):
        self.x=x+100/2
        self.y=y-10
        self.speed=10
        self.screen=screen
        # 子弹图片
        self.image=pygame.image.load("pythonGame/images/bullet2.png")
    def display(self):
        #  显示子弹窗口
        self.screen.blit(self.image,(self.x,self.y))
    def auto_move(self):
        # 子弹移动
        self.y-=self.speed
# 敌方子弹类
class EnemyBullet(object):
    def __init__(self,screen,x,y):
        self.x=x+50/2-8/2
        self.y=y+39
        self.speed=10
        self.screen=screen
        # 子弹图片
        self.image=pygame.image.load("pythonGame/images/bullet1.png")
    def display(self):
        #  显示子弹窗口
        self.screen.blit(self.image,(self.x,self.y))
    def auto_move(self):
        # 子弹移动
        self.y+=self.speed
        
        
class GameSound(object):
    def __init__(self):
        # 音乐模块初始化
        pygame.mixer.init()
        pygame.mixer.music.load("pythonGame/sound/game_music.ogg")
        pygame.mixer.music.set_volume(0.5)
    def playBackgroundMusic(self):
        # 播放音乐
        pygame.mixer.music.play(-1)
    
        
def main():
    ''' 完成整个程序的控制 '''
    sound=GameSound()
    sound.playBackgroundMusic()
    # 创建一个窗口
    screen=pygame.display.set_mode((480,700),0,32)
    # 创建一个图片当做背景
    background=pygame.image.load("pythonGame/images/background.png")
    # 飞机对象
    player=Player(screen)
    # 敌方飞机对象
    enemy=Enemy(screen)
    
    while True:
        # 将背景贴到窗口中
        screen.blit(background,(0,0))

        #获取事件
        for event in pygame.event.get():
            # 判断事件类型
            if event.type==pygame.QUIT:
                # 执行退出
                pygame.quit()
                # 程序退出
                exit()
        # 飞机按键监听
        player.key_control()
        player.display()
        
        # 显示敌机
        enemy.display()
        enemy.auto_move()
        
        # 敌机自动调用开火
        enemy.auto_fire()
        
        # 显示窗口的内容
        pygame.display.update();
        time.sleep(0.01);

if __name__=='__main__':
    main()