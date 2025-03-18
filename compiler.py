import sys

def load_file(file_path: str) -> list[list[str]]:
	with open(file_path, 'r') as plik:
		program: list[str] = plik.readlines()
	program_lines: list[str] = [line.strip().split() for line in program]
	return program_lines




if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Proszę podać ścieżkę do pliku.")
		sys.exit(1)

	file_path = sys.argv[1]

	print(load_file(file_path))