import random
import time
import pygame;

# 飞机类
class Player(pygame.sprite.Sprite):
    # 存放所有危机的子弹组
    bullets=pygame.sprite.Group()
    
    def __init__(self,screen):
        # 精灵初始化
        pygame.sprite.Sprite.__init__(self)
                    # 创建飞机图片
        self.image=pygame.image.load("pythonGame/images/me1.png")
        # 根据图片获取矩形对象
        self.rect=self.image.get_rect()
        self.rect.topleft=[480/2-100/2,550]
 
        # 飞机速度
        self.speed=5
        self.screen=screen
        
        # 装子弹的列表
        self.bullets=pygame.sprite.Group()

    def update(self):
        self.key_control()
        self.display()
        
    def key_control(self):
        # 监听键盘事件
            key_pressed=pygame.key.get_pressed()
            
            if key_pressed[pygame.K_w] and self.rect.top>0:
                self.rect.top-=self.speed
            if key_pressed[pygame.K_s] and self.rect.bottom<600:
                self.rect.bottom+=self.speed
            if key_pressed[pygame.K_a] and self.rect.left>-50:
                self.rect.left-=self.speed
            if key_pressed[pygame.K_d] and self.rect.right<520:
                self.rect.right+=self.speed
            if key_pressed[pygame.K_SPACE]:
                #按下空格键发射子弹
                bullet=Bullet(self.screen,self.rect.left,self.rect.top)
                # 把子弹加入列表中
                self.bullets.add(bullet)
                # 存放所有子弹飞机的组
                Player.bullets.add(bullet)
        
    def display(self):
               # 把飞机加入到窗口
        self.screen.blit(self.image,self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把子弹加入到屏幕
        self.bullets.draw(self.screen)
        
    @classmethod
    def clear_bullets(cls):
        # 清空子弹
        cls.bullets.empty()
            
            
# 敌方飞机类    
class Enemy(pygame.sprite.Sprite):
        # 敌方所有子弹
    enemy_bullets=pygame.sprite.Group()
    def __init__(self,screen):
        # 精灵初始化
        pygame.sprite.Sprite.__init__(self)
                    # 创建飞机图片
        self.image=pygame.image.load("pythonGame/images/enemy1.png")
        # 根据图片获取矩形对象
        self.rect=self.image.get_rect()
        x=random.randrange(1,Manager.bg_size[0],50)
        self.rect.topleft=[x,0]
  
        # 飞机速度
        self.speed=3
        self.screen=screen
        
        # 装子弹的列表
        self.bullets=pygame.sprite.Group()
        # 敌机移动方向
        self.direction='right'
    def display(self):
               # 把飞机加入到窗口
        self.screen.blit(self.image,self.rect)
                # 更新子弹坐标
        self.bullets.update()
        # 把子弹加入到屏幕
        self.bullets.draw(self.screen)
    def update(self):
        self.auto_move()
        self.auto_fire()
        self.display()
        
    def auto_move(self):
        if self.direction=='right':
            self.rect.right+=self.speed
        elif self.direction=='left':
            self.rect.left-=self.speed
        if self.rect.right>420:
            self.direction='left'
        elif self.rect.right<0:
            self.direction='right'
        self.rect.bottom+=self.speed
            
    def auto_fire(self):
        random_num=random.randint(1,50) 
        if random_num==8:
        # 自动开火
            bullet=EnemyBullet(self.screen,self.rect.left,self.rect.top)
            self.bullets.add(bullet)
            # 把子弹添加到精灵类
            Enemy.enemy_bullets.add(bullet)
    @classmethod
    def clear_bullets(cls):
        # 清空子弹
        cls.enemy_bullets.empty()
            

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        # 精灵初始化
        pygame.sprite.Sprite.__init__(self)
        # 子弹图片
        self.image=pygame.image.load("pythonGame/images/bullet2.png")
        # 获取矩形对象
        self.rect=self.image.get_rect()
        self.rect.topleft=[x+100/2,y-10]
        # 窗口
        self.screen=screen
        # 速度
        self.speed=10
    def update(self):
        self.rect.top-=self.speed
        # 如果子弹移到屏幕上方，就销毁子弹
        if self.rect.top<-22:
            self.kill()
        
        
# 敌方子弹类
class EnemyBullet(pygame.sprite.Sprite):

    def __init__(self,screen,x,y):
        # 精灵初始化
        pygame.sprite.Sprite.__init__(self)
        # 子弹图片
        self.image=pygame.image.load("pythonGame/images/bullet1.png")
        # 获取矩形对象
        self.rect=self.image.get_rect()
        self.rect.topleft=[x+50/2-8/2,y+39]
        # 窗口
        self.screen=screen
        # 速度
        self.speed=4
    def update(self):
        self.rect.top+=self.speed
        # 如果子弹移到屏幕上方，就销毁子弹
        if self.rect.top>600:
            self.kill()
        
# 音乐类       
class GameSound(object):
    def __init__(self):
        # 音乐模块初始化
        pygame.mixer.init()
        pygame.mixer.music.load("pythonGame/sound/game_music.ogg")
        pygame.mixer.music.set_volume(0.5)
        self.__bomb=pygame.mixer.Sound('pythonGame/sound/use_bomb.wav')
    def playBackgroundMusic(self):
        # 播放音乐
        pygame.mixer.music.play(-1)
    def playBombSound(self):
        pygame.mixer.Sound.play(self.__bomb)


# 碰撞类
class Bomb(object):
    # 初始化碰撞
    def __init__(self,screen,type):
        self.screen=screen
        if type=="enemy":
            # 加载爆炸资源
            self.mImage=[(pygame.image.load("pythonGame/images/enemy1_down"+str(v)+".png")) for v in range(1,5)]
        else:
            self.mImage=[(pygame.image.load("pythonGame/images/me_destroy_"+str(v)+".png")) for v in range(1,5)]
    # 设置当前爆炸播放索引
        self.mIndex=0
    #  爆炸设置
        self.mPos=[0,0]
    # 是否可见
        self.mVisible=False
    def action(self,rect):
        # 触发爆炸的方法draw
        self.mPos[0]=rect.left
        self.mPos[1]=rect.top
        # 打开爆炸的开关
        self.mVisible=True
    def draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImage[self.mIndex],(self.mPos[0],self.mPos[1]))
        self.mIndex+=1
        if self.mIndex>=len(self.mImage):
            self.mIndex=0
            self.mVisible=False


class GameBackGround(object):
    def __init__(self,screen):
        self.mImage1=pygame.image.load("pythonGame/images/background.png")
        self.mImage2=pygame.image.load("pythonGame/images/background.png")
        self.screen=screen
        self.y1=0
        self.y2=-Manager.bg_size[1]
    # 移动地图
    def move(self):
        self.y1+=2
        self.y2+=2
        if self.y1>=Manager.bg_size[1]:
            self.y1=0
        if self.y2>=0:
            self.y2=-Manager.bg_size[1]
    # 绘制地图
    def draw(self):
        self.screen.blit(self.mImage1,(0,self.y1))
        self.screen.blit(self.mImage2,(0,self.y2))
        

# 管理类      
class Manager(object):
    bg_size=(480,700)
    # 游戏倒计时的id
    game_over_id=11
    # 游戏是否结束
    is_game_over=False
    # 创建敌机定时器的id
    create_enemy_id=10
    # 倒计时时间
    over_time=3
    # 得分
    score=0
    
    def __init__(self):
        pygame.init()
        # 创建窗口
        self.screen=pygame.display.set_mode(self.bg_size,0,32)
        # 创建背景图片
        self.background=pygame.image.load("pythonGame/images/background.png")
        # 初识化一个装有玩家精灵类的group
        self.players=pygame.sprite.Group()
        # 初始化一个装敌机的精灵类的group
        self.enemys=pygame.sprite.Group()
        # 初始化玩家爆炸的对象
        self.player_bomb=Bomb(self.screen,'player')
        # 初始化敌机爆炸的对象
        self.enemy_bomb=Bomb(self.screen,'enemy')
        # 初始化声音的对象
        self.sound=GameSound()
        # 调用地图类方法
        self.map=GameBackGround(self.screen)
        
        
    def exit(self):
        print('退出')
        pygame.quit()
        exit()
    
    def show_over_text(self):
        # 游戏结束后，倒计时重新开始
        self.drawText('GameOver %d'%Manager.over_time,100,Manager.bg_size[1]/2,textHeight=50,fontColor=[255,0,0])
    def game_over_time(self):
        self.show_over_text()
        # 倒计时-1
        Manager.over_time-=1
        if Manager.over_time==0:
            # 参数设置为0，游戏结束
            pygame.time.set_timer(Manager.game_over_id,0)
            # 倒计时结束后重新开始
            Manager.over_time=3
            Manager.is_game_over=False
            Manager.score=0
            self.start_game()
    def start_game(self):
        # 重新开始游戏
        Player.clear_bullets()
        Enemy.clear_bullets()
        manager=Manager()
        manager.main()
        
    def new_player(self):
        # 创建玩家飞机添加到group中
        player=Player(self.screen)
        self.players.add(player)
    def new_enemy(self):
        # 创建敌机添加到group中
        enemy=Enemy(self.screen)
        self.enemys.add(enemy)
    def drawText(self,text,x,y,textHeight=30,fontColor=(255,0,0),backgroundColor=None):
        # 通过字体文件获取字体对象
        font_obj=pygame.font.Font("pythonGame/font/font.ttf",textHeight)
        # 配置你要显示的文字
        text_obj=font_obj.render(text,True,fontColor,backgroundColor)
        # 获取你要显示对象的rect
        text_rect=text_obj.get_rect()  
        # 设置显示对象的坐标
        text_rect=(x,y)      
        # 绘制字到指定区域
        self.screen.blit(text_obj,text_rect)
        
    def main(self):
        # 播放音乐
        self.sound.playBackgroundMusic()
        # 创建一个玩家
        self.new_player()
        # 开启创建敌机的定时器
        pygame.time.set_timer(Manager.create_enemy_id,1000)
        while True:
            # 把背景添加到窗口
            self.screen.blit(self.background,(0,0))
            # 移动地图
            self.map.move()
            # 把地图贴到窗口
            self.map.draw()
            
            # 绘制文字
            self.drawText('hp:%d'%Manager.score,0,0)
            
            if Manager.is_game_over:
                # 判断游戏结束才显示结束文字
                self.show_over_text()
            
            #获取事件
            for event in pygame.event.get():
                # 判断事件类型
                if event.type==pygame.QUIT:
                    # 退出
                    self.exit()
                elif event.type==Manager.create_enemy_id:
                    # 创建一个敌机
                    self.new_enemy()
                elif event.type==Manager.game_over_id:
                    # 定时器触发的事件
                    self.game_over_time()
                     
            # 调用爆炸的对象
            self.player_bomb.draw()   
            self.enemy_bomb.draw()        
            # 判断碰撞
            iscollide=pygame.sprite.groupcollide(self.players,self.enemys,True,True)
            
            if iscollide:
                Manager.is_game_over=True
                pygame.time.set_timer(Manager.game_over_id,1000)
                items=list(iscollide.items())[0]
                print(items)
                x=items[0]
                y=items[1][0]
                # 玩家爆炸图片
                self.player_bomb.action(x.rect)
                # 敌机爆炸图片
                self.enemy_bomb.action(y.rect)
                # 爆炸声音
                self.sound.playBombSound()
            
            # 玩家子弹和所有敌机的碰撞判断
            is_enemy=pygame.sprite.groupcollide(Player.bullets,self.enemys,True,True)
            if is_enemy:
                items=list(is_enemy.items())[0]
                y=items[1][0]
                # 敌机爆炸图片
                self.enemy_bomb.action(y.rect)
                # 爆炸声音
                self.sound.playBombSound()
                Manager.score+=100
            # 玩家飞机和敌机子弹的判断
            if self.players.sprites():
                isover=pygame.sprite.spritecollide(self.players.sprites()[0],Enemy.enemy_bullets,True)
                if isover:
                    # 游戏结束
                    Manager.is_game_over=True
                    pygame.time.set_timer(Manager.game_over_id,1000)
                    self.player_bomb.action(self.players.sprites()[0].rect)
                    # 移除精灵组
                    self.players.remove(self.players.sprites()[0])
                    # 爆炸的声音
                    self.sound.playBombSound()
                    
            
            # 玩家飞机和子弹显示
            self.players.update()
            # 敌机和子弹的显示
            self.enemys.update()
            # 刷新窗口内容
            pygame.display.update()
            time.sleep(0.01)
            
            
if __name__=='__main__':
    manager=Manager()
    manager.main()