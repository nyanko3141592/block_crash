import tkinter as tk
import sys
import random
import pygame
import emoji
from PIL import Image, ImageTk

root = tk.Tk()

root.geometry('300x200')
root.title('サンプルプログラム')

buffer = tk.StringVar()
buffer.set('')

# キーの表示
def print_key(event):
    root.destroy()

# ラベルの設定
tk.Label(root, text='Press Space Key！', font=('FixedSys', 30)).pack()
a = tk.Label(root, textvariable=buffer)
a.pack()
a.bind('<Key>', print_key)
a.focus_set()
root.mainloop()

# 基本設定
win_width = 600  # ウインドウサイズ(x)
win_height = 480  # ウインドウサイズ(y)
win_center_x = win_width / 2  # 画面のセンター(x座標)
win_center_y = win_height / 2  # 画面のセンター(x座標)
tick = 10  # ティック数(ミリ秒)
game_over_flag = False

root = tk.Tk()
root.title(u"ブロック崩し")
root.geometry("600x480")
cv = tk.Canvas(root, width=win_width, height=win_height)  # キャンバスの作成
cv.pack()  # パック


# 基本設定
img = Image.open("face.png")
pien_img = ImageTk.PhotoImage(img)


def alarm(music_path):
    pygame.mixer.init(frequency=44100)  # 初期設定
    pygame.mixer.music.load(music_path)  # 音楽ファイルの読み込み
    pygame.mixer.music.play(1)  # 音楽の再生回数(1回)
    return 0


# ボールのクラス
class Ball:
    x = 150 + int(random.random() * 100)  # ボールの中心のX座標(初期値）
    y = 250  # ボールの中心のY座標(初期値)
    w = 15  # ボールの幅

    dx = dy = 2  # 移動量(X),移動量(Y)
    color = "red"  # ボールの色

    def draw(self):
        cv.create_oval(self.x - self.w, self.y - self.w, self.x + self.w, self.y + self.w, fill=self.color, tag="ball")
        cv.create_image(self.x, self.y, image=pien_img, tag='pien')
        cv.pack()

    def move(self):
        # 移動
        self.x += self.dx
        self.y += self.dy
        # ボールVS壁
        if self.x - self.w < 0 or self.x + self.w > win_width:
            self.dx *= -1
            alarm('boyon1.mp3')
            cv.delete("say_pien")
        if self.y - self.w < 0 or self.y + self.w > win_height:
            self.dy *= -1
            alarm('boyon1.mp3')
            cv.delete("say_pien")
        # ボールVSパドル
        if self.y + self.w > paddle.y - paddle.wy and ball.x > paddle.x - paddle.wx and ball.x < paddle.x + paddle.wx:
            if game_over_flag:
                return 0
            self.dy *= -1
            alarm('boyon1.mp3')
            cv.delete("say_pien")

    def delete(self):
        cv.delete("ball")
        cv.delete("pien")


# ボールのクラス

# パドルのクラス
class Paddle:
    x = win_center_x  # パドルの初期値(y座標)
    y = win_height - 30  # パドルの初期値(x座標)
    wx = 45  # パドルの幅(x座標)
    wy = 8  # パドルの幅(y座標)
    dx = 10  # パドルの移動量(x成分)
    color = "blue"

    def draw(self):
        cv.create_rectangle(self.x - self.wx, self.y - self.wy, self.x + self.wx, self.y + self.wy, fill=self.color,
                            tag="paddle")

    def right(self, event):
        cv.delete("paddle")
        self.x += self.dx
        self.draw()

    def left(self, event):
        cv.delete("paddle")
        self.x -= self.dx
        self.draw()

    def move(self):
        root.bind("<Right>", self.right)
        root.bind("<Left>", self.left)


# パドルのクラス

# ブロックのクラス
class Block:
    w_x = 100  # ブロックの幅(x座標)
    w_y = 30 + int(random.random() * 10)  # ブロックの幅(y座標)
    block_text = ['鬱', "ぼっち", '遅刻', '彼ピッピ', '金欠','タピオカ']
    global dy, score  # 衝突の際にボールのクラスの移動量およびスコアを変更したいので、グローバル宣言を行う。

    # ブロックのスイッチ。1がON,0がOFF
    block_list = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # j = 0 , i = 0 ~ 11
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # j = 1 , i = 0 ~ 11
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # j = 2 , i = 0 ~ 11 行・列の順番

    def draw(self):
        for i in range(6):
            for j in range(3):
                cv.create_rectangle(i * self.w_x, j * self.w_y, (i + 1) * self.w_x, (j + 1) * self.w_y, fill="yellow",
                                    tag="block" + str(j) + str(i))
                cv.create_text(i * self.w_x + self.w_x / 2, j * self.w_y + self.w_y / 2,
                               text=self.block_text[int(random.random() * len(self.block_text))],
                               font=('FixedSys', 20), tag="block_text" + str(j) + str(i))

    def reflect(self):
        if game_over_flag:
            return 0
        for i in range(12):
            for j in range(3):
                # ボールが上から反射
                if (ball.y - ball.w < (j + 1) * self.w_y  # ボールがブロックよりも下
                        and i * self.w_x < ball.x < (i + 1) * self.w_x  # ボールがブロックの左右に挟まれている
                        and self.block_list[j][i] == 1):  # スイッチが1
                    ball.dy *= -1  # 反射させる
                    cv.delete("block" + str(j) + str(i))  # ブロックの描画を消す
                    cv.delete("block_text" + str(j) + str(i))  # ブロックの描画を消す
                    alarm('pien.mp3')
                    self.block_list[j][i] = 0  # スイッチを切る
                    score.score += 1  # スコアの加点
                    score.delete()  # スコアを更新（削除-生成)
                    score.draw()
                    cv.create_text(win_center_x, win_center_y, text="🥺ぴえん", font=('FixedSys', 20), tag='say_pien')


# ブロックのクラス

# スコアのクラス
class Score():
    score = 0  # スコアの初期値

    def draw(self):
        cv.create_text(win_width - 50, 150, text=str(self.score) + "ぴえん", font=('FixedSys', 16), tag="score")

    def delete(self):
        cv.delete("score")


# スコアのクラス

# ゲームオーバーのメソッド
def gameover():
    global w, dx, dy, game_over_flag
    if ball.y + ball.w > win_height:
        cv.delete("paddle")
        cv.delete("ball")
        cv.create_text(win_center_x, win_center_y, text="🥺やばたにえん", font=('FixedSys', 40))
        ball.w = 0
        ball.dx = 0
        ball.dy = 0
        game_over_flag = True
        alarm('chan-chan3.mp3')


# ゲームオーバーのメソッド
clear_flag = False
# ゲームクリアのメソッド
def gameclear():
    global w, dx, dy, clear_flag
    if score.score == 18:
        cv.delete("paddle")
        cv.delete("ball")
        cv.create_text(win_center_x, win_center_y, text="🥺テンアゲ〜", font=('FixedSys', 40))
        ball.w = 0
        ball.dx = 0
        ball.dy = 0
        cv.delete("say_pien")
        if not clear_flag:
            alarm('dondonpafupafu1.mp3')
        clear_flag = True


# ゲームクリアのメソッド

# インスタンス生成
paddle = Paddle()  # パドル
ball = Ball()  # ボール
block = Block()  # ブロック
score = Score()  # スコア
# インスタンス生成

# 初期描画
ball.draw()  # ボール
paddle.draw()  # パドル
block.draw()  # ブロック
score.draw()  # スコア

# 初期描画
# ゲームのメインループ
def gameloop():
    ball.delete()  # ボールを消す
    ball.move()  # ボールを動かす
    paddle.move()  # ボールを動かす
    block.reflect()  # ボールを反射させ、ブロックを消す
    ball.draw()  # ボールを描く
    gameover()  # ゲームオーバーを表示させる
    gameclear()  # ゲームクリアを表示させる
    root.after(tick, gameloop)  # 50ミリ秒経過後,ループの最初に戻る


# ゲームのメインループ

# メインの実行部分
gameloop()
root.mainloop()  # 画面を表示
# メインの実行部分
