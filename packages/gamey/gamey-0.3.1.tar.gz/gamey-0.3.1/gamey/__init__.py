import pygame as p

p.init()

last_window = None

class Window:

	def __init__(self, title="Gamie Window", width=800, height=600):
		global last_window

		self.window = p.display.set_mode((width, height))
		p.display.set_caption(title)

		self.background = (255, 255, 255)

		self.sprites = []

		self.events = {}
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
			
			p.display.flip()
			p.display.update()

	def close(self, event):
		p.quit()
		quit()

class Sprite:

	def __init__(self, image_path, x=0, y=0):
		self.image = p.image.load(image_path)
		self.x = x
		self.y = y
		last_window.sprites.append(self)

	def set_size(self, width, height=None):
		if not height:
			height = width
		self.image = p.transform.scale(self.image, (width, height))
