from z3 import *


wolf, fox, bird, caterpillar, snail = Bools('wolf fox bird caterpillar snail')
wolf_eat_fox, wolf_eat_bird, wolf_eat_caterpillar, wolf_eat_snail = Bools('wolf_eat_fox wolf_eat_bird wolf_eat_caterpillar wolf_eat_snail')
fox_eat_wolf, fox_eat_bird, fox_eat_caterpillar, fox_eat_snail = Bools('fox_eat_wolf fox_eat_bird fox_eat_caterpillar fox_eat_snail')
bird_eat_wolf, bird_eat_fox, bird_eat_caterpillar, bird_eat_snail = Bools('bird_eat_wolf bird_eat_fox bird_eat_caterpillar bird_eat_snail')
caterpillar_eat_wolf, caterpillar_eat_fox, caterpillar_eat_bird, caterpillar_eat_snail = Bools('caterpillar_eat_wolf caterpillar_eat_fox caterpillar_eat_bird caterpillar_eat_snail')
snail_eat_wolf, snail_eat_fox, snail_eat_bird, snail_eat_caterpillar = Bools('snail_eat_wolf, snail_eat_fox, snail_eat_bird, snail_eat_caterpillar')

s: Solver = Solver()

wolf_eat_grain, wolf_eat_plant = Bools('wolf_eat_grain wolf_eat_plant')
fox_eat_grain, fox_eat_plant = Bools('fox_eat_grain fox_eat_plant')
bird_eat_grain, bird_eat_plant = Bools('bird_eat_grain bird_eat_plant')
caterpillar_eat_grain, caterpillar_eat_plant = Bools('caterpillar_eat_grain caterpillar_eat_plant')
snail_eat_grain, snail_eat_plant = Bools('snail_eat_grain snail_eat_plant')

s.add(And(wolf, fox, bird, caterpillar, snail))
s.add(And(Not(wolf_eat_fox), Not(wolf_eat_grain), bird_eat_caterpillar, Not(bird_eat_snail), caterpillar_eat_plant, snail_eat_plant, caterpillar_eat_grain, snail_eat_grain))
s.add((Or(And(wolf_eat_plant, wolf_eat_grain), And(wolf_eat_caterpillar, wolf_eat_snail))))
s.add((Or(And(fox_eat_plant, fox_eat_grain), And(fox_eat_caterpillar, fox_eat_snail))))
s.add((Or(And(bird_eat_plant, bird_eat_grain), And(bird_eat_caterpillar, bird_eat_snail))))

s.add(Or(And(wolf_eat_fox,fox_eat_grain), And(wolf_eat_bird, bird_eat_grain), And(wolf_eat_caterpillar, caterpillar_eat_grain), And(wolf_eat_snail, snail_eat_grain), 
And(fox_eat_bird, bird_eat_grain), And(fox_eat_caterpillar, caterpillar_eat_grain), And(fox_eat_snail, snail_eat_grain), 
And(bird_eat_caterpillar, caterpillar_eat_grain), And(bird_eat_snail, snail_eat_grain)))

print(s.check())