import pygame
import os
import sys
from category import Player, GameState, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE, YELLOW,SkillAnimation
from level import Level

# 定义 resource_path 函数
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Game:
    #初始化游戏类，设置游戏窗口、字体、游戏状态、设置主菜单背景图
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("跑酷闯关游戏")
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.running = True
        self.current_screen = "menu"
        self.bo=0
        # 确保皮肤目录存在
        if not os.path.exists(resource_path("resource/image/skins")):
            os.makedirs(resource_path("resource/image/skins"))

        # 加载字体
        try:
            # 加载自定义字体
            self.font = pygame.font.Font(resource_path("fonts/ARCADE_N.TTF"), 24)
            self.large_font = pygame.font.Font(resource_path("fonts/ARCADE_N.TTF"), 48)
        except FileNotFoundError:
            # 如果自定义字体不存在，尝试使用系统中可用的中文字体
            pygame.font.init()
            available_fonts = pygame.font.get_fonts()
            # 定义中文字体备选列表
            chinese_fonts = ["simhei", "microsoftyahei", "simsun", "heiti"]
            # 查找系统中可用的中文字体
            found_font = None
            for font_name in chinese_fonts:
                if font_name in available_fonts:
                    found_font = font_name
                    break

            if found_font:
                self.font = pygame.font.SysFont(found_font, 24)
                self.large_font = pygame.font.SysFont(found_font, 48)
            else:
                # 使用系统默认字体
                self.font = pygame.font.SysFont(None, 24)
                self.large_font = pygame.font.SysFont(None, 48)

        #加载菜单背景，保持原比例，填充空白，
        try:
            # 加载原始背景图
            original_bg = pygame.image.load(resource_path("resource/image/background/menu.webp")).convert()  #这边切换路径
            # 计算缩放比例（保持宽高比）
            bg_ratio = original_bg.get_width() / original_bg.get_height()
            screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT           
            if bg_ratio > screen_ratio:
                # 以高度为基准缩放
                new_height = SCREEN_HEIGHT
                new_width = int(new_height * bg_ratio)
            else:
                # 以宽度为基准缩放
                new_width = SCREEN_WIDTH
                new_height = int(new_width / bg_ratio)                
            # 缩放图片
            scaled_bg = pygame.transform.scale(original_bg, (new_width, new_height))
            # 居中裁剪
            x_offset = (new_width - SCREEN_WIDTH) // 2
            y_offset = (new_height - SCREEN_HEIGHT) // 2
            self.menu_background = scaled_bg.subsurface((x_offset, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("背景加载失败")
            self.menu_background = None

        # 确保保存数据的文件夹存在
        if not os.path.exists(resource_path("saves")):
            os.makedirs(resource_path("saves"))

    #游戏主循环
    def run(self):
        while self.running:
            if self.current_screen == "menu":
                self.menu_screen()
            elif self.current_screen == "game":
                self.game_screen()
            elif self.current_screen == "level_select":
                self.level_select_screen()
            elif self.current_screen == "skins":
                self.skins_screen()
            elif self.current_screen == "stats":
                self.stats_screen()
            elif self.current_screen == "game_over":
                self.game_over_screen()
            elif self.current_screen == "level_complete":
                self.level_complete_screen()

    #主菜单界面，显示游戏标题和选项按钮，背景图在init里设置
    def menu_screen(self):
        """主菜单界面"""
        while self.current_screen == "menu":
            self.screen.fill(BLACK)

            # 绘制背景
            if self.menu_background:
                self.screen.blit(self.menu_background, (0, 0))
            else:
                self.screen.fill(BLACK)  # 如果背景图加载失败，使用黑色背景                                    
                        
            # 绘制标题
            title_text = self.large_font.render("跑酷闯关游戏", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)
            
            # 绘制按钮
            button_width, button_height = 220, 60  
            button_radius = 12 
            buttons = [
                {"text": "开始游戏", "y": 220, "action": "level_select"},
                {"text": "选择皮肤", "y": 300, "action": "skins"},  # 调整按钮间距
                {"text": "游戏统计", "y": 380, "action": "stats"},
                {"text": "退出游戏", "y": 460, "action": "quit"}
            ]

            for button in buttons:
                button_x = (SCREEN_WIDTH - button_width) // 2
                button_y = button["y"]
                rect = pygame.Rect(button_x, button_y, button_width, button_height)
                
                # 按钮状态检测
                is_hovered = rect.collidepoint(pygame.mouse.get_pos())
                is_clicked = pygame.mouse.get_pressed()[0] and is_hovered
                
                # 根据按钮状态选择颜色
                if is_clicked:
                    button_color = (40, 110, 200)   # 点击时的深蓝色
                    text_color = (230, 230, 230)    # 点击时的文本颜色
                    border_color = (255, 255, 255)  # 点击时的边框颜色
                    shadow_color = (0, 0, 0, 0)     # 点击时不显示阴影
                elif is_hovered:
                    button_color = (70, 140, 240)   # 悬停时的亮蓝色
                    text_color = WHITE
                    border_color = (255, 255, 255)
                    shadow_color = (0, 0, 0, 60)    # 悬停时的半透明阴影
                else:
                    button_color = (50, 120, 220)   # 默认蓝色
                    text_color = WHITE
                    border_color = (220, 220, 220)
                    shadow_color = (0, 0, 0, 40)    # 默认半透明阴影
                
                # 绘制按钮阴影
                shadow_rect = pygame.Rect(button_x + 3, button_y + 3, button_width, button_height)
                pygame.draw.rect(self.screen, shadow_color, shadow_rect, border_radius=button_radius)
                
                # 绘制按钮主体
                pygame.draw.rect(self.screen, button_color, rect, border_radius=button_radius)
                
                # 绘制按钮边框
                pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=button_radius)
                
                # 绘制按钮文本
                text = self.font.render(button["text"], True, text_color)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
                
                # 检查点击
                if is_clicked:
                    pygame.time.delay(200)  # 防止重复点击
                    if button["action"] == "quit":
                        self.running = False
                        self.current_screen = None
                    else:
                        self.current_screen = button["action"]    

            # 显示总积分和金币
            stats_text = self.font.render(f"总积分: {self.game_state.total_score}   总金币: {self.game_state.total_coins}", True, WHITE)
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
            self.screen.blit(stats_text, stats_rect)

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.current_screen = None

    #关卡选择界面，显示可选的关卡和锁定状态，在这里面设置背景图
    def level_select_screen(self):
        """关卡选择界面 - 10关，每行5个，固定总背景图"""
        level_buttons = []
        for i in range(10):  # 10个关卡
            level_buttons.append({
                "hover": False,
                "scale": 1.0
            })
        
        # 加载背景图
        background = None
        try:
            original_bg = pygame.image.load(resource_path("resource/image/background/background4.webp")).convert()  # 背景图
            bg_ratio = original_bg.get_width() / original_bg.get_height()
            screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
            new_width = SCREEN_WIDTH if bg_ratio <= screen_ratio else int(SCREEN_HEIGHT * bg_ratio)
            new_height = SCREEN_HEIGHT if bg_ratio >= screen_ratio else int(SCREEN_WIDTH / bg_ratio)
            scaled_bg = pygame.transform.scale(original_bg, (new_width, new_height))
            x_offset = (new_width - SCREEN_WIDTH) // 2
            y_offset = (new_height - SCREEN_HEIGHT) // 2
            background = scaled_bg.subsurface((x_offset, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"加载背景图失败: {e}")
        
        star_img = None
        try:
            star_img = pygame.image.load(resource_path("resource/image/icons/star.png")).convert_alpha()
            star_img = pygame.transform.scale(star_img, (20, 20))
        except:
            pass
        
        lock_img = None
        try:
            lock_img = pygame.image.load(resource_path("resource/image/icons/lock.png")).convert_alpha()
            lock_img = pygame.transform.scale(lock_img, (50, 50))
        except:
            pass

        while self.current_screen == "level_select":
            self.screen.fill(BLACK)
            # 显示固定的总背景图
            if background:
                self.screen.blit(background, (0, 0))
            else:
                # 渐变背景
                for y in range(SCREEN_HEIGHT):
                    color = (0, 0, max(50, int(150 * y / SCREEN_HEIGHT)))
                    pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
            
            # 绘制标题
            title_text = self.large_font.render("选择关卡", True, WHITE)
            title_shadow = self.large_font.render("选择关卡", True, (100, 100, 100))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            self.screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
            self.screen.blit(title_text, title_rect)
            
            # 按钮布局：每行5个，共2行（0-4第一行，5-9第二行）
            button_size = 90
            margin = 20
            start_x = (SCREEN_WIDTH - (5 * button_size + 4 * margin)) // 2
            start_y = 160
            
            mouse_pos = pygame.mouse.get_pos()
            
            for level in range(10):
                row = level // 5 
                col = level % 5
                x = start_x + col * (button_size + margin)
                y = start_y + row * (button_size + margin)
                
                rect = pygame.Rect(x, y, button_size, button_size)
                
                # 更新悬停状态
                if level <= self.game_state.current_level:
                    level_buttons[level]["hover"] = rect.collidepoint(mouse_pos)
                else:
                    level_buttons[level]["hover"] = False
                
                # 平滑缩放动画
                target_scale = 1.1 if level_buttons[level]["hover"] else 1.0
                level_buttons[level]["scale"] = max(1.0, min(1.1, level_buttons[level]["scale"] + (target_scale - level_buttons[level]["scale"]) * 0.1))
                scale = level_buttons[level]["scale"]
                scaled_size = int(button_size * scale)
                scale_offset = (scaled_size - button_size) // 2
                
                if level <= self.game_state.current_level:
                    # 已解锁关卡绘制
                    button_color = (50, 150, 255) if level_buttons[level]["hover"] else (30, 100, 200)
                    border_color = (200, 200, 0) if level == self.game_state.current_level else (200, 200, 200)
                    
                    button_surf = pygame.Surface((scaled_size, scaled_size), pygame.SRCALPHA)
                    pygame.draw.rect(button_surf, (*button_color, 200), (0, 0, scaled_size, scaled_size), border_radius=15)
                    pygame.draw.rect(button_surf, border_color, (0, 0, scaled_size, scaled_size), width=3, border_radius=15)
                    self.screen.blit(button_surf, (x - scale_offset, y - scale_offset))
                    
                    # 关卡文字
                    level_text = self.large_font.render("教程关" if level == 0 else str(level), True, WHITE)
                    scaled_text = pygame.transform.scale(level_text, (int(level_text.get_width() * scale), int(level_text.get_height() * scale)))
                    text_rect = scaled_text.get_rect(center=(x + button_size // 2, y + button_size // 2 - 15))
                    self.screen.blit(scaled_text, text_rect)
                    
                    # 星级显示
                    if level in self.game_state.level_stats and star_img:
                        stars = min(3, self.game_state.level_stats[level]["score"] // 1000)
                        for s in range(stars):
                            star_x = x + button_size // 2 - 30 + s * 20
                            star_y = y + button_size // 2 + 15
                            self.screen.blit(star_img, (star_x, star_y))
                    
                    # 点击事件
                    if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
                        pygame.time.delay(100)
                        self.current_level = level
                        self.current_screen = "game"
                else:
                    # 未解锁关卡绘制
                    button_surf = pygame.Surface((button_size, button_size), pygame.SRCALPHA)
                    pygame.draw.rect(button_surf, (50, 50, 50, 200), (0, 0, button_size, button_size), border_radius=15)
                    pygame.draw.rect(button_surf, (100, 100, 100), (0, 0, button_size, button_size), width=2, border_radius=15)
                    self.screen.blit(button_surf, (x, y))
                    
                    # 锁图标
                    if lock_img:
                        lock_rect = lock_img.get_rect(center=(x + button_size // 2, y + button_size // 2))
                        self.screen.blit(lock_img, lock_rect)
                    else:
                        lock_text = self.font.render("🔒", True, WHITE)
                        lock_rect = lock_text.get_rect(center=(x + button_size // 2, y + button_size // 2))
                        self.screen.blit(lock_text, lock_rect)
                    
                    # 解锁提示
                    unlock_text = self.font.render(f"关卡{level + 1}", True, WHITE)
                    unlock_rect = unlock_text.get_rect(center=(x + button_size // 2, y + button_size + 15))
                    self.screen.blit(unlock_text, unlock_rect)
            
            # 返回按钮
            back_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 80, 150, 50)
            back_color = (200, 50, 50) if back_button.collidepoint(mouse_pos) else (150, 40, 40)
            for i in range(back_button.height):
                shade = max(0, min(255, back_color[0] + (i * 10 // back_button.height)))
                pygame.draw.rect(self.screen, (shade, back_color[1], back_color[2]), (back_button.x, back_button.y + i, back_button.width, 1))
            pygame.draw.rect(self.screen, (255, 255, 255), back_button, 2, border_radius=5)
            back_text = self.font.render("返回", True, WHITE)
            self.screen.blit(back_text, back_text.get_rect(center=back_button.center))
            
            if pygame.mouse.get_pressed()[0] and back_button.collidepoint(mouse_pos):
                pygame.time.delay(200)
                self.current_screen = "menu"
            
            pygame.display.flip()
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.current_screen = None   

    #皮肤选择界面，显示可用的皮肤和解锁条件，在这里面设置背景图
    def skins_screen(self):
        """皮肤选择界面"""
        
        # 加载背景图（保持原比例，填充空白）
        try:
            original_bg = pygame.image.load(resource_path("resource/image/background/background1.webp")).convert()
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
            background = scaled_bg.subsurface((x_offset, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            background = None

        # 皮肤文案解释
        skin_descriptions = {
            "default": "默认皮肤",
            "皮肤1": "无额外属性加成",
            "皮肤2": "无视路障",
            "皮肤3": "可释放技能"
        }

        skin_names = list(Player.SKIN_PATHS.keys())
        current_index = 0
        
        # 为每个皮肤创建预览图像
        skin_previews = {}
        for skin_name in skin_names:
            try:
                # 尝试加载静止图像作为预览
                skin_data = Player.SKIN_PATHS[skin_name]
                if isinstance(skin_data["idle"], str):
                    preview_image = pygame.image.load(resource_path(skin_data["idle"])).convert_alpha()
                else:
                    preview_image = pygame.image.load(resource_path(skin_data["idle"][0])).convert_alpha()
                skin_previews[skin_name] = preview_image
            except:
                # 如果加载失败，创建一个彩色矩形作为预览
                preview_image = pygame.Surface((120, 120))
                colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
                color_index = skin_names.index(skin_name) % len(colors)
                preview_image.fill(colors[color_index])
                skin_previews[skin_name] = preview_image

        button_width, button_height = 120, 120
        margin = 60 
        buttons_per_row = 2

        # 左右切换按钮
        left_button = pygame.Rect(30, SCREEN_HEIGHT // 2 - 30, 60, 60)
        right_button = pygame.Rect(SCREEN_WIDTH - 90, SCREEN_HEIGHT // 2 - 30, 60, 60)
        
        # 动画相关变量
        animation_frames = {}  # 存储每个皮肤的动画帧
        animation_index = 0    # 当前动画帧索引
        animation_speed = 10   # 动画速度（数值越小，速度越快）
        frame_counter = 0      # 帧计数器
        
        # 初始化动画帧
        for skin_name in skin_names:
            skin_data = Player.SKIN_PATHS[skin_name]
            frames = []
            
            # 检查移动资源是单张图片还是列表
            if isinstance(skin_data["move"], list):
                # 有多个移动帧，加载所有帧
                for path in skin_data["move"]:
                    try:
                        frame = pygame.image.load(resource_path(path)).convert_alpha()
                        frame = pygame.transform.scale(frame, (button_width - 20, button_height - 20))
                        frames.append(frame)
                    except:
                        pass  # 如果加载失败，跳过该帧
            
            if not frames:
                # 如果没有动画帧或加载失败，使用静止图像或默认图像
                try:
                    if isinstance(skin_data["idle"], str):
                        frame = pygame.image.load(resource_path(skin_data["idle"])).convert_alpha()
                    else:
                        frame = pygame.image.load(resource_path(skin_data["idle"][0])).convert_alpha()
                    frame = pygame.transform.scale(frame, (button_width - 20, button_height - 20))
                    frames.append(frame)
                except:
                    # 创建默认帧
                    frame = pygame.Surface((button_width - 20, button_height - 20))
                    frame.fill((255, 100, 100))
                    frames.append(frame)
            
            animation_frames[skin_name] = frames

        while self.current_screen == "skins":
            self.screen.fill(BLACK)
            if background:
                self.screen.blit(background, (0, 0))
            else:
                self.screen.fill(BLACK)

            # 绘制标题
            title_text = self.large_font.render("选择皮肤", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title_text, title_rect)

            # 绘制左右切换按钮
            pygame.draw.rect(self.screen, RED if left_button.collidepoint(pygame.mouse.get_pos()) else (200, 0, 0), left_button)
            pygame.draw.rect(self.screen, WHITE, left_button, 2)
            left_arrow = self.font.render("<", True, WHITE)
            left_arrow_rect = left_arrow.get_rect(center=left_button.center)
            self.screen.blit(left_arrow, left_arrow_rect)

            pygame.draw.rect(self.screen, RED if right_button.collidepoint(pygame.mouse.get_pos()) else (200, 0, 0), right_button)
            pygame.draw.rect(self.screen, WHITE, right_button, 2)
            right_arrow = self.font.render(">", True, WHITE)
            right_arrow_rect = right_arrow.get_rect(center=right_button.center)
            self.screen.blit(right_arrow, right_arrow_rect)

            # 更新动画帧
            frame_counter += 1
            if frame_counter >= animation_speed:
                frame_counter = 0
                animation_index = (animation_index + 1) % max(len(frames) for frames in animation_frames.values())

            # 绘制当前显示的两个皮肤
            start_x = (SCREEN_WIDTH - (buttons_per_row * button_width + (buttons_per_row - 1) * margin)) // 2
            start_y = 200

            for i in range(2):
                if current_index + i < len(skin_names):
                    skin_name = skin_names[current_index + i]
                    col = i
                    x = start_x + col * (button_width + margin)
                    y = start_y

                    rect = pygame.Rect(x, y, button_width, button_height)

                    # 检查皮肤是否已解锁
                    if skin_name in self.game_state.unlocked_skins:
                        # 绘制皮肤图片
                        try:
                            # 使用当前动画帧
                            frames = animation_frames[skin_name]
                            current_frame = frames[animation_index % len(frames)]
                            self.screen.blit(current_frame, (x + 10, y + 10))
                        except:
                            name_text = self.font.render(skin_name, True, WHITE)
                            name_rect = name_text.get_rect(center=rect.center)
                            self.screen.blit(name_text, name_rect)

                        # 鼠标悬停效果
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            hover_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                            hover_surface.fill((255, 255, 255, 30))
                            self.screen.blit(hover_surface, (x, y))

                        # 选中效果
                        if skin_name == self.game_state.selected_skin:
                            border_surface = pygame.Surface((button_width + 10, button_height + 10), pygame.SRCALPHA)
                            pygame.draw.rect(border_surface, (255, 255, 0, 150), (0, 0, button_width + 10, button_height + 10), 5, border_radius=10)
                            self.screen.blit(border_surface, (x - 5, y - 5))

                            check_mark = self.font.render("✓", True, YELLOW)
                            check_rect = check_mark.get_rect(topright=(x + button_width - 5, y + 5))
                            self.screen.blit(check_mark, check_rect)

                        # 皮肤名称
                        name_text = self.font.render(skin_name, True, WHITE)
                        name_rect = name_text.get_rect(center=(rect.centerx, y + button_height + 15))  # 微调位置
                        self.screen.blit(name_text, name_rect)

                        # 皮肤文案解释，分成两行显示，增加行间距
                        description = skin_descriptions.get(skin_name, "")
                        words = description.split()
                        line1 = " ".join(words[:len(words)//2])
                        line2 = " ".join(words[len(words)//2:])

                        description_text1 = self.font.render(line1, True, WHITE)
                        description_rect1 = description_text1.get_rect(center=(rect.centerx, y + button_height + 45))  # 增加间距
                        self.screen.blit(description_text1, description_rect1)

                        description_text2 = self.font.render(line2, True, WHITE)
                        description_rect2 = description_text2.get_rect(center=(rect.centerx, y + button_height + 70))  # 增加间距
                        self.screen.blit(description_text2, description_rect2)

                        # 检查点击
                        if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()):
                            pygame.time.delay(200)
                            self.game_state.selected_skin = skin_name
                            self.game_state.save_game_data()
                    else:
                        # 未解锁的皮肤
                        lock_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                        lock_surface.fill((0, 0, 0, 150))
                        self.screen.blit(lock_surface, (x, y))
                        pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)

                        # 显示解锁条件
                        if skin_name == "皮肤1":
                            required_score = 10000
                        elif skin_name == "皮肤2":
                            required_score = 30000
                        elif skin_name == "皮肤3":
                            required_score = 50000
                        else:
                            required_score = 0

                        lock_text = self.font.render(f"需要 {required_score} 积分", True, WHITE)
                        lock_rect = lock_text.get_rect(center=rect.center)
                        self.screen.blit(lock_text, lock_rect)

                        # 皮肤文案解释，分成两行显示，增加行间距
                        description = skin_descriptions.get(skin_name, "")
                        words = description.split()
                        line1 = " ".join(words[:len(words)//2])
                        line2 = " ".join(words[len(words)//2:])

                        description_text1 = self.font.render(line1, True, WHITE)
                        description_rect1 = description_text1.get_rect(center=(rect.centerx, y + button_height + 45))  # 增加间距
                        self.screen.blit(description_text1, description_rect1)

                        description_text2 = self.font.render(line2, True, WHITE)
                        description_rect2 = description_text2.get_rect(center=(rect.centerx, y + button_height + 70))  # 增加间距
                        self.screen.blit(description_text2, description_rect2)

            # 返回按钮
            back_button = pygame.Rect((SCREEN_WIDTH - 120) // 2, 520, 120, 40)
            color = RED if back_button.collidepoint(pygame.mouse.get_pos()) else (200, 0, 0)
            pygame.draw.rect(self.screen, color, back_button)
            pygame.draw.rect(self.screen, WHITE, back_button, 2)

            back_text = self.font.render("返回", True, WHITE)
            back_rect = back_text.get_rect(center=back_button.center)
            self.screen.blit(back_text, back_rect)

            if pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                pygame.time.delay(200)
                self.current_screen = "menu"

            # 显示当前积分
            score_text = self.font.render(f"当前积分: {self.game_state.total_score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 580))
            self.screen.blit(score_text, score_rect)

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.current_screen = None

                # 处理左右切换按钮点击事件
                if pygame.mouse.get_pressed()[0]:
                    if left_button.collidepoint(pygame.mouse.get_pos()) and current_index > 0:
                        pygame.time.delay(200)
                        current_index -= 2
                    elif right_button.collidepoint(pygame.mouse.get_pos()) and current_index + 2 < len(skin_names):
                        pygame.time.delay(200)
                        current_index += 2

    #游戏统计界面，显示游戏进度和成就，在这里面设置背景图
    def stats_screen(self):
        """游戏统计界面"""
        
        # 加载背景图（保持原比例，填充空白）
        try:
            original_bg = pygame.image.load(resource_path("resource/image/background/background3.webp")).convert()
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
            background = scaled_bg.subsurface((x_offset, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            background = None

        while self.current_screen == "stats":
            self.screen.fill(BLACK)
            if background:
                self.screen.blit(background, (0, 0))
            else:
                self.screen.fill(BLACK)

            # 绘制标题
            title_text = self.large_font.render("游戏统计", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title_text, title_rect)

            # 绘制总统计
            stats_y = 180
            total_texts = [
                f"总积分: {self.game_state.total_score}",
                f"总金币: {self.game_state.total_coins}",
                f"已解锁皮肤: {len(self.game_state.unlocked_skins)}/{len(Player.SKIN_PATHS)}"
            ]

            for text in total_texts:
                stats_surface = self.font.render(text, True, WHITE)
                self.screen.blit(stats_surface, (100, stats_y))
                stats_y += 40

            # 绘制关卡统计
            level_title = self.font.render("关卡统计:", True, WHITE)
            self.screen.blit(level_title, (100, stats_y + 20))

            stats_y += 60
            for level in range(len(self.game_state.level_stats)):
                if level in self.game_state.level_stats:
                    stats = self.game_state.level_stats[level]
                    level_text = f"关卡 {level + 1}: 金币 {stats['coins']}, 时间 {stats['time']:.1f}秒, 积分 {stats['score']}"
                else:
                    level_text = f"关卡 {level + 1}: 未完成"

                level_surface = self.font.render(level_text, True, WHITE)
                self.screen.blit(level_surface, (100, stats_y))
                stats_y += 40

            # 返回按钮
            back_button = pygame.Rect((SCREEN_WIDTH - 150) // 2, 500, 150, 50)
            color = RED if back_button.collidepoint(pygame.mouse.get_pos()) else (200, 0, 0)
            pygame.draw.rect(self.screen, color, back_button)
            pygame.draw.rect(self.screen, WHITE, back_button, 2)

            back_text = self.font.render("返回", True, WHITE)
            back_rect = back_text.get_rect(center=back_button.center)
            self.screen.blit(back_text, back_rect)

            if pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                pygame.time.delay(200)
                self.current_screen = "menu"

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.current_screen = None

    #游戏主界面，处理游戏逻辑和绘制，///创建精灵组、游戏循环在此///，背景图在level.py设置
    def game_screen(self):

        # 初始化变量
        card_message_timer = 0

        # 加载关卡
        level = Level(self.current_level)
        total_coins_in_level = len(level.coins)     # 关卡初始金币总数
        level_requires_card = False                 # 标记关卡是否需要校卡

        # 检查关卡是否需要校卡
        for item in level.items:
            if item.item_type == "card":
                level_requires_card = True
                break

        # 加载关卡背景
        level_background = level.load_background()

        # 创建玩家（使用选中的皮肤）
        player = Player(level.player_start_x, level.player_start_y, self.game_state.selected_skin)

        # 创建精灵组
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        all_sprites.add(level.platforms)
        all_sprites.add(level.coins)
        all_sprites.add(level.obstacles)
        if hasattr(level, 'items'):
            all_sprites.add(level.items)
        if level.goal:
            all_sprites.add(level.goal)

        # 游戏计时器
        start_time = pygame.time.get_ticks()
        game_time = 0
        coins_collected = 0

        # 新增玩法相关变量
        skill_image = None
        skill_available = True
        skill_start_time = 0
        skill_duration = 5000  # 技能持续时间（毫秒）
        skill_cooldown = 20000  # 技能冷却时间（毫秒）
        skill_rect = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 - 25, 50, 50)  # 技能图标位置
        
        # 技能动画精灵
        skill_animation = None
        
        # 玩家原始图像备份
        player_original_image = None
        
        # 加载技能资源
        if self.game_state.selected_skin == "皮肤3":
            try:
                # 加载技能图标
                skill_image = pygame.image.load(resource_path("resource/image/skins/skin_3_jineng.png")).convert_alpha()
                skill_image = pygame.transform.scale(skill_image, (50, 50))
                
                # 加载技能动画帧
                skill_frames = []
                for i in range(1, 4):
                    img_path = resource_path(f"resource/image/skins/skin_3_move_{i}.png")
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (player.rect.width, player.rect.height))
                    skill_frames.append(img)
            except Exception as e:
                print(f"加载皮肤3技能图片时出错: {e}")
                skill_frames = []
                skill_image = None

        # 游戏循环
        running = True
        while running:
            # 绘制背景
            if level_background:
                self.screen.blit(level_background, (0, 0))
            else:
                self.screen.fill(BLACK)

            # 计算游戏时间
            game_time = (pygame.time.get_ticks() - start_time) / 1000

            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.current_screen = None
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        result = self.pause_menu()
                        if result == "quit":
                            running = False
                            self.current_screen = "menu"
                        elif result == "restart":
                            running = False
                            self.game_screen()
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.jump()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 技能触发逻辑
                    if (self.game_state.selected_skin == "皮肤3" and 
                        skill_rect.collidepoint(event.pos) and 
                        skill_available and 
                        skill_frames):
                        skill_start_time = pygame.time.get_ticks()
                        skill_available = False
                        print("技能已激活")
                        
                        # 备份玩家原始图像并隐藏玩家
                        player_original_image = player.image
                        player.visible = False
                        
                        # 创建技能动画精灵
                        skill_animation = SkillAnimation(skill_frames, player.rect)
                        all_sprites.add(skill_animation)

            # 玩家移动控制
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move_right()
            else:
                player.stop()

            # 更新玩家状态
            player.update(level.platforms, level.coins)

            # 更新已收集金币数
            coins_collected = total_coins_in_level - len(level.coins)

            # 障碍物碰撞处理
            collided_obstacles = pygame.sprite.spritecollide(player, level.obstacles, False)
            for obstacle in collided_obstacles:
                if self.game_state.selected_skin == "皮肤2" and obstacle.obstacle_type == "obstacle_2":
                    obstacle.rect.x += 50
                    if obstacle.rect.x > SCREEN_WIDTH:
                        level.obstacles.remove(obstacle)
                        all_sprites.remove(obstacle)
                elif self.game_state.selected_skin=="皮肤3" and obstacle.obstacle_type=="obstacle_1" and self.bo==1:
                    pass
                elif not player.invincible:
                    running = False
                    self.current_screen = "game_over"

            # 障碍物移动
            for obstacle in level.obstacles:
                obstacle.update()

            # 道具碰撞处理
            if hasattr(level, 'items'):
                for item in pygame.sprite.spritecollide(player, level.items, True):
                    player.apply_item_effect(item)

            # 到达终点
            if level.goal and player.rect.colliderect(level.goal.rect):
                if not level_requires_card or player.has_card:
                    self.level_complete_coins = coins_collected
                    self.level_complete_time = game_time
                    running = False
                    self.current_screen = "level_complete"
                else:
                    card_message_timer = 60

            # 绘制校卡提示消息
            if card_message_timer > 0:
                card_message = self.large_font.render("你没有校卡，不得进校", True, RED)
                message_rect = card_message.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(card_message, message_rect)
                card_message_timer -= 1

            # 超时或掉落处理
            if game_time > level.time_limit or player.rect.y > SCREEN_HEIGHT:
                running = False
                self.current_screen = "game_over"

            # 绘制所有元素和UI
            for sprite in all_sprites:
                if hasattr(sprite, 'visible') and not sprite.visible:
                    continue
                self.screen.blit(sprite.image, sprite.rect)
                
            time_text = self.font.render(f"时间: {max(0, level.time_limit - game_time):.1f}秒", True, WHITE)
            coin_text = self.font.render(f"金币: {coins_collected}/{total_coins_in_level}", True, WHITE)
            level_text = self.font.render(f"关卡 {self.current_level}", True, WHITE)
            desc_text = self.font.render(level.level_description, True, WHITE)

            self.screen.blit(time_text, (20, 20))
            self.screen.blit(coin_text, (20, 50))
            self.screen.blit(level_text, (SCREEN_WIDTH - 120, 20))

            # 显示无敌时间
            if player.invincible:
                invincible_text = self.font.render(f"无敌时间: {player.invincible_timer / 60:.1f}秒", True, WHITE)
                self.screen.blit(invincible_text, (20, 80))
            
            # 显示冻结剩余时间
            if player.freeze_timer > 0:
                freeze_text = self.font.render(f"吃饭中: {player.freeze_timer / 60:.1f}秒", True, RED)
                self.screen.blit(freeze_text, (20, 110 if player.invincible else 80))
            
            # 在屏幕底部显示关卡描述
            self.screen.blit(desc_text, (20, SCREEN_HEIGHT - 40)) 

            # 技能系统逻辑
            current_time = pygame.time.get_ticks()
            
            # 更新技能动画
            if skill_animation and current_time - skill_start_time < skill_duration:
                skill_animation.update(player.rect, player.facing_right)
                self.bo=1
            elif skill_animation:
                # 技能结束，移除动画精灵并恢复玩家图像
                all_sprites.remove(skill_animation)
                self.bo=0
                if player_original_image:
                    player.image = player_original_image
                    player.visible = True
                    player_original_image = None
                skill_animation = None

            # 绘制技能图标
            if self.game_state.selected_skin == "皮肤3" and skill_image:
                if not skill_available:
                    if current_time - skill_start_time < skill_duration:
                        # 技能播放中
                        progress = (current_time - skill_start_time) / skill_duration
                        progress_rect = pygame.Rect(skill_rect.x, skill_rect.y, 
                                                int(skill_rect.width * progress), skill_rect.height)
                        skill_icon_copy = skill_image.copy()
                        pygame.draw.rect(skill_icon_copy, (100, 100, 100), progress_rect)
                        self.screen.blit(skill_icon_copy, skill_rect)
                        self.bo=1
                        
                        # 显示技能倒计时
                        skill_time_text = self.font.render(f"{(skill_duration - (current_time - skill_start_time)) // 1000 + 1}", 
                                                        True, WHITE)
                        self.screen.blit(skill_time_text, (skill_rect.centerx - 5, skill_rect.centery - 8))
                    else:
                        # 技能冷却中
                        cooldown_progress = (current_time - skill_start_time - skill_duration) / (skill_cooldown - skill_duration)
                        grayed_skill_image = skill_image.copy()
                        pygame.transform.grayscale(grayed_skill_image)
                        self.bo=0
                        # 显示冷却进度条
                        cooldown_rect = pygame.Rect(0, 0, 
                                                skill_rect.width, skill_rect.height * (1 - cooldown_progress))
                        pygame.draw.rect(grayed_skill_image, (100, 100, 100), cooldown_rect)
                        self.screen.blit(grayed_skill_image, skill_rect)
                        
                        # 显示冷却剩余时间
                        cooldown_text = self.font.render(f"{int((skill_cooldown - (current_time - skill_start_time)) // 1000 + 1)}", 
                                                    True, WHITE)
                        self.screen.blit(cooldown_text, (skill_rect.centerx - 5, skill_rect.centery - 8))
                        
                        # 检查冷却是否结束
                        if current_time - skill_start_time >= skill_cooldown:
                            skill_available = True
                else:
                    # 技能可用 - 正常显示图标
                    self.screen.blit(skill_image, skill_rect)
                    # 添加提示文字
                    hint_text = self.font.render("点击释放技能", True, WHITE)
                    hint_rect = hint_text.get_rect(midleft=(skill_rect.right + 10, skill_rect.centery))
                    self.screen.blit(hint_text, hint_rect)

            pygame.display.flip()
            self.clock.tick(60)
        # 技能动画精灵类

    #暂停菜单
    def pause_menu(self):
        paused = True
        result = None

        # 加载背景图（保持原比例，填充空白）
        try:
            original_bg = pygame.image.load(resource_path("resource/image/background/background9.webp")).convert()
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
            background = scaled_bg.subsurface((x_offset, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            background = None

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.current_screen = None
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                        return "continue"

            # 鼠标位置
            mouse_pos = pygame.mouse.get_pos()

            # 绘制背景
            if background:
                self.screen.blit(background, (0, 0))
            else:
                self.screen.fill(BLACK)

            # 绘制半透明背景
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.screen.blit(s, (0, 0))

            # 绘制标题（添加阴影效果）
            title_text = self.large_font.render("暂停", True, WHITE)
            title_shadow = self.large_font.render("暂停", True, (100, 100, 100))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(title_shadow, (title_rect.x+3, title_rect.y+3))
            self.screen.blit(title_text, title_rect)

            # 绘制按钮
            button_width, button_height = 200, 50
            buttons = [
                {"text": "继续游戏", "y": 300, "action": "continue"},
                {"text": "重新开始", "y": 370, "action": "restart"},
                {"text": "返回主菜单", "y": 440, "action": "quit"}
            ]

            for button in buttons:
                rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, button["y"], button_width, button_height)
                color = BLUE if rect.collidepoint(mouse_pos) else GREEN

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)

                text = self.font.render(button["text"], True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

                # 检查点击
                if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
                    pygame.time.delay(200)
                    paused = False
                    result = button["action"]

            pygame.display.flip()
            self.clock.tick(60)

        return result

    #游戏结束界面，显示失败信息和选项，在这里面设置背景图
    def game_over_screen(self):
        # 加载背景图（保持原比例，填充空白）
        try:
            original_bg = pygame.image.load(resource_path("resource/image/background/background5.webp")).convert()
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
            background = scaled_bg.subsurface((x_offset, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            background = None
        while self.current_screen == "game_over":
            # 绘制背景
            if background:
                self.screen.blit(background, (0, 0))
            else:
                self.screen.fill(BLACK)

            # 绘制标题
            title_text = self.large_font.render("游戏结束", True, RED)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)

            # 绘制提示
            prompt_text = self.font.render("按ESC返回主菜单，按R重新开始", True, WHITE)
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
            self.screen.blit(prompt_text, prompt_rect)

            # 绘制按钮
            button_width, button_height = 200, 50
            buttons = [
                {"text": "重新开始", "y": 350, "action": "restart"},
                {"text": "返回主菜单", "y": 420, "action": "menu"}
            ]

            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, button["y"], button_width, button_height)
                color = BLUE if rect.collidepoint(mouse_pos) else GREEN

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)

                text = self.font.render(button["text"], True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

                if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
                    pygame.time.delay(200)
                    if button["action"] == "restart":
                        self.current_screen = "game"
                    else:
                        self.current_screen = "menu"

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.current_screen = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_screen = "menu"
                    elif event.key == pygame.K_r:
                        self.current_screen = "game"

    #关卡完成界面，显示通关信息和统计，在这里面设置背景图
    def level_complete_screen(self):
        # 加载背景图（保持原比例，填充空白）
        try:
            original_bg = pygame.image.load(resource_path("resource/image/background/background3.webp")).convert()
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
            background = scaled_bg.subsurface((x_offset, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            background = None

        # 更新游戏状态
        self.game_state.update_level_stats(
            self.current_level,
            self.level_complete_coins,
            self.level_complete_time
        )
        
        # 只有当完成的关卡是当前最高关卡时才解锁下一关
        if self.current_level == self.game_state.current_level and self.current_level < 9:  # 假设总共有10个关卡
            self.game_state.current_level = self.current_level + 1
            self.game_state.save_game_data()

        while self.current_screen == "level_complete":
            # 绘制背景
            if background:
                self.screen.blit(background, (0, 0))
            else:
                self.screen.fill(BLACK)
            
            # 绘制标题
            title_text = self.large_font.render("关卡完成!", True, GREEN)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title_text, title_rect)
            
            # 绘制统计信息
            stats = [
                f"收集金币: {self.level_complete_coins}",
                f"用时: {self.level_complete_time:.1f}秒",
                f"得分: {self.game_state.calculate_score(self.current_level, self.level_complete_coins, self.level_complete_time)}"
            ]
            
            for i, stat in enumerate(stats):
                text = self.font.render(stat, True, BLACK)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 250 + i*40))
                self.screen.blit(text, text_rect)
            
            # 绘制按钮
            button_width, button_height = 200, 50
            buttons = [
                {"text": "下一关", "y": 400, "action": "next"},
                {"text": "返回主菜单", "y": 470, "action": "menu"}
            ]

            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, button["y"], button_width, button_height)
                color = BLUE if rect.collidepoint(mouse_pos) else GREEN

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)

                text = self.font.render(button["text"], True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

                if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
                    pygame.time.delay(200)
                    if button["action"] == "next" and self.current_level < 9:  # 假设总共有10个关卡
                        self.current_level += 1
                        self.current_screen = "game"
                    else:
                        self.current_screen = "menu"

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.current_screen = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_screen = "menu"
                    elif event.key == pygame.K_RETURN:
                        if self.current_level < 9:  # 假设总共有10个关卡
                            self.current_level += 1
                            self.current_screen = "game"
                        else:
                            self.current_screen = "level_select"



