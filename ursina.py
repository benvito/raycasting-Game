from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.editor_camera import EditorCamera


app = Ursina()
#hp = HealthBar()
#camera = EditorCamera()
player = FirstPersonController(
jump_height = 4,
speed = 7,
jump_up_duration = 1,
fall_after = 0.4,
gravity = 0.5,



							   )



#pl = Entity(model = 'cube', color = color.red, texture = 'rock1', position = (player.x, player.y+1, player.z), scale=(1.5,1.5,1.5))

for x in range(10):
	for z in range(10):
		ground = Entity(model = 'plane', texture = 'brick4', collider = 'box',position = (player.x+x, player.y-1, player.z+z), scale = (1, 1, 1))
		ground = Entity(model = 'plane', texture = 'brick4', collider = 'box',position = (player.x+x, player.y-1, player.z-z), scale = (1, 1, 1))
		ground = Entity(model = 'plane', texture = 'brick4', collider = 'box',position = (player.x-x, player.y-1, player.z-z), scale = (1, 1, 1))
		ground = Entity(model = 'plane', texture = 'brick4', collider = 'box',position = (player.x-x, player.y-1, player.z+z), scale = (1, 1, 1))

blocks = []
direction = []
from random import uniform
window.fullscreen = True



for i in range(10):
	r = uniform(-2, 2)
	block = Entity(model = 'cube', color = color.azure, texture = 'rock1', position = (r, 1+i, 3+i*5), scale=(3,3,3), collider = 'box')
	if r < 0:
		direction.append(1)
	else:
		direction.append(-1)
	blocks.append(block)

def update():
	#pl.position = Vec3(player.x, player.y + 1, player.z)

	i = 0
	for block in blocks:
		block.x -= direction[i]*time.dt
		if abs(block.x) > 5:
			direction[i] *= -1
		if block.intersects().hit:
			player.x -= direction[i]*time.dt
		if player.z > 56:
			print("You WIN!" * 6)

goal = Entity(color = color.gold, model = 'cube', texture = 'white_cube', position = (0, 11, 55), scale = (10,1,10), collider = 'box')
pillar = Entity(color = color.green, model = 'cube', position = (0, 36, 58), scale = (1, 50, 1))


Sky()
app.run()