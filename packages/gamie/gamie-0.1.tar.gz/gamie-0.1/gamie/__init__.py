import pygame as p

p.init()

class Window:

	def __init__(self, title="Gamie Window", width=800, height=600):
		self.window = p.display.set_mode((width, height))
		p.display.set_caption(title)

		self.background = (255, 255, 255)

		self.events = {}
		self.add_default_events()

	def add_event(self, event, callback):
		self.events[str(event)] = callback

	def add_default_events(self):
		self.add_event(p.QUIT, self.close)
	
	def run(self):
		self.running = True
		while self.running:
			for event in p.event.get():
				if str(event.type) in self.events:
					self.events[str(event.type)](event)

			self.window.fill(self.background)
			
			p.display.flip()
			p.display.update()

	def close(self, event):
		p.quit()
		quit()
