import os, time, msvcrt, random as rand
from Grid import Grid

gamewidth = 30
gameheight = 10

p1scorex = 10
p2scorex = 20
scorey = 1

fps = 30

ltime = 0


class Pong:
    def __init__(
        self, balltime, speed_scalar, score_to_win
    ):  # creates necessary components for a new pong game like the new screen grid and reset player scores
        self.grid = Grid.build(
            [[" " for i in range(gamewidth)] for j in range(gameheight)]
        )
        self.p1score = 0
        self.p2score = 0
        self.p1paddle = Paddle(5, 2)
        self.p2paddle = Paddle(5, gamewidth - 3)
        self.AIplayer = AIPlayer(self.p2paddle, self)
        self.ball = Ball(15, 5)
        self.balltime = balltime
        self.baseballtime = balltime
        self.speed_scalar = speed_scalar
        self.score_to_win = score_to_win
        self.is_running = True

        self.lastspacestr = " "

    def move_paddle(self, paddle, move_to):
        if paddle.position + move_to > 0 and paddle.position + move_to < gameheight - 1:
            if move_to == 1:
                self.grid.set(paddle.x, paddle.position - 1, " ")
                self.grid.set(paddle.x, paddle.position + 2, "|")
            elif move_to == -1:
                self.grid.set(paddle.x, paddle.position + 1, " ")
                self.grid.set(paddle.x, paddle.position - 2, "|")
            paddle.position += move_to

    def check_paddle_collision(self, paddle, moveto_x, moveto_y):
        if self.ball.y == paddle.position:
            moveto_x = -moveto_x
            self.ball.dirx = moveto_x
            moveto_y = 0
            self.ball.diry = 0
        elif self.ball.y == paddle.position + 1:
            moveto_x = -moveto_x
            self.ball.dirx = moveto_x
            moveto_y = 1
            self.ball.diry = 1
        elif self.ball.y == paddle.position - 1:
            moveto_x = -moveto_x
            self.ball.dirx = moveto_x
            moveto_y = -1
            self.ball.diry = -1
        self.balltime -= self.speed_scalar
        return moveto_x, moveto_y

    def move_ball(self, moveto_x, moveto_y):
        if (
            self.ball.x + moveto_x > gamewidth - 1 or self.ball.x + moveto_x < 0
        ):  # check edge collision x
            goal_handler(self)
            return

        if self.ball.x + moveto_x == 2:  # check p1 paddle collision
            moveto_x, moveto_y = self.check_paddle_collision(
                self.p1paddle, moveto_x, moveto_y
            )
        elif self.ball.x + moveto_x == gamewidth - 3:  # check p2 paddle collision
            moveto_x, moveto_y = self.check_paddle_collision(
                self.p2paddle, moveto_x, moveto_y
            )

        if (
            self.ball.y + moveto_y > gameheight - 1 or self.ball.y + moveto_y < 0
        ):  # check edge collision y
            moveto_y = -moveto_y
            self.ball.diry = moveto_y

        self.grid.set(self.ball.x, self.ball.y, self.lastspacestr)
        self.ball.x += moveto_x
        self.ball.y += moveto_y
        self.lastspacestr = self.grid.get(self.ball.x, self.ball.y)
        self.grid.set(self.ball.x, self.ball.y, "o")


class Paddle:
    def __init__(self, position, x):
        self.position = position
        self.x = x


class Ball:
    def __init__(self, x=15, y=5):
        self.x = x
        self.y = y
        self.dirx = -1
        self.diry = -1


class AIPlayer:
    def __init__(self, paddle, game):
        self.paddle = paddle
        self.game = game
        self.target_position = None

    # basic AI
    def update(self):
        if self.game.ball.dirx > 0:
            if self.paddle.position < self.game.ball.y:
                self.game.move_paddle(self.paddle, 1)
            elif self.paddle.position > self.game.ball.y:
                self.game.move_paddle(self.paddle, -1)

    # smart AI
    def smart_update(self):
        if self.game.ball.dirx < 0:
            self.target_position = None
        elif self.game.ball.dirx > 0:
            if self.target_position == None:  # if there is no target position, find one
                ballx = self.game.ball.x
                bally = self.game.ball.y
                balldirx = self.game.ball.dirx
                balldiry = self.game.ball.diry

                self.target_position = self.look_ahead(
                    ballx, bally, balldirx, balldiry
                ) + rand.randint(-1, 1)
            else:  # otherwise, move towards the current target position
                if self.target_position - self.paddle.position < 0:
                    self.game.move_paddle(self.paddle, -1)
                elif self.target_position - self.paddle.position > 0:
                    self.game.move_paddle(self.paddle, 1)

    def look_ahead(self, ballx, bally, balldirx, balldiry):
        if ballx == self.paddle.x - 1:
            return bally
        else:
            if bally + balldiry > gameheight - 1 or bally + balldiry < 0:
                balldiry = -balldiry

            ballx += balldirx
            bally += balldiry
            return self.look_ahead(ballx, bally, balldirx, balldiry)


def menu_screen():
    playerinput = None
    print(
        """
    /------------------------------\\
    |                              |
    |                              |
    |       Welcome to Pong        |
    |                              |
    |  Select Difficulty Scaling:  |
    |          Low (1)             |
    |          Medium (2)          |
    |          High (3)            |
    |                              |
    |                              |
    \\------------------------------/
    """
    )
    while playerinput not in [1, 2, 3]:
        while msvcrt.kbhit():  # flush the input and only keep the last keypress
            playerinput = msvcrt.getch()

            if playerinput == b"1":
                return 0.01
            if playerinput == b"2":
                return 0.025
            if playerinput == b"3":
                return 0.05


def set_up_game(game):
    # p1 paddle
    game.grid.set(2, game.p1paddle.position + 1, "|")
    game.grid.set(2, game.p1paddle.position, "|")
    game.grid.set(2, game.p1paddle.position - 1, "|")

    # AI paddle
    game.grid.set(gamewidth - 3, game.p2paddle.position + 1, "|")
    game.grid.set(gamewidth - 3, game.p2paddle.position, "|")
    game.grid.set(gamewidth - 3, game.p2paddle.position - 1, "|")

    # ball and score
    game.grid.set(game.ball.x, game.ball.y, "o")
    game.grid.set(p1scorex, scorey, str(game.p1score))
    game.grid.set(p2scorex, scorey, str(game.p2score))


def winner_screen(game, player_num):
    # p1 paddle
    game.grid.set(2, game.p1paddle.position + 1, " ")
    game.grid.set(2, game.p1paddle.position, " ")
    game.grid.set(2, game.p1paddle.position - 1, " ")

    # AI paddle
    game.grid.set(gamewidth - 3, game.p2paddle.position + 1, " ")
    game.grid.set(gamewidth - 3, game.p2paddle.position, " ")
    game.grid.set(gamewidth - 3, game.p2paddle.position - 1, " ")

    # ball and win text
    game.grid.set(game.ball.x, game.ball.y, " ")
    game.grid.array[6][9:22] = "Player " + str(player_num) + " wins"
    game.is_running = False


def goal_handler(game):  # animates and manages scoring
    game.balltime = game.baseballtime
    for i in range(4):  # make ball stop and blink at scoring line
        if game.grid.get(game.ball.x, game.ball.y) == " ":
            game.grid.set(game.ball.x, game.ball.y, "o")
        elif game.grid.get(game.ball.x, game.ball.y) == "o":
            game.grid.set(game.ball.x, game.ball.y, " ")
        draw(game)
        time.sleep(0.5)

    if game.ball.x < 2:  # means player 2 scored
        game.p2score += 1
        game.grid.set(p2scorex, scorey, str(game.p2score))
        if game.p2score >= game.score_to_win:
            winner_screen(game, 2)
    elif game.ball.x > gamewidth - 2:  # means player 1 scored
        game.p1score += 1
        game.grid.set(p1scorex, scorey, str(game.p1score))
        if game.p1score >= game.score_to_win:
            winner_screen(game, 1)

    game.grid.set(game.ball.x, game.ball.y, " ")
    game.ball.x = 15
    game.ball.y = 5
    game.ball.dirx = -game.ball.dirx
    game.ball.diry = rand.randint(-1, 1)
    game.grid.set(game.ball.x, game.ball.y, "o")
    draw(game)
    time.sleep(1)
    global ltime
    ltime = time.time()


def draw(
    game,
):  # creates border and grid as multiline string and displays it as one frame
    displaystr = "/" + "-" * (gamewidth) + "\\\n"
    for y in range(game.grid.height):
        displaystr += "|"
        for x in range(game.grid.width):
            displaystr += game.grid.get(x, y)
        displaystr += "|\n"
    displaystr += "\\" + "-" * (gamewidth) + "/"
    os.system("cls")
    print(displaystr)


def update_loop(game, fps):
    global ltime
    playerinput = None
    ltime = time.time()

    while playerinput != b"\x1b" and game.is_running:
        ctime = time.time() - ltime
        playerinput = None  # reset playerinput to None to stop the paddle from drifting even after releasing the key
        while msvcrt.kbhit():  # flush the input and only keep the last keypress
            playerinput = msvcrt.getch()

        if playerinput == b"P":
            game.move_paddle(game.p1paddle, 1)
        elif playerinput == b"H":
            game.move_paddle(game.p1paddle, -1)

        game.AIplayer.smart_update()

        if ctime > game.balltime:
            ltime += game.balltime
            game.move_ball(game.ball.dirx, game.ball.diry)

        draw(game)
        time.sleep(fps)


def main():
    scaling = menu_screen()
    game = Pong(0.3, scaling, 1)
    set_up_game(game)
    update_loop(game, 1 / fps)


if __name__ == "__main__":
    main()
