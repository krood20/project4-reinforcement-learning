from api_interaction import *

world_num = "0"
x = "10"

enter_world(world_num)

while(1):
    move = "N"
    make_move(move, world_num)
    
    sleep(1)