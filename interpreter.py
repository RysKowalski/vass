import sys
from sys import exit

def log_data(text: str) -> None:
	with open('logs.log', 'a') as plik:
		plik.write(text + '\n')

class Interpreter:
	def __init__(self):
		self.variables = {"A": 0, "B": 0, "C": 0, "D": 0}
		self.program = []
		self.current_line = 0
		self.steps = 0

	def load_program(self, file_path):
		with open(file_path, 'r') as f:
			self.program = f.readlines()

	def execute(self):
		while self.current_line < len(self.program):
			self.steps += 1
			line = self.program[self.current_line].strip()

			if line.lstrip().startswith("#"):
				self.current_line += 1
				continue

			if line == "":
				self.current_line += 1
				continue

			parts = line.split()
			command = parts[0]
			#print('\n',command)
			try:
				if command == "wypisz":
					self.print_instruction(parts)
				elif command == "wczytaj":
					self.read_input(parts)
				elif command == "ustaw":
					self.set_variable(parts)
				elif command == "zwiększ":
					self.increment_variable(parts)
				elif command == "zmniejsz":
					self.decrement_variable(parts)
				elif command == "jeżeli":
					self.conditional_jump(parts)
				elif command == "skocz":
					self.jump(parts)
				elif command == "nowa":
					self.new_line()
				else:
					print(f"Unknown command: {command}")
					self.current_line += 1
					
				log_data(f'steps: {self.steps}, line = {self.current_line}, vars = {self.variables}, {command = }, {parts = }')
				if self.steps > 10_000:
					raise RuntimeError('program nie może być dłóższy niż 10_000 linijek')

			except Exception as e:
				raise RuntimeError(f'{e}\n\nwystąpił błąd.\n{parts = }\n{self.current_line = }\n{self.variables = }')
		print()

	def print_instruction(self, parts):
		if parts[1] == "zmienną":
			print(self.variables[parts[2]], end='')
		elif parts[1] == "napis":
			# Łączenie wszystkich części po słowie "napis" w jeden ciąg
			text = " ".join(parts[2:])
			# Znalezienie pierwszego i drugiego wystąpienia cudzysłowu
			start = text.find('"') + 1
			end = text.find('"', start)
			if start > 0 and end > start:
				# Wydrukowanie tekstu pomiędzy cudzysłowami
				print(text[start:end], end='')
		self.current_line += 1



	def read_input(self, parts):
		var = parts[1]
		self.variables[var] = int(input('podaj liczbę: '))
		self.current_line += 1  # Kontynuuj po wczytaniu danych

	def set_variable(self, parts):
		var = parts[1]
		value = parts[2]
		if value in self.variables:
			self.variables[var] = self.variables[value]
		else:
			self.variables[var] = int(value)
		self.current_line += 1

	def increment_variable(self, parts):
		var = parts[1]
		value = parts[2]
		if value in self.variables:
			self.variables[var] += self.variables[value]
		else:
			self.variables[var] += int(value)
		
		self.current_line += 1

	def decrement_variable(self, parts):
		var = parts[1]
		value = parts[2]
		if value in self.variables:
			self.variables[var] -= self.variables[value]
		else:
			self.variables[var] -= int(value)
		
		self.current_line += 1

	def conditional_jump(self, parts):
		var = parts[1]
		operator = parts[2]
		value = parts[3]
		if value in self.variables:
			value = self.variables[value]
		else:
			value = int(value)

		if operator == "<":
			condition = self.variables[var] < value
		elif operator == "<=":
			condition = self.variables[var] <= value
		elif operator == "=":
			condition = self.variables[var] == value
		elif operator == "!=":
			condition = self.variables[var] != value
		elif operator == ">":
			condition = self.variables[var] > value
		elif operator == ">=":
			condition = self.variables[var] >= value
		else:
			condition = False
		
		#log_data(f'{condition = }, {parts = }, vars = {self.variables}')
		
		if condition:
			if parts[4] == "end":
				exit()
			elif parts[4] == "next":
				self.current_line += 1
			else:
				self.current_line = int(parts[4]) -1
		else:
			if parts[5] == "end":
				self.current_line = len(self.program)
			elif parts[5] == "next":
				self.current_line += 1
			else:
				self.current_line = int(parts[5]) -1

	def jump(self, parts):
		target = parts[1]
		if target == "end":
			self.current_line = len(self.program)
		else:
			self.current_line = int(target) - 1

	def jump_to(self, line):
		if line == "end":
			self.current_line = len(self.program)
		else:
			self.current_line = int(line) - 1

	def new_line(self):
		print()
		self.current_line += 1

def main():
	if len(sys.argv) < 2:
		print("Proszę podać ścieżkę do pliku.")
		sys.exit(1)

	log_data('\n\n\n\n')
	file_path = sys.argv[1]
	interpreter = Interpreter()
	interpreter.load_program(file_path)
	interpreter.execute()

if __name__ == "__main__":
	main()
