import pygame
import sys
import os
from category import Platform, Coin, Goal, Obstacle, Item, SCREEN_WIDTH, SCREEN_HEIGHT

# 定义 resource_path 函数
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Level:
    # 初始化关卡类
    def __init__(self, level_num: int):
        self.level_num = level_num
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.goal = None
        self.items = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.player_start_x = 50
        self.player_start_y = 500
        self.time_limit = 120  # 默认时间限制（秒）
        self.background_path = self.get_background_path()  # 背景图路径
        self.level_description = ""  # 新增属性，用于存储关卡描述
        self.setup_level()

    # 获取当前关卡的背景图路径，在这里设置背景图路径
    def get_background_path(self):
        background_files = [
            resource_path("resource/image/background/background1.webp"),    # 第0关
            resource_path("resource/image/background/background2.webp"),    # 第1关
            resource_path("resource/image/background/background3.webp"),    # 第2关
            resource_path("resource/image/background/background4.webp"),    # 第3关
            resource_path("resource/image/background/background5.webp"),    # 第4关
            resource_path("resource/image/background/background6.webp"),    # 第5关
            resource_path("resource/image/background/background7.webp"),    # 第6关
            resource_path("resource/image/background/background8.webp"),    # 第7关
            resource_path("resource/image/background/background9.webp"),    # 第8关
            resource_path("resource/image/background/background10.webp")     # 第9关
        ]
        return background_files[self.level_num]

    # 加载背景图（保持原比例）
    def load_background(self):
        try:
            # 使用 self.background_path 加载对应关卡的背景图
            original_bg = pygame.image.load(self.background_path).convert()
            bg_ratio = original_bg.get_width() / original_bg.get_height()
            screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
            if bg_ratio > screen_ratio:
                new_height = SCREEN_HEIGHT
                new_width = int(new_height * bg_ratio)
            else:
                new_width = SCREEN_WIDTH
                new_height = int(new_width / bg_ratio)
            scaled_bg = pygame.transform.scale(original_bg, (new_width, new_height))
            x_offset = (new_width - SCREEN_WIDTH) // 2
            y_offset = (new_height - SCREEN_HEIGHT) // 2
            return scaled_bg.subsurface((x_offset, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            return None

    # 根据关卡号设置不同的关卡布局
    def setup_level(self):
        # 根据关卡号设置不同的关卡布局
        if self.level_num == 0:
            self.setup_tutorial_level()
        elif self.level_num == 1:
            self.setup_level_1()
        elif self.level_num == 2:
            self.setup_level_2()
        elif self.level_num == 3:
            self.setup_level_3()
        elif self.level_num == 4:
            self.setup_level_4()
        elif self.level_num == 5:
            self.setup_level_5()
        elif self.level_num == 6:
            self.setup_level_6()
        elif self.level_num == 7:
            self.setup_level_7()
        elif self.level_num == 8:
            self.setup_level_8()
        elif self.level_num == 9:
            self.setup_level_9()

    # 教程关卡(第0关）布局
    def setup_tutorial_level(self):
        # 教程关卡
        self.time_limit = 60
        self.level_description = "方向键移动，空格或上跳跃，注意躲避耄耋"

        # 地面
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, platform_type="platform_2"))

        # 平台
        self.platforms.add(Platform(100, 450, 100, 20, platform_type="platform_1"))
        self.platforms.add(Platform(300, 400, 100, 20, platform_type="platform_1"))
        self.platforms.add(Platform(500, 350, 100, 20, platform_type="platform_1"))

        # 金币
        self.coins.add(Coin(140, 430))
        self.coins.add(Coin(340, 380))
        self.coins.add(Coin(540, 330))

        #障碍物
        self.obstacles.add(Obstacle(250, 300, "obstacle_1", move_pattern="horizontal")) # 水平移动
        self.obstacles.add(Obstacle(450, 350, "obstacle_1", move_pattern="vertical"))   # 垂直移动

        # 终点
        self.goal = Goal(700, 300)

    # 第一关布局
    def setup_level_1(self):
        self.level_description = "需要校卡才能进入学校，记得先拿校卡"
        # 地面
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, platform_type="platform_2"))

        # 平台
        self.platforms.add(Platform(150, 470, 150, 20, platform_type="platform_1"))
        self.platforms.add(Platform(550, 470, 150, 20, platform_type="platform_1"))

        # 墙壁
        self.platforms.add(Platform(200, 300, 20, 100, platform_type="platform_1"))
        self.platforms.add(Platform(680, 470, 20, 80, platform_type="platform_1"))

        # 金币
        self.coins.add(Coin(190, 430))

        # 障碍物
        self.obstacles.add(Obstacle(500, 420, "obstacle_1",move_pattern="vertical"))

        # 道具
        self.items.add(Item(720, 500, "card"))

        # 终点
        self.goal = Goal(600, 500)
 
    # 第二关布局
    def setup_level_2(self):
        self.time_limit = 120
        self.level_description = "鸡哥是不会伤害你的"

        # 地面
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, "platform_2"))

        # 平台
        self.platforms.add(Platform(150, 470, 150, 20, "platform_1"))
        self.platforms.add(Platform(350, 380, 100, 20, "platform_1"))
        self.platforms.add(Platform(550, 370, 100, 20, "platform_1"))
        self.platforms.add(Platform(50, 280, 70, 20, "platform_1"))

        # 墙壁
        self.platforms.add(Platform(200, 300, 20, 100, "platform_1"))

        # 金币
        self.coins.add(Coin(190, 430))
        self.coins.add(Coin(390, 430))
        self.coins.add(Coin(590, 350))
        self.coins.add(Coin(80, 210))

        # 障碍物
        self.obstacles.add(Obstacle(150, 320, "obstacle_1" , move_pattern="horizontal"))
        self.obstacles.add(Obstacle(470, 330, "obstacle_1" , move_pattern="vertical" ))

        # 道具
        self.items.add(Item(360, 330, "kunge"))

        # 终点
        self.goal = Goal(750, 500)

    # 第三关布局
    def setup_level_3(self):
        self.time_limit = 20
        self.level_description = "时间限制缩短，注意控制好时间。"

        # 地面
        self.platforms.add(Platform(0, 550, 800, 50, "platform_2"))

        # 平台
        self.platforms.add(Platform(100, 450, 100, 20, "platform_1"))
        self.platforms.add(Platform(250, 330, 100, 20, "platform_1"))
        self.platforms.add(Platform(100, 210, 100, 20, "platform_1"))
        self.platforms.add(Platform(250,  90, 100, 20, "platform_1"))
        self.platforms.add(Platform(370, 450, 100, 20, "platform_1"))
        self.platforms.add(Platform(530, 350, 100, 20, "platform_1"))
        self.platforms.add(Platform(700, 300, 100, 20, "platform_1"))

        # 墙壁
        self.platforms.add(Platform(350,  90, 20, 460, "platform_2"))

        # 金币
        self.coins.add(Coin(140, 410))
        self.coins.add(Coin(290, 290))
        self.coins.add(Coin(140, 170))
        self.coins.add(Coin(290,  60))
        self.coins.add(Coin(410, 410))
        self.coins.add(Coin(570, 310))


        # 道具
        self.items.add(Item(410, 500, "kunge"))
        self.items.add(Item(700, 500, "card"))

        # 终点
        self.goal = Goal(750, 250)

    # 第四关布局
    def setup_level_4(self):
        self.time_limit = 30
        self.level_description = ""

        # 地面
        self.platforms.add(Platform(0, 550, 800, 50, "platform_2"))

        # 平台
        self.platforms.add(Platform(100, 450, 100, 20, "platform_1"))
        self.platforms.add(Platform(300, 400, 100, 20, "platform_1"))
        self.platforms.add(Platform(500, 350, 100, 20, "platform_1"))
        self.platforms.add(Platform(700, 300, 100, 20, "platform_1"))
        self.platforms.add(Platform(300, 250, 100, 20, "platform_1"))

        # 墙壁
        self.platforms.add(Platform(200, 300, 20, 100, "platform_1"))
        self.platforms.add(Platform(400, 350, 20, 80, "platform_1"))
        self.platforms.add(Platform(600, 300, 20, 100, "platform_1"))
        self.platforms.add(Platform(400, 200, 20, 100, "platform_1"))

        # 金币
        self.coins.add(Coin(140, 430))
        self.coins.add(Coin(340, 380))
        self.coins.add(Coin(540, 330))
        self.coins.add(Coin(740, 280))
        self.coins.add(Coin(340, 230))

        # 障碍物
        self.obstacles.add(Obstacle(250, 260, "obstacle_1", move_pattern="vertical"))
        self.obstacles.add(Obstacle(500, 510, "obstacle_2"))
        self.obstacles.add(Obstacle(650, 300, "obstacle_1"))
        self.obstacles.add(Obstacle(450, 200, "obstacle_1"))

        # 道具
        self.items.add(Item(420, 370, "kunge"))
        self.items.add(Item(320, 270, "kunge"))
        self.items.add(Item(600, 500, "card"))

        # 终点
        self.goal = Goal(750, 200)

    # 第五关布局
    def setup_level_5(self):
        self.time_limit = 90
        self.level_description = "无敌道具可以收集到险处的金币"

        # 地面
        self.platforms.add(Platform(0, 550, 800, 50, "platform_2"))

        # 平台
        self.platforms.add(Platform(100, 450, 100, 20, "platform_1"))
        self.platforms.add(Platform(300, 400, 100, 20, "platform_1"))
        self.platforms.add(Platform(500, 350, 100, 20, "platform_1"))
        self.platforms.add(Platform(700, 300, 100, 20, "platform_1"))
        self.platforms.add(Platform(300, 250, 100, 20, "platform_1"))
        self.platforms.add(Platform(500, 200, 100, 20, "platform_1"))

        # 墙壁
        self.platforms.add(Platform(200, 300, 20, 100, "platform_1"))
        self.platforms.add(Platform(400, 350, 20, 80, "platform_1"))
        self.platforms.add(Platform(600, 300, 20, 100, "platform_1"))
        self.platforms.add(Platform(400, 200, 20, 100, "platform_1"))
        self.platforms.add(Platform(600, 150, 20, 100, "platform_1"))

        # 金币
        self.coins.add(Coin(140, 430))
        self.coins.add(Coin(340, 380))
        self.coins.add(Coin(540, 330))
        self.coins.add(Coin(740, 280))
        self.coins.add(Coin(340, 230))
        self.coins.add(Coin(540, 180))

        # 障碍物
        self.obstacles.add(Obstacle(250, 300, "obstacle_1"))
        self.obstacles.add(Obstacle(450, 350, "obstacle_2"))
        self.obstacles.add(Obstacle(650, 300, "obstacle_1"))
        self.obstacles.add(Obstacle(450, 200, "obstacle_2"))
        self.obstacles.add(Obstacle(640, 160, "obstacle_1"))

        # 道具
        self.items.add(Item(320, 270, "invincible"))

        # 终点
        self.goal = Goal(750, 150)

    # 第六关布局
    def setup_level_6(self):
        self.time_limit = 80
        self.level_description = "高空跳跃，精确控制落点"

        # 地面很少
        self.platforms.add(Platform(0, 550, 100, 50, "platform_2"))
        self.platforms.add(Platform(700, 550, 100, 50, "platform_2"))

        # 高空平台 
        self.platforms.add(Platform(100, 450, 60, 20, "platform_1"))
        self.platforms.add(Platform(200, 350, 60, 20, "platform_1"))
        self.platforms.add(Platform(300, 250, 60, 20, "platform_1"))
        self.platforms.add(Platform(400, 350, 60, 20, "platform_1"))
        self.platforms.add(Platform(500, 250, 60, 20, "platform_1"))
        self.platforms.add(Platform(600, 350, 60, 20, "platform_1"))
        self.platforms.add(Platform(700, 450, 60, 20, "platform_1"))

        # 金币 
        self.coins.add(Coin(130, 420))
        self.coins.add(Coin(230, 320))
        self.coins.add(Coin(330, 220))
        self.coins.add(Coin(430, 320))
        self.coins.add(Coin(530, 220))
        self.coins.add(Coin(630, 320))
        self.coins.add(Coin(730, 420))

        # 移动障碍 
        self.obstacles.add(Obstacle(150, 300, "obstacle_1", move_pattern="vertical"))
        self.obstacles.add(Obstacle(350, 200, "obstacle_1", move_pattern="horizontal"))
        self.obstacles.add(Obstacle(550, 200, "obstacle_1", move_pattern="vertical"))

        # 道具
        self.items.add(Item(400, 150, "invincible")) 
        self.items.add(Item(650, 500, "card")) 

        # 终点
        self.goal = Goal(730, 400)
 
    # 第七关布局
    def setup_level_7(self):
        self.time_limit = 80
        self.level_description = ""

        # 地面
        self.platforms.add(Platform(0, 550, 400, 50, "platform_2"))

        # 平台
        self.platforms.add(Platform(100, 450, 100, 20, "platform_1"))
        self.platforms.add(Platform(280, 370, 100, 20, "platform_1"))       
        self.platforms.add(Platform(280, 100, 100, 20, "platform_1"))
        self.platforms.add(Platform( 80, 160,  80, 20, "platform_1"))
        self.platforms.add(Platform(440, 400, 80, 20, "platform_1"))
        self.platforms.add(Platform(460, 200, 80, 20, "platform_1"))
        self.platforms.add(Platform(660, 180, 80, 20, "platform_1"))
        self.platforms.add(Platform(560, 300, 80, 20, "platform_1"))
        self.platforms.add(Platform(560, 500, 80, 20, "platform_1"))
        self.platforms.add(Platform(680, 550, 100, 20, "platform_1"))
        self.platforms.add(Platform(650, 400, 150, 20, "platform_1"))

        # 墙壁
        self.platforms.add(Platform(380, 100, 20, 450, "platform_2"))
        self.platforms.add(Platform(180, 260, 20, 80 , "platform_1"))

        # 金币
        self.coins.add(Coin(140, 410))
        self.coins.add(Coin(480, 350))
        self.coins.add(Coin(500, 120))
        self.coins.add(Coin(720, 280))
        self.coins.add(Coin(320, 270))

        # 障碍物
        self.obstacles.add(Obstacle(150, 300, "obstacle_1",move_pattern="horizontal"))
        self.obstacles.add(Obstacle(630, 20, "obstacle_1",move_pattern="vertical"))

        # 道具     
        self.items.add(Item(680, 120, "card"))

        # 终点
        self.goal = Goal(720, 500)

    # 第八关布局
    def setup_level_8(self):
        self.time_limit = 70
        self.level_description = ""

        # 地面
        self.platforms.add(Platform(0, 550, 620, 50, "platform_2"))
        self.platforms.add(Platform(670, 550, 130, 50, "platform_2"))

        # 平台
        self.platforms.add(Platform(100, 450, 100, 20, "platform_1"))
        self.platforms.add(Platform(300, 400, 100, 20, "platform_1"))
        self.platforms.add(Platform(500, 350, 100, 20, "platform_1"))
        self.platforms.add(Platform(700, 300, 100, 20, "platform_1"))
        self.platforms.add(Platform(300, 250, 100, 20, "platform_1"))
        self.platforms.add(Platform(500, 200, 100, 20, "platform_1"))
        self.platforms.add(Platform(700, 150, 100, 20, "platform_1"))

        # 墙壁
        self.platforms.add(Platform(200, 300, 20, 100, "platform_1"))
        self.platforms.add(Platform(400, 350, 20, 80, "platform_1"))
        self.platforms.add(Platform(600, 300, 20, 100, "platform_1"))
        self.platforms.add(Platform(400, 200, 20, 100, "platform_1"))
        self.platforms.add(Platform(600, 150, 20, 100, "platform_1"))
        self.platforms.add(Platform(800, 100, 20, 100, "platform_1"))

        # 金币
        self.coins.add(Coin(140, 410))
        self.coins.add(Coin(340, 360))
        self.coins.add(Coin(540, 300))
        self.coins.add(Coin(740, 250))
        self.coins.add(Coin(340, 210))

        # 障碍物
        self.obstacles.add(Obstacle(250, 300, "obstacle_1"))
        self.obstacles.add(Obstacle(450, 350, "obstacle_1"))
        self.obstacles.add(Obstacle(650, 300, "obstacle_1"))
        self.obstacles.add(Obstacle(450, 200, "obstacle_1"))
        self.obstacles.add(Obstacle(650, 150, "obstacle_1"))

        # 道具
        self.items.add(Item(320, 270, "invincible"))
        self.items.add(Item(520, 220, "kunge"))
        self.items.add(Item(720, 190, "card"))
        self.items.add(Item(520, 120, "invincible"))

        # 终点
        self.goal = Goal(720, 80)

    # 第九关布局
    def setup_level_9(self):
        self.time_limit = 90
        self.level_description = "最终挑战！精确跳跃和快速反应"

        # 地面
        self.platforms.add(Platform(0, 550, 100, 50, "platform_2"))
        self.platforms.add(Platform(700, 550, 100, 50, "platform_2"))

        # 平台
        self.platforms.add(Platform(150, 500, 60, 20, "platform_1"))
        self.platforms.add(Platform(250, 450, 60, 20, "platform_1"))
        self.platforms.add(Platform(350, 400, 60, 20, "platform_1"))
        self.platforms.add(Platform(450, 350, 40, 15, "platform_1"))
        self.platforms.add(Platform(550, 300, 40, 15, "platform_1"))
        self.platforms.add(Platform(650, 250, 40, 15, "platform_1"))
        self.platforms.add(Platform(450, 200, 50, 20, "platform_1"))
        self.platforms.add(Platform(350, 150, 60, 20, "platform_1"))
        self.platforms.add(Platform(250, 100, 60, 20, "platform_1"))
        self.platforms.add(Platform(150, 50, 60, 20, "platform_1"))
        self.platforms.add(Platform(560, 150, 60, 20, "platform_1"))
        self.platforms.add(Platform(650, 100, 60, 20, "platform_1"))

        # 金币
        self.coins.add(Coin(180, 470))
        self.coins.add(Coin(280, 420))
        self.coins.add(Coin(380, 370))
        
        self.coins.add(Coin(470, 320))
        self.coins.add(Coin(570, 270))
        
        self.coins.add(Coin(480, 170))
        self.coins.add(Coin(380, 120))
        self.coins.add(Coin(280, 70))
        self.coins.add(Coin(180, 20))
        
        self.coins.add(Coin(580, 120))
        self.coins.add(Coin(680, 70))

        # 障碍物
        self.obstacles.add(Obstacle(300, 370, "obstacle_1", move_pattern="horizontal"))
        self.obstacles.add(Obstacle(510, 270, "obstacle_1", move_pattern="vertical"))
        self.obstacles.add(Obstacle(400, 170, "obstacle_1", move_pattern="horizontal"))
        self.obstacles.add(Obstacle(600, 70, "obstacle_1", move_pattern="vertical"))

        # 道具
        self.items.add(Item(730, 30, "card"))

        # 终点
        self.goal = Goal(700, 500)


        