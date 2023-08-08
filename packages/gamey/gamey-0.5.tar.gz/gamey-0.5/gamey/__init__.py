import pygame as p

p.init()

last_window = None

FPS = 60
clock = p.time.Clock()

class Window:

	def __init__(self, title="Gamie Window", width=800, height=600):
		global last_window

		self.window = p.display.set_mode((width, height))
		p.display.set_caption(title)

		self.background = (255, 255, 255)

		self.sprites = []
		self.objects = []
		self.events = {}
		self.runlist = []
		
		self.add_default_events()

		last_window = self

	def add_event(self, event_type, callback):
		if str(event_type) not in self.events:
			self.events[str(event_type)] = []
		self.events[str(event_type)].append(callback)

	def add_default_events(self):
		self.add_event(p.QUIT, self.close)
	
	def run(self):
		self.running = True
		while self.running:
			for event in p.event.get():
				if str(event.type) in self.events:
					for callback in self.events[str(event.type)]:
						callback(event)

			self.window.fill(self.background)

			for sprite in self.sprites:
				self.window.blit(sprite.image, (sprite.x, sprite.y))

			for i in self.runlist:
				i()

			p.display.flip()
			p.display.update()

			clock.tick(FPS)

	def close(self, event):
		p.quit()
		quit()

class Sprite:

	def __init__(self, image_path, x=0, y=0):
		self.image = p.image.load(image_path)
		self.x = x
		self.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		last_window.sprites.append(self)

	def set_size(self, width, height=None):
		if not height:
			height = width
		self.width = width
		self.height = height
		self.image = p.transform.scale(self.image, (self.width, self.height))

class Player:

	def __init__(self, sprite, movement_speed=100):
		last_window.add_event(p.KEYDOWN, self.keydown)
		last_window.add_event(p.KEYUP, self.keyup)
		self.sprite = sprite
		self.speed = movement_speed / FPS

		self.KEYS_UP     =  [p.K_w, p.K_UP]
		self.KEYS_DOWN   =  [p.K_s, p.K_DOWN]
		self.KEYS_LEFT   =  [p.K_a, p.K_LEFT]
		self.KEYS_RIGHT  =  [p.K_d, p.K_RIGHT]

		self.MOVING_UP = self.MOVING_DOWN = self.MOVING_LEFT = self.MOVING_RIGHT = False
	
		last_window.runlist.append(self.check_motion)
	
	def keydown(self, event):
		if event.key in self.KEYS_UP:
			self.MOVING_UP = True
		if event.key in self.KEYS_DOWN:
			self.MOVING_DOWN = True
		if event.key in self.KEYS_LEFT:
			self.MOVING_LEFT = True
		if event.key in self.KEYS_RIGHT:
			self.MOVING_RIGHT = True

	def keyup(self, event):
		if event.key in self.KEYS_UP:
			self.MOVING_UP = False
		if event.key in self.KEYS_DOWN:
			self.MOVING_DOWN = False
		if event.key in self.KEYS_LEFT:
			self.MOVING_LEFT = False
		if event.key in self.KEYS_RIGHT:
			self.MOVING_RIGHT = False

	def check_motion(self):
		old_pos = (self.sprite.x, self.sprite.y)
		if self.MOVING_UP:
			self.sprite.y -= self.speed
		if self.MOVING_DOWN:
			self.sprite.y += self.speed
		if self.MOVING_LEFT:
			self.sprite.x -= self.speed
		if self.MOVING_RIGHT:
			self.sprite.x += self.speed

		x = self.sprite.x
		y = self.sprite.y
		xr = x + self.sprite.width
		yb = y + self.sprite.height

		
		
		for obj in last_window.objects:

			obj.x_left = obj.sprite.x
			obj.x_right = obj.sprite.x + obj.sprite.width
			obj.y_top = obj.sprite.y
			obj.y_bottom = obj.sprite.y + obj.sprite.height

			if x > obj.x_left and x < obj.x_right:
				if y > obj.y_top and y < obj.y_bottom:
					self.sprite.x, self.sprite.y = old_pos
			if xr > obj.x_left and xr < obj.x_right:
				print(obj.y_bottom)
				if yb > obj.y_top and yb < obj.y_bottom:
					self.sprite.x, self.sprite.y = old_pos

class Object:
	def __init__(self, sprite):
		self.sprite = sprite
		last_window.objects.append(self)
