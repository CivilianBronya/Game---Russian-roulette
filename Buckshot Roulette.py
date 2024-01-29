import random
import importlib
import time
import pygame
import sys
import pymsgbox

importlib.reload(sys)
pygame.mixer.init()


def load_bullets():
    while True:
        num_bullets = random.randint(2, 8)
        if num_bullets > 2 and num_bullets <= 8:
            break

    num_real_bullets = num_bullets // 2
    num_empty_bullets = num_bullets - num_real_bullets
    bullet_distribution = [1] * num_real_bullets + [0] * num_empty_bullets

    if random.random() < 1:
        bullet_distribution.append(1)

    random.shuffle(bullet_distribution)

    return bullet_distribution


def reload_bullets(bullets):
    bullets.extend(load_bullets())
    pymsgbox.alert(text="重新装填子弹...", title="装填子弹")
    reload_bullets_sound = pygame.mixer.Sound('reload_bullets.wav')
    reload_bullets_sound.play()

    time.sleep(1.5)
    pymsgbox.alert(text=f"当前子弹数量: {len(bullets)}\n实弹数量: {bullets.count(1)}\n空弹数量: {bullets.count(0)}",
                   title="子弹状态")


def player_round(player_name, opponent_name, player_lives, opponent_lives, bullets):
    heart_audio = pygame.mixer.Sound('heart.wav')

    while True:
        if len(bullets) == 0:
            reload_bullets(bullets)
            break

        pymsgbox.alert(text=f"\n{player_name}的回合", title="回合开始")

        action = pymsgbox.confirm(text="选择行动", title=player_name, buttons=["向自己射击", f"向{opponent_name}射击"])

        if action == '向自己射击':
            heart_audio = pygame.mixer.Sound('heart.wav')
            heart_audio.play()
            time.sleep(4)
            bullet = bullets.pop(0)
            if bullet == 1:
                shot_audio = pygame.mixer.Sound('shot.wav')
                shot_audio.play()
                time.sleep(2)
                pymsgbox.alert(
                    text=f"{player_name}选择了向自己开枪，但是不幸是实弹！\n{player_name}失去了一条命......\n剩余生命值: {player_lives - 1}",
                    title=f"{player_name}被击中")
                player_lives -= 1
            else:
                pymsgbox.alert(text=f"{player_name}选择了向自己开枪，但是幸运是空弹！", title="结果")

        elif action == f"向{opponent_name}射击":
            heart_audio.play()
            time.sleep(4)
            bullet = bullets.pop(0)
            if bullet == 1:
                shot_audio = pygame.mixer.Sound('shot.wav')
                shot_audio.play()
                time.sleep(2)
                pymsgbox.alert(
                    text=f"{player_name} 选择向 {opponent_name}开枪! 竟然是实弹！\n{opponent_name}失去了一条命......\n剩余生命值: {opponent_lives - 1}",
                    title="结果")
                opponent_lives -= 1
            else:
                pymsgbox.alert(text=f"{player_name} 选择向 {opponent_name}开枪! 竟然是空弹！{opponent_name} 幸免于难.",
                               title="结果")

        if player_lives <= 0 or opponent_lives <= 0:
            break

        if len(bullets) == 0:
            reload_bullets(bullets)

        if len(bullets) == 0:
            break

        pymsgbox.alert(text=f"\n{opponent_name}的回合", title="回合开始")

        action = pymsgbox.confirm(text="选择行动", title=opponent_name, buttons=["向自己射击", f"向{player_name}射击"])

        if action == '向自己射击':
            heart_audio.play()
            time.sleep(4)
            bullet = bullets.pop(0)
            if bullet == 1:
                shot_audio = pygame.mixer.Sound('shot.wav')
                shot_audio.play()
                time.sleep(2)
                pymsgbox.alert(
                    text=f"{opponent_name} 选择了向自己开枪，但是不幸是实弹！\n{opponent_name}失去了一条命......\n剩余生命值: {opponent_lives - 1}",
                    title=f"{opponent_name}被击中")
                opponent_lives -= 1
            else:
                pymsgbox.alert(text=f"{opponent_name} 选择了向自己开枪，但是幸运是空弹！", title="结果")

        elif action == f"向{player_name}射击":
            heart_audio.play()
            time.sleep(4)
            bullet = bullets.pop(0)
            if bullet == 1:
                shot_audio = pygame.mixer.Sound('shot.wav')
                shot_audio.play()
                time.sleep(2)
                pymsgbox.alert(
                    text=f"{opponent_name} 选择向 {player_name}开枪! 竟然是实弹！\n{player_name} 失去了一条命......\n剩余生命值: {player_lives - 1}",
                    title="结果")
                player_lives -= 1
            else:
                pymsgbox.alert(text=f"{opponent_name} 选择向 {player_name}开枪! 竟然是空弹！{player_name} 幸免于难.",
                               title="结果")

        if player_lives <= 0 or opponent_lives <= 0:
            break

    return player_lives, opponent_lives


def play_game():
    pymsgbox.alert(text="欢迎来到俄罗斯轮盘赌！", title="游戏开始")
    pymsgbox.alert(text="你们需要轮流向对方或自己开枪！", title="游戏规则")
    pymsgbox.alert(text="游戏由三轮组成，在第三轮中，如果击败对手，那么获胜！如果自己输了，准备见上帝吧！", title="游戏规则")

    player1_name = pymsgbox.prompt(text="请玩家1输入自己的游戏名(最多32个字符):", title="输入游戏名", default="")
    player2_name = pymsgbox.prompt(text="请玩家2输入自己的游戏名(最多32个字符):", title="输入游戏名", default="")

    bullets = load_bullets()

    round_num = 1
    while round_num <= 2:
        pymsgbox.alert(text=f"\n第 {round_num} 回合", title="回合开始")
        player1_lives = 2
        player2_lives = 2

        if round_num >= 3:
            player1_lives = 6
            player2_lives = 6

        while True:
            player1_lives, player2_lives = player_round(player1_name, player2_name, player1_lives, player2_lives,
                                                        bullets)

            if len(bullets) == 0 or player1_lives <= 0 or player2_lives <= 0:
                break

        if round_num > 0:
            if player1_lives > player2_lives:
                pymsgbox.alert(text=f"\n{player1_name} 获胜！", title="胜利")
            elif player2_lives > player1_lives:
                pymsgbox.alert(text=f"\n{player2_name} 获胜！", title="胜利")
            else:
                pymsgbox.alert(text="\n打成平手！", title="平局")

        play_again = pymsgbox.confirm(text="是否继续下一轮游戏？", title="继续游戏", buttons=["是", "否"])
        if play_again == "否":
            break

        round_num += 1


if __name__ == "__main__":
    play_game()
