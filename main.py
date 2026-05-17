from engine import Engine

game = Engine()

while True:
    game.events()
    game.update()
    game.draw()
    game.clock.tick(60)