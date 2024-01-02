import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

kivy.require('2.1.0')

# python script
from itertools import permutations, product

# primes for each spell level
qprimes = [[3, 5, 7], [11, 13, 17], [19, 23, 29], [31, 37, 41], [43, 47, 53], [59, 61, 67], [71, 73, 79], [83, 89, 97], [101, 103, 107]]

# list of displayable operations once found a correct combination
ops = [
	(0, "{0} + {1}"),
	(1, "{0} - {1}"),
	(2, "{1} - {0}"),
	(3, "{0} * {1}"),
	(4, "{0} / {1}"),
	(5, "{1} / {0}"),
]

# operations function: defines all the possible ops
def opf(i,x,y):
	if i == 0:
		return x+y
	if i == 1:
		return x-y
	if i == 2:
		return y-x
	if i == 3:
		return x*y
	if i == 4:
		return x/y
	if i == 5:
		return y/x
	return None

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    for indices in product(range(n), repeat=r):
        yield tuple(pool[i] for i in indices)

def process(level, dice):
	targets = qprimes[level-1]

	dperms = list(permutations(dice)) # use every die exactly once
	operms = list(combinations(ops, len(dice)-1)) # any combination of operations
	oplen = len(operms)

	for idp in range(len(dperms)):
		for iop in range(oplen):
			dp = dperms[idp]
			op = operms[iop]
			try:
				num = opf(op[0][0],dp[0],dp[1]) # result of op on first two dice
				for i in range(2, len(dp)): # loop through remaining dice/ops
					num = opf(op[i-1][0],num,dp[i])

			except ZeroDivisionError:
				continue # our final result won't have any division by zero, so skip

			if num in targets:
				# We found it, now build and display the string of this result
				s = op[0][1].format(dp[0], dp[1])
				for i in range(2,len(dp)):
					s = op[i-1][1].format("({0})".format(s),dp[i])
				
				return "{0} = {1:d}".format(s, int(num))

# kivy app
class MainApp(App):
	def build(self):
		layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

		with layout.canvas.before:
			Color(0.13, 0.14, 0.145, 1)
			self.background = Rectangle(pos=(0, 0), size=Window.size)
			Window.bind(on_resize=self.update_background_size)

		level_input_layout = BoxLayout(orientation='vertical', spacing=10)
		self.level_input_label = Label(text='Enter spell level:')
		self.level_input_field = TextInput(hint_text='number 1-9', multiline=False, foreground_color = (1, 1, 1, 1), background_color = (0.09, 0.1, 0.1, 1))
		level_input_layout.add_widget(self.level_input_label)
		level_input_layout.add_widget(self.level_input_field)

		dices_input_layout = BoxLayout(orientation='vertical', spacing=10)
		self.dices_input_label = Label(text='Enter dices:')
		self.dices_input_field = TextInput(hint_text='1 2 3 4 5 6 ...', multiline=False, foreground_color = (1, 1, 1, 1), background_color = (0.09, 0.1, 0.1, 1))
		level_input_layout.add_widget(self.dices_input_label)
		level_input_layout.add_widget(self.dices_input_field)
			
		submit_button = Button(text='Submit', on_press=self.calculate_result, size_hint=(1, None), height=60)
		self.result_label = Label(text='', size_hint_y=None, height=50)

		layout.add_widget(level_input_layout)
		layout.add_widget(dices_input_layout)
		layout.add_widget(submit_button)
		layout.add_widget(self.result_label)
        
		return layout

	def calculate_result(self, instance):
		try:
			level = int(self.level_input_field.text)
			dice = list(map(int, self.dices_input_field.text.split()))
			
			result = process(level, dice)

			self.result_label.text = f'Result: {result}'
			
		except ValueError:
			self.result_label.text = 'Invalid input'

	def update_background_size(self, instance, width, height):
		self.background.size = (width, height)

if __name__ == '__main__':
    MainApp().run()
