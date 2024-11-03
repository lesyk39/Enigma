from string import ascii_uppercase as ABC

class Enigma:
	list_of_rotors = {
		'ETW':   'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
		'1':     'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
		'2':     'AJDKSIRUXBLHWTMCQGZNPYFVOE',
		'3':     'BDFHJLCPRTXVZNYEIWGAKMUSQO',
		'4':     'ESOVPZJAYQUIRHXLNFTGKDCMWB',
		'5':     'VZBRGITYUPSDNHLXAWMJQOFECK',
		'6':     'JPGVOUMFYQBENHZRDKASXLICTW',
		'7':     'NZJHGRCXMYSWBOUFAIVLPEKQDT',
		'8':     'FKQHTLXOCBJSPDZRAMEWNIUYGV',
		'beta':  'LEYJVCNIXWPBQMDRTAKZGFUHOS',
		'gamma': 'FSOKANUERHMBTIYCWLQPZXVGJD'
	}

	list_of_reflektors = {
		'A':      'EJMZALYXVBWFCRQUONTSPIKHGD',
		'B':      'YRUHQSLDPXNGOKMIEBFZCWVJAT',  #Wehrmacht
		'C':      'FVPJIAOYEDRZXWGCTKUQSBNMHL',  #Luftwaffe
		'B Thin': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
		'C Thin': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
	}

	def __init__(self, rotors: list[str], positions: list[int], rings: list[int], reflektor: str, plugboard: str='') -> None:
		'''
		enigma = Enigma(
			rotors=['1', '2', '3'],
			positions=[1, 1, 1],
			rings=[17, 5, 22],
			reflektor='B',
			plugboard = 'AB CD EF'
		)
		'''
		self.set_rotors(rotors, positions, rings)
		self.set_reflektor(reflektor)
		self.set_plugboard(plugboard)

	def set_rotors(self, rotors: list[str], positions: list[int], rings: list[int]) -> None:
		if not all(isinstance(i, str) for i in rotors):
			raise TypeError
		if not all(isinstance(i, int) for i in positions + rings):
			raise TypeError

		if not (len(rotors) == len(positions) == len(rings)):
			raise ValueError
		if not all(i in self.list_of_rotors for i in rotors):
			raise ValueError
		if not all(1 <= i <= 26 for i in positions + rings):
			raise ValueError
		
		self._rotors = [self.list_of_rotors[i] for i in rotors]
		self._positions = positions
		self._rings = rings

	def set_reflektor(self, reflektor: str) -> None:
		if reflektor not in self.list_of_reflektors:
			raise ValueError
		self._reflektor = self.list_of_reflektors[reflektor]

	def set_plugboard(self, plugboard: str) -> None:
		plugboard = plugboard.strip().upper()
		if not isinstance(plugboard, str):
			raise TypeError
		p = plugboard.split(' ')
		if not all(len(i)==2 and i in ABC for i in p):
			raise TypeError
		if len(plugboard) > 38 or set(plugboard.replace(' ', '')).difference(ABC):
			raise ValueError
		self._plugboard = dict(p + plugboard[::-1].split(' '))
	
	def encode(self, text: str) -> str:
		ans = []
		text = text.upper()
		for i in text:
			if i in ABC:
				self.pust_rotors()
				i = ABC.index(self._plugboard.get(i, i))
				for j, k, r in zip(self._rotors[::-1], self._positions[::-1], self._rings[::-1]):
					n = k - r
					i = ABC.index(j[(i + n)%26]) - n
				
				i = ABC.index(self._reflektor[i%26])

				for j, k, r in zip(self._rotors, self._positions, self._rings):
					n = k - r
					i = j.index(ABC[(i + n)%26]) - n

				i = ABC[i%26]
				i = self._plugboard.get(i, i)
			ans.append(i)
		return ''.join(ans)

	def pust_rotors(self) -> None:
		t = [0, 0, 1]
		if self._positions[2] == self._rings[2]:
			t[1] = 1
		if self._positions[1] == self._rings[1]:
			t[0] = t[1] = 1
		self._positions = [(i+j-1)%26+1 for i, j in zip(self._positions, t)]