import sys

def load_file(file_path: str) -> list[list[str]]:
	with open(file_path, 'r') as plik:
		program: list[str] = plik.readlines()
	program_lines: list[list[str]] = [line.strip().split() for line in program]
	return program_lines


def compile_code(lines: list[list[str]]) -> list[list[str]]:
	"""
	Kompiluje kod, usuwając puste linie i zamieniając wystąpienia etykiet (def <nazwa>)
	na numer linii wynikowego kodu. Linie definiujące etykiety nie są dodawane do wyniku.
	
	:param lines: Lista linijek, gdzie każda linijka to lista tokenów.
	:return: Lista linijek z zamienionymi etykietami na numery linii.
	"""
	compiled_code: list[list[str]] = []
	labels: dict[str, int] = {}  # Przechowuje etykiety i odpowiadające im numery linii

	# Pierwszy przebieg: rejestracja etykiet oraz usuwanie pustych linii
	for line in lines:
		# Pomijamy linie puste lub składające się tylko z białych znaków
		if not line or all(token.strip() == "" for token in line):
			continue
		if line[0] == "def" and len(line) > 1:
			labels[line[1]] = len(compiled_code) + 1
		else:
			compiled_code.append(line)

	# Drugi przebieg: zamiana wystąpień etykiet na numer linii
	for line in compiled_code:
		for i, token in enumerate(line):
			token_stripped = token.strip()
			if token_stripped in labels:
				# Zachowujemy oryginalne odstępy (leading/trailing)
				leading = token[:len(token) - len(token.lstrip())]
				trailing = token[len(token.rstrip()):]
				line[i] = leading + str(labels[token_stripped]) + trailing

	return compiled_code


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Proszę podać ścieżkę do pliku.")
		sys.exit(1)

	file_path = sys.argv[1]

	loaded_file: list[list[str]] = load_file(file_path)
	 
	compiled_code: list[list[str]] = compile_code(loaded_file)

	for line in compiled_code:
		print(*line)