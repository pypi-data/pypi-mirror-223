import random
from evolution import diagram, trigram, evolutional_number

begin_number = evolutional_number - 6

def calculate(begin):
    sky = random.randint(1, begin)
    land = begin - sky - 1
    human = 1
    
    move_sky = sky % 4 if sky % 4 != 0 else 4
    move_land = land % 4 if land % 4 != 0 else 4
    
    sky = sky - move_sky
    land = land - move_land
    total = sky + land + human
    return (total, sky+land, sky, land, human)
    
def make_trigram():
    global begin_number
    first = calculate(begin_number)[0]
    second = calculate(first)[0]
    third = calculate(second)[1]
    trigram_number = int(third / 4)
    return trigram(trigram_number)

def divine():
    return diagram([make_trigram(), make_trigram(), make_trigram(), make_trigram(), make_trigram(), make_trigram()])

if __name__ == "__main__":
    print(divine())