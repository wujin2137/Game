import pygame
import json
import os
import sys
from typing import List, Dict, Tuple, Optional

# 定义 resource_path 函数
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 玩家类，在此处设置皮肤路径
class Player(pygame.sprite.Sprite):
    # 皮肤数据
    SKIN_PATHS = {
        "default": {
            "idle": resource_path("resource/image/skins/default_idle.png"),
            "move": resource_path("resource/image/skins/default_move.png")
        },
        "皮肤1": {
            "idle": resource_path("resource/image/skins/skin_1_idle.png"),
            "move": resource_path("resource/image/skins/skin_1_move.png")
        },
        "皮肤2": {
            "idle": resource_path("resource/image/skins/skin_2_idle.png"),
            "move": resource_path("resource/image/skins/skin_2_move.png")
        },
        "皮肤3": {
            "idle": resource_path("resource/image/skins/skin_3_idle.png"),
            "move": resource_path("resource/image/skins/skin_3_move.png")  # 修改为单个图片路径
        },
    }

    # 初始化玩家角色
    def __init__(self, x: int, y: int, skin_name: str = "default"):
        super().__init__()
        self.height = 50                # 预设高度
        self.speed = 4                  # 默认速度
        self.speed_up_timer = 0         # 加速计时器
        self.skin_name = skin_name
        self.facing_right = True
        self.move_frame = 0             # 移动帧索引
        self.move_animation_speed = 10  # 移动动画速度
        self.invincible = False         # 无敌状态
        self.invincible_timer = 0       # 无敌计时器
        self.freeze_timer = 0           # 冻结计时器
        self.freeze_duration = 0        # 冻结总时长
        self.visible = True      
        self.has_card = False

        # 尝试加载皮肤图片
        self.idle_image, self.move_images, self.width = self._load_skin(skin_name)
        self.image = self.idle_image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.jump_strength = -15
        self.gravity = 0.68
        self.on_ground = False

    # 加载皮肤
    def _load_skin(self, skin_name):
        """加载皮肤并按原始比例调整尺寸"""
        skin_data = self.SKIN_PATHS.get(skin_name, self.SKIN_PATHS["default"])

        # 加载静止图片
        try:
            idle_image = pygame.image.load(skin_data["idle"]).convert_alpha()
        except:
            try:
                default_idle = pygame.image.load(self.SKIN_PATHS["default"]["idle"]).convert_alpha()
                original_width, original_height = default_idle.get_size()
                if original_height == 0:  # 防止除零错误
                    ratio = 1
                else:
                    ratio = original_width / original_height
                new_width = int(self.height * ratio)
                idle_image = pygame.Surface((new_width, self.height))
                idle_image.fill((255, 100, 100))  # 默认颜色
            except:
                idle_image = pygame.Surface((30, self.height))
                idle_image.fill((255, 100, 100))  # 默认颜色

        # 加载移动图片
        move_images = []
        try:
            move_image = pygame.image.load(skin_data["move"]).convert_alpha()
            original_width, original_height = move_image.get_size()
            if original_height == 0:  # 防止除零错误
                ratio = 1
            else:
                ratio = original_width / original_height
            new_width = int(self.height * ratio)
            scaled_move_image = pygame.transform.scale(move_image, (new_width, self.height))
            move_images.append(scaled_move_image)
        except:
            try:
                default_move = pygame.image.load(self.SKIN_PATHS["default"]["move"]).convert_alpha()
                original_width, original_height = default_move.get_size()
                if original_height == 0:  # 防止除零错误
                    ratio = 1
                else:
                    ratio = original_width / original_height
                new_width = int(self.height * ratio)
                move_image = pygame.Surface((new_width, self.height))
                move_image.fill((255, 100, 100))  # 默认颜色
                move_images.append(move_image)
            except:
                move_image = pygame.Surface((30, self.height))
                move_image.fill((255, 100, 100))  # 默认颜色
                move_images.append(move_image)

        # 获取原始图像宽高比
        original_width, original_height = idle_image.get_size()
        if original_height == 0:  # 防止除零错误
            ratio = 1
        else:
            ratio = original_width / original_height

        # 根据比例和预设高度计算新宽度
        new_width = int(self.height * ratio)

        # 缩放静止图像
        idle_image = pygame.transform.scale(idle_image, (new_width, self.height))

        return idle_image, move_images, new_width

    # 更新玩家状态
    def update(self, platforms: pygame.sprite.Group, coins: pygame.sprite.Group):
        # 处理冻结计时器
        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            if self.freeze_timer == 0:
                self.freeze_duration = 0  # 重置冻结总时长        

        # 只有在非冻结状态下才处理移动
        if self.freeze_timer <= 0:
            # 应用重力
            self.vel_y += self.gravity
            if self.vel_y > 20:  # 限制最大下落速度
                self.vel_y = 20

            # 移动并检测平台碰撞
            self.rect.x += self.vel_x
            self.check_collision(self.vel_x, 0, platforms)

            self.rect.y += self.vel_y
            self.on_ground = False
            self.check_collision(0, self.vel_y, platforms)

        # 检测金币碰撞
        pygame.sprite.spritecollide(self, coins, True)

        # 处理加速计时器
        if self.speed_up_timer > 0:
            self.speed_up_timer -= 1
            if self.speed_up_timer == 0:
                self.speed = 4  # 恢复默认速度

        # 处理无敌计时器
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0:
                self.invincible = False  # 取消无敌状态

        # 更新动画
        self.update_animation()

    # 更新动画
    def update_animation(self):
        if self.vel_x != 0:
            # 移动状态
            if len(self.move_images) > 1:
                # 有多个移动帧，播放动画
                self.move_frame = (self.move_frame + 1) % (len(self.move_images) * self.move_animation_speed)
                frame_index = self.move_frame // self.move_animation_speed
                self.image = self.move_images[frame_index]
            else:
                # 只有一个移动帧，显示移动图片
                self.image = self.move_images[0]

            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            # 静止状态
            self.image = self.idle_image
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

        # 无敌特效展示：闪烁
        if self.invincible and self.invincible_timer % 10 < 5:
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)

    # 检测与平台的碰撞
    def check_collision(self, vel_x: int, vel_y: int, platforms: pygame.sprite.Group):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if vel_x > 0:  # 向右移动
                    self.rect.right = platform.rect.left
                    self.vel_x = 0
                if vel_x < 0:  # 向左移动
                    self.rect.left = platform.rect.right
                    self.vel_x = 0
                if vel_y > 0:  # 向下移动
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                if vel_y < 0:  # 向上移动
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

    # 执行跳跃
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_strength

    # 向左移动
    def move_left(self):
        self.vel_x = -self.speed
        self.facing_right = False

    # 向右移动
    def move_right(self):
        self.vel_x = self.speed
        self.facing_right = True

    # 停止水平移动
    def stop(self):
        self.vel_x = 0

    # 应用道具
    def apply_item_effect(self, item):
        if item.item_type == "speed_up":
            self.speed = 8  # 加速
            self.speed_up_timer = 300  # 5 秒（60 帧/秒）
            item.kill()
        elif item.item_type == "invincible":
            self.invincible = True
            self.invincible_timer = 300  # 5 秒（60 帧/秒）
            item.kill()
        elif item.item_type == "kunge":
            kunge_sound = pygame.mixer.Sound(resource_path("resource/sound/ji.mp3"))
            kunge_sound.play()
            item.kill()
        elif item.item_type == "canteen":  
            self.freeze_timer = 300  # 5秒 (60帧/秒)
            self.freeze_duration = 300
            item.kill()
        elif item.item_type == "card":  # 新增校卡效果
            self.has_card = True
            item.kill()

# 技能动画精灵类
class SkillAnimation(pygame.sprite.Sprite):
    def __init__(self, frames, player_rect):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=player_rect.center)
        self.animation_speed = 3  # 动画速度，数值越小越快
        self.animation_timer = 0
        
    def update(self, player_rect, direction):
        # 更新动画帧
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            
            # 确保动画方向与玩家一致
            if direction != (self.rect.width > 0):  # 检查图像是否已翻转
                self.image = pygame.transform.flip(self.image, True, False)
        
        # 跟随玩家位置
        self.rect.center = player_rect.center

# 平台类，在此处设置平台图片
class Platform(pygame.sprite.Sprite):
    # 定义不同类型平台对应的图标路径
    PLATFORM_TYPES = {
        "platform_1": resource_path("resource/image/platform/platform_1.png"),
        "platform_2": resource_path("resource/image/platform/platform_2.png"),
        # 可以根据需要添加更多类型
    }

    #初始化
    def __init__(self, x: int, y: int, width: int, height: int, platform_type: str = None, color: Tuple[int, int, int] = (0, 200, 0)):
        super().__init__()
        try:
            # 根据平台类型加载对应的图标
            if platform_type:
                icon_path = self.PLATFORM_TYPES.get(platform_type)
                if icon_path:
                    original_image = pygame.image.load(icon_path).convert_alpha()
                    self.image = pygame.transform.smoothscale(original_image, (width, height))  # 设置图片尺寸
                else:
                    # 如果类型不存在，使用默认的简单图形
                    self.image = pygame.Surface((width, height))
                    self.image.fill(color)
            else:
                # 如果未指定类型，使用默认的简单图形
                self.image = pygame.Surface((width, height))
                self.image.fill(color)
        except FileNotFoundError:
            # 如果图片不存在，绘制一个简单图形
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 金币类
class Coin(pygame.sprite.Sprite):
    # 定义金币图标的路径
    COIN_ICON_PATH = resource_path("resource/image/icons/coin.png")

    #初始化
    def __init__(self, x: int, y: int):
        super().__init__()
        try:
            # 尝试加载金币图标
            original_image = pygame.image.load(self.COIN_ICON_PATH).convert_alpha()
            self.image = pygame.transform.smoothscale(original_image, (15, 15))  # 设置图片尺寸15*15
        except FileNotFoundError:
            # 如果图片不存在，绘制一个15*15的简单图形
            self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 215, 0), (7, 7), 7)
            pygame.draw.circle(self.image, (255, 215, 0), (7, 7), 5)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 障碍物类，在此处设置障碍物图标
class Obstacle(pygame.sprite.Sprite):
    # 定义不同类型障碍物对应的图标路径
    OBSTACLE_TYPES = {
        "obstacle_1": resource_path("resource/image/obstacle/obstacle_1.png"),
        "obstacle_2": resource_path("resource/image/obstacle/obstacle_2.png"),
    }
    
    # 定义障碍物的最大尺寸
    MAX_WIDTH = 40
    MAX_HEIGHT = 40

    def __init__(self, x: int, y: int, obstacle_type: str, move_pattern=None):
        super().__init__()
        self.obstacle_type = obstacle_type
        self.move_pattern = move_pattern  # 移动模式: None(固定), "horizontal"(水平), "vertical"(垂直)
        self.move_speed = 2  # 移动速度
        self.move_distance = 100  # 移动距离
        self.move_counter = 0  # 移动计数器
        self.move_direction = 1  # 移动方向: 1(右/下), -1(左/上)
        
        try:
            # 根据障碍物类型加载对应的图标
            icon_path = self.OBSTACLE_TYPES.get(obstacle_type)
            if icon_path:
                original_image = pygame.image.load(icon_path).convert_alpha()
                self.image = self._scale_with_aspect_ratio(original_image)
            else:
                # 如果类型不存在，使用默认的简单图形
                self.image = self._create_default_icon()
        except FileNotFoundError:
            # 如果图片不存在，绘制一个默认图标
            self.image = self._create_default_icon()
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x  # 原始x坐标
        self.original_y = y  # 原始y坐标

    def update(self):
        """更新障碍物位置（如果设置了移动模式）"""
        if self.move_pattern == "horizontal":
            # 水平移动
            self.rect.x += self.move_speed * self.move_direction
            self.move_counter += self.move_speed
            
            if abs(self.move_counter) >= self.move_distance:
                self.move_direction *= -1  # 反向移动
                self.move_counter = 0
                
        elif self.move_pattern == "vertical":
            # 垂直移动
            self.rect.y += self.move_speed * self.move_direction
            self.move_counter += self.move_speed
            
            if abs(self.move_counter) >= self.move_distance:
                self.move_direction *= -1  # 反向移动
                self.move_counter = 0

    # 其他方法保持不变...
    def _scale_with_aspect_ratio(self, image):
        """按原始比例缩放图像，使其适应最大尺寸"""
        original_width, original_height = image.get_size()
        
        # 计算宽高比
        ratio = min(self.MAX_WIDTH / original_width, self.MAX_HEIGHT / original_height)
        
        # 根据比例计算新尺寸
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # 缩放图像
        return pygame.transform.smoothscale(image, (new_width, new_height))

    def _create_default_icon(self):
        """创建默认图标（绿色矩形带边框）"""
        surface = pygame.Surface((self.MAX_WIDTH, self.MAX_HEIGHT), pygame.SRCALPHA)
        surface.fill(GREEN)
        pygame.draw.rect(surface, (0, 150, 0), (5, 5, 30, 30))
        pygame.draw.rect(surface, WHITE, (10, 10, 20, 20), 2)
        return surface

# 道具类，在此处设置道具图标
class Item(pygame.sprite.Sprite):
    # 定义不同类型道具对应的图标路径
    ITEM_TYPES = {
        "speed_up": resource_path("resource/image/item/speed_up.png"),
        "kunge" : resource_path("resource/image/item/kunge.png"),
        "invincible" : resource_path("resource/image/item/invincible.png"),
        "canteen" : resource_path("resource/image/item/canteen.png"),
        "card": resource_path("resource/image/item/card.png")  
    }
    
    # 定义道具的最大尺寸
    MAX_WIDTH = 40
    MAX_HEIGHT = 40

    #初始化
    def __init__(self, x: int, y: int, item_type: str):
        super().__init__()
        try:
            # 根据道具类型加载对应的图标
            icon_path = self.ITEM_TYPES.get(item_type)
            if icon_path:
                original_image = pygame.image.load(icon_path).convert_alpha()
                self.image = self._scale_with_aspect_ratio(original_image)
            else:
                # 如果类型不存在，使用默认的简单图形
                self.image = self._create_default_icon()
        except FileNotFoundError:
            # 如果图片不存在，绘制一个默认图标
            self.image = self._create_default_icon()
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.item_type = item_type

    #按原始比例缩放图像           
    def _scale_with_aspect_ratio(self, image):
        """按原始比例缩放图像，使其适应最大尺寸"""
        original_width, original_height = image.get_size()
        
        # 计算宽高比
        ratio = min(self.MAX_WIDTH / original_width, self.MAX_HEIGHT / original_height)
        
        # 根据比例计算新尺寸
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # 缩放图像
        return pygame.transform.smoothscale(image, (new_width, new_height))

    #创建默认图标    
    def _create_default_icon(self):
        """创建默认图标（黄色矩形带边框）"""
        surface = pygame.Surface((self.MAX_WIDTH, self.MAX_HEIGHT), pygame.SRCALPHA)
        surface.fill(YELLOW)
        pygame.draw.rect(surface, (200, 200, 0), (5, 5, 30, 30))
        pygame.draw.rect(surface, WHITE, (10, 10, 20, 20), 2)
        return surface

# 终点类，在此处设置终点图标
class Goal(pygame.sprite.Sprite):
    #初始化
    def __init__(self, x: int, y: int):
        super().__init__()
        try:
            # 加载自定义的终点图标
            original_image = pygame.image.load(resource_path("resource/image/icons/goal.png")).convert_alpha()
            self.image = pygame.transform.smoothscale(original_image, (40, 40)) #设置图片尺寸40*40
        except FileNotFoundError:
            # 如果图片不存在，绘制一个40*40的简单图形
            self.image = pygame.Surface((40, 40))
            self.image.fill(GREEN)
            pygame.draw.rect(self.image, (0, 150, 0), (5, 5, 30, 30))
            pygame.draw.rect(self.image, WHITE, (10, 10, 20, 20), 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 游戏状态类
class GameState:
    #初始化游戏状态
    def __init__(self):
        self.current_level = 0
        self.total_coins = 0
        self.total_score = 0
        self.unlocked_skins = ["default"]
        self.selected_skin = "default"
        self.level_stats = {}  # 存储每关的统计数据
        self.load_game_data()

    #从json文件加载游戏存档数据
    def load_game_data(self):
        try:
            with open(resource_path("saves/game_data.json"), "r") as file:
                data = json.load(file)
                self.current_level = data.get("current_level", 0)
                self.total_coins = data.get("total_coins", 0)
                self.total_score = data.get("total_score", 0)
                self.unlocked_skins = data.get("unlocked_skins", ["default"])
                self.selected_skin = data.get("selected_skin", "default")
                self.level_stats = data.get("level_stats", {})
        except (FileNotFoundError, json.JSONDecodeError):
            # 使用默认值
            pass

    #将当前游戏状态保存到json文件
    def save_game_data(self):
        data = {
            "current_level": self.current_level,
            "total_coins": self.total_coins,
            "total_score": self.total_score,
            "unlocked_skins": self.unlocked_skins,
            "selected_skin": self.selected_skin,
            "level_stats": self.level_stats
        }
        with open(resource_path("saves/game_data.json"), "w") as file:
            json.dump(data, file)

    #计算关卡得分
    def calculate_score(self, level: int, coins_collected: int, time_taken: float) -> int:
        # 基础分数算法：金币数量乘以系数，再根据时间调整
        base_score = coins_collected * 500
        time_bonus = max(0, (300 - time_taken) / 300)  # 300秒是基准时间
        return int(base_score * (3 + time_bonus))

    #更新关卡统计数据   level：关卡编号 coins_collected：收集的金币数量 time_taken通关时间
    def update_level_stats(self, level: int, coins_collected: int, time_taken: float):
        score = self.calculate_score(level, coins_collected, time_taken)

        # 如果这关之前已经完成过，比较分数
        if level in self.level_stats:
            prev_score = self.level_stats[level]["score"]
            if score > prev_score:
                self.level_stats[level] = {
                    "coins": coins_collected,
                    "time": time_taken,
                    "score": score
                }
                self.total_score += (score - prev_score)
        else:
            self.level_stats[level] = {
                "coins": coins_collected,
                "time": time_taken,
                "score": score
            }
            self.total_score += score
            self.total_coins += coins_collected

            # 检查是否解锁新皮肤
            if self.total_score >= 10000 and "皮肤1" not in self.unlocked_skins:
                self.unlocked_skins.append("皮肤1")
            if self.total_score >= 30000 and "皮肤2" not in self.unlocked_skins:
                self.unlocked_skins.append("皮肤2")
            if self.total_score >= 50000 and "皮肤3" not in self.unlocked_skins:
                self.unlocked_skins.append("皮肤3")

        self.save_game_data()