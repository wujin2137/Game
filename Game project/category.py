import pygame
import json
import os
from typing import List, Dict, Tuple, Optional

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
    #皮肤数据
    SKIN_PATHS = {
        "default": "resource/image/skins/default.png",
        "皮肤1": "resource/image/skins/skin_1.png",
        "皮肤2": "resource/image/skins/skin_2.png",
        "皮肤3": "resource/image/skins/skin_3.png",
        # 可以继续添加更多皮肤
    }

    #初始化玩家角色
    def __init__(self, x: int, y: int, skin_name: str = "default"):
        super().__init__()
        self.height = 50  # 预设高度
        self.speed = 5  # 默认速度
        self.speed_up_timer = 0  # 加速计时器
        self.skin_name = skin_name
        self.facing_right = True
        
        # 尝试加载皮肤图片
        self.image, self.width = self._load_skin(skin_name)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.jump_strength = -15
        self.gravity = 0.68
        self.on_ground = False

    #加载皮肤
    def _load_skin(self, skin_name):
        """加载皮肤并按原始比例调整尺寸"""
        try:
            # 尝试加载指定皮肤
            skin_path = self.SKIN_PATHS.get(skin_name, self.SKIN_PATHS["default"])
            original_image = pygame.image.load(skin_path).convert_alpha()
        except:
            try:
                # 指定皮肤加载失败，尝试加载默认皮肤
                original_image = pygame.image.load(self.SKIN_PATHS["default"]).convert_alpha()
            except:
                # 默认皮肤也加载失败，创建纯色矩形
                original_image = pygame.Surface((30, self.height))
                original_image.fill((255, 100, 100))  # 默认颜色
                return original_image, 30
        
        # 获取原始图像宽高比
        original_width, original_height = original_image.get_size()
        if original_height == 0:  # 防止除零错误
            ratio = 1
        else:
            ratio = original_width / original_height
            
        # 根据比例和预设高度计算新宽度
        new_width = int(self.height * ratio)
        
        # 缩放图像
        scaled_image = pygame.transform.scale(original_image, (new_width, self.height))
        
        return scaled_image, new_width

    #更新玩家状态
    def update(self, platforms: pygame.sprite.Group, coins: pygame.sprite.Group):
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
                self.speed = 5  # 恢复默认速度

    #检测与平台的碰撞
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

    #执行跳跃
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_strength

    #向左移动
    def move_left(self):
        self.vel_x = -self.speed
        self.facing_right = False

    #向右移动
    def move_right(self):
        self.vel_x = self.speed
        self.facing_right = True

    #停止水平移动
    def stop(self):
        self.vel_x = 0

    #应用道具
    def apply_item_effect(self, item):
        if item.item_type == "speed_up":
            self.speed = 10  # 加速（翻倍）
            self.speed_up_timer = 300  # 5 秒（60 帧/秒）
            item.kill()  # 移除道具

# 平台类，在此处设置平台图片
class Platform(pygame.sprite.Sprite):
    # 定义不同类型平台对应的图标路径
    PLATFORM_TYPES = {
        "platform_1": "resource/image/platform/platform_1.png",
        "platform_2": "resource/image/platform/platform_2.png",
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
    COIN_ICON_PATH = "resource/image/icons/coin.png"

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
        "obstacle_1": "resource/image/icons/obstacle_1.png",
        "obstacle_2": "resource/image/icons/obstacle_2.png",
        # 可以根据需要添加更多类型
    }
    
    # 定义障碍物的最大尺寸
    MAX_WIDTH = 40
    MAX_HEIGHT = 40

    #初始化
    def __init__(self, x: int, y: int, obstacle_type: str):
        super().__init__()
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
        self.obstacle_type = obstacle_type

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
        "speed_up": "resource/image/icons/speed_up.png",
        # 可以根据需要添加更多类型
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
            original_image = pygame.image.load("resource/image/icons/goal.png").convert_alpha()
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
            with open("saves/game_data.json", "r") as file:
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
        with open("saves/game_data.json", "w") as file:
            json.dump(data, file)

    #计算关卡得分
    def calculate_score(self, level: int, coins_collected: int, time_taken: float) -> int:
        # 基础分数算法：金币数量乘以系数，再根据时间调整
        base_score = coins_collected * 300
        time_bonus = max(0, (300 - time_taken) / 300)  # 300秒是基准时间
        return int(base_score * (2 + time_bonus))

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