import turtle


class Box(turtle.Turtle):
    def __init__(self, x, y, w, h):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.goto(x,y)
        self.shapesize(w, h)

    def up(self):
        self.sety(self.ycor() + (self.ycor() < 220) * 20)

    def down(self):
        self.sety(self.ycor() - (self.ycor() > -220) * 20)

    def draw(self):
        self.write("{}               {}".format(self.pts, self.ptsMachine),
                   font = ("Arial", 40, "normal"), align = "center")


class Score(Box):
    def __init__(self, x, y, w, h):
        Box.__init__(self, x, y, w, h)
        self.goto(x, y)
        self.pts = 0
        self.ptsMachine = 0
        self.hideturtle()
        self.draw()


class Ball(Box):
    def __init__(self, x, y, w, h):
        Box.__init__(self, x, y, w, h)
        self.machiney = 0
        self.bx = 0
        self.by = 0
        self.vx = 1
        self.vy = 1

    def update(self):
        self.bx += self.vx
        self.by += self.vy
        ball.goto(self.bx, self.by)
        machine.goto(machine.xcor(), self.machiney)
        if self.bx >= machine.xcor() -30:
            self.vx *= -1
        if self.bx <= human.xcor() + 30 and self.by < human.ycor() +100 and self.by > human.ycor() - 100:
            self.vx *= -1
        elif self.bx < human.xcor():
            self.vx *= -1
            self.bx = 0
            score.pts += 1
            score.clear()
            score.draw()
        if self.by >= 280 or self.by <= -280:
            self.vy *= -1
        if self.bx > 20:
            if machine.ycor() < self.by and self.machiney < 220:
                self.machiney +=1
            if machine.ycor() > self.by and self.machiney > -220:
                self.machiney -=1


        
human = Box(-350, 0, 8, 1)
machine = Box(350, 1, 8, 1)
ball = Ball(0, 0, 2, 2)
score = Score(0, 230, 10, 10)

win = turtle.Screen()
win.title("Pong Python")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)


win.listen()
win.onkeypress(human.up, "Up")
win.onkeypress(human.down, "Down")

while True:
    win.update()
    ball.update()
