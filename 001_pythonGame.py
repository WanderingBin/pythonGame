import time
import pygame;



def main():
    ''' 完成整个程序的控制 '''
    # 创建一个窗口
    screen=pygame.display.set_mode((480,700),0,32)
    # 创建一个图片当做背景
    background=pygame.image.load("pythonGame/images/background.png")
    # 创建飞机图片
    player=pygame.image.load("pythonGame/images/me1.png")  
    x=480/2-100/2
    y=550
    speed=5
    while True:
        # 将背景贴到窗口中
        screen.blit(background,(0,0))
       # 把飞机加入到界面
        screen.blit(player,(x,y))
        #获取事件
        for event in pygame.event.get():
            # 判断事件类型
            if event.type==pygame.QUIT:
                # 执行退出
                pygame.quit()
                # 程序退出
                exit()
            # 监听键盘事件
            key_pressed=pygame.key.get_pressed()
            
            if key_pressed[pygame.K_w]:
                print('上')
                y-=speed
            if key_pressed[pygame.K_s]:
                print('下')
                y+=speed
            if key_pressed[pygame.K_a]:
                print('左')
                x-=speed
            if key_pressed[pygame.K_d]:
                print('右')
                x+=speed
            if key_pressed[pygame.K_SPACE]:
                print('空格')
        # 显示窗口的内容
        pygame.display.update();
        time.sleep(0.001);

if __name__=='__main__':
    main()