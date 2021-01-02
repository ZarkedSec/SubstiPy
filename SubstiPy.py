# coding: utf-8

import sys
import string
from os import system, path
from math import log10 as log
from random import shuffle, randint

class Color:
	GREEN = "\033[32m"
	MAGENTA = "\033[35m"
	CYAN = "\033[36m"
	WHITE = "\033[37m"
	RED = "\033[31m"

def check_file():
	(sys.argv).remove("SubstiPy.py")
	if len(sys.argv) != 2:
		print(Color.WHITE+"\nusage : python3 SubstiPy.py <text_file> <wordlist>\n")
		exit(1)
	file = sys.argv[0]
	wordlist = sys.argv[1]
	if path.isfile(file) == False or path.isfile(wordlist) == False :
		print(Color.WHITE+"\nFile selected doesn't exist")
		print(Color.WHITE+"usage : python3 SubstiPy.py <text_file> <wordlist>\n")
		exit(1)
	return file, wordlist

file, wordlist = check_file()
words = (open(wordlist, "r").read()).split("\n")
original_text = open(file, "r").read()
text = original_text

changed_index = [] # Index of changed letters
changed_letters = [] # Original letters
changed_letters_in = [] # New letters
replaced_letters = list(string.ascii_uppercase) # New letters + others (table)
punctuation = ["-","'"]

class menu:
	def help():												# help function
		print(Color.WHITE+"""
clear .......................... Clear the terminal screen
replace A B .................... Replace a letter A by a letter B
swap <cword> <word> ............ Replace a word with another one
frequency ...................... Calculate letters frequency in the text
find <cword> <clear_letters> ... Find a ciphered word in a word list
original ....................... Print original text
restart ........................ Delete all changes and come back to the original text
exit ........................... Leave the program
		""")
	def clear(text, changed_index, replaced_letters):		# clear function
		system("clear && printf '\e[3J'")
		print(Color.MAGENTA+"""
███████╗██╗   ██╗██████╗ ███████╗████████╗██╗██████╗ ██╗   ██╗
██╔════╝██║   ██║██╔══██╗██╔════╝╚══██╔══╝██║██╔══██╗╚██╗ ██╔╝
███████╗██║   ██║██████╔╝███████╗   ██║   ██║██████╔╝ ╚████╔╝
╚════██║██║   ██║██╔══██╗╚════██║   ██║   ██║██╔═══╝   ╚██╔╝
███████║╚██████╔╝██████╔╝███████║   ██║   ██║██║        ██║
╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝╚═╝        ╚═╝""")
		print(Color.MAGENTA+"       Substitution helper\n\n")
		text = list(text)
		for i in range(0, len(text)):
			if i in changed_index:
				text[i] = Color.GREEN+text[i]+Color.WHITE
		text = ''.join(text)
		print(Color.WHITE+text+"\n\n┌─"+"┬─"*25+"┐")
		table=""
		for char in list(string.ascii_uppercase):
			table += "│"+char
		print(Color.WHITE+table+"│\n"+"├─"+"┼─"*25+"┤")
		table=""
		for char in list(replaced_letters):
			table += "│"+char
		print(Color.WHITE+table+"│\n"+"└─"+"┴─"*25+"┘\n")
	def replace(a, b, text, changed_index):					# replace function
		text = list(text)
		for i in range(0,len(text)):
			if not(i in changed_index):
				char = text[i]
				if char == a.lower():
					text[i] = b.lower()
					changed_index += [i]
				elif char == a.upper():
					text[i] = b.upper()
					changed_index += [i]
		text = ''.join(text)
		return text, changed_index
	def swap(a, b, changed_index, changed_letters, changed_letters_in, text):
		for i in range(0, len(a)):
			if a[i] in changed_letters:
				continue
			elif b[i] in changed_letters_in:
				continue
			changed_letters += [a[i]]
			changed_letters_in += [b[i]]
			text, changed_index = menu.replace(a[i], b[i], text, changed_index)
			if b[i].upper() in list(string.ascii_uppercase):
				replaced_letters[list(string.ascii_uppercase).index(a[i].upper())] = Color.GREEN+b[i].upper()+Color.WHITE
			if b[i].upper() in replaced_letters:
				replaced_letters[replaced_letters.index(b[i].upper())] = Color.RED+"?"+Color.WHITE
		return changed_index, changed_letters, changed_letters_in, text
	def frequency(text):									# frequency function
		text = list(text)
		counter = {}
		total = 0
		for letter in list(string.ascii_uppercase):
			counter.update({letter:0})
		for letter in list(text):
			if letter.upper() in list(string.ascii_uppercase):
				total += 1
				counter.update({letter.upper():counter[letter.upper()]+1})
		print("┌───┬──────┐")
		for letter in list(string.ascii_uppercase):
			if list(string.ascii_uppercase).index(letter) > 0 :
				print("├───┼──────┤")
			counter.update({letter.upper():(counter[letter.upper()]/float(total))*100})
			percent = "{:.1f}".format(counter[letter.upper()])+"%"
			print("│ "+letter.upper()+" │"+percent+" "*(6-len(percent))+"│")
		print("└───┴──────┘")
	def find(find, clear_letters):											# find function
		find_size = len(find)
		find_pattern = []
		for char in find:
			pattern = []
			if char in punctuation :
				pattern = [char]
			else:
				for i in range(0, find_size):
					if find[i] == char :
						pattern += [i]
			find_pattern += [pattern]
		found = []
		for word in words:
			word_size = len(word)
			if word_size == find_size:
				word_pattern = []
				for char in word:
					pattern = []
					if char in punctuation :
						pattern = [char]
					else :
						for i in range(0, find_size):
							if word[i] == char :
								pattern += [i]
					word_pattern += [pattern]
				if word_pattern == find_pattern :
					if clear_letters != "":
						add=True
						for i in range(0, len(clear_letters)):
							if clear_letters[i] != "_":
								if clear_letters[i] != word[i]:
									add=False
						if add == True:
							found += [word]
					else:
						found += [word]
		if clear_letters != "":
			to_delete = []
			for i in range(0, len(found)):
				for e in range(0, len(clear_letters)):
					if clear_letters[e] != "_":
						if clear_letters[e] != found[i][e]:
							to_delete += [found[i]]
			for i in to_delete:
				del found[found.index(i)]
		return found
		print("\n")
	def exit():												# exit function
		print("\n")
		exit()

class autocompletion:
	def RighFormat(text):
	    text = (text.upper()).replace(" ","")
	    for char in list(text) :
	        if not(char in string.ascii_uppercase):
	        	text = text.replace(char, "")
	    return text

	def QuadgramsN(file):
	    quadgrams = {}
	    N = 0
	    for i in range(0, len(file)-1):
	        file[i] = file[i].split(" ")
	        quadgrams[file[i][0]] = float(file[i][1])
	        N += int(file[i][1])
	    return quadgrams, N

	def Fitness(text, quadgrams, N):
	    fitness = 0
	    for i in range(0, len(text)-3):
	        try:
	            fitness += log(quadgrams[text[i:i+4]]/N)
	        except:
	            fitness += log(0.01/N)
	    return fitness

	def Substitute(TEXT, ALPHABET, SUBSTITUTED_ALPHABET):
	    substituted_text = list(TEXT)
	    for i in range(0, len(TEXT)):
	        substituted_text[i] = SUBSTITUTED_ALPHABET[ALPHABET.index(substituted_text[i])]
	    return ''.join(substituted_text)

	def Break(TEXT, ALPHABET, QUADGRAMS, N, limit):
	    TEXT_RIGHT_FORMAT = TEXT
	    text_sample = TEXT

	    key = ALPHABET[:]

	    final_key = []
	    final_fitness = -9e+10

	    endless = 0

	    system("clear && printf '\e[3J'")
	    print("["+"#"*int(endless*30/limit)+" "*int(30/limit*(limit-endless))+"] "+str(endless)+" / "+str(limit))

	    while endless < limit:
	        shuffle(key)
	        loop = True
	        best_fitness = -9e+10
	        best_key = []
	        while loop:
	            loop = False
	            for a in range(0, 26):
	                for b in range(0, 26):
	                    new_key = key[:]
	                    new_key[a], new_key[b] = new_key[b], new_key[a]
	                    text_sample = autocompletion.Substitute(TEXT_RIGHT_FORMAT, ALPHABET, new_key)
	                    fitness = autocompletion.Fitness(text_sample, QUADGRAMS, N)
	                    if fitness > best_fitness:
	                        best_fitness = fitness
	                        best_key = new_key[:]
	                        best_text = text_sample
	                        loop = True
	            key = best_key[:]
	        if final_fitness < best_fitness:
	            final_fitness = best_fitness
	            final_key = best_key
	            final_text = best_text
	            endless = 0
	        else :
	            endless += 1
	        system("clear && printf '\e[3J'")
	        print("["+"#"*int(endless*30/limit)+" "*int(30/limit*(limit-endless))+"] "+str(endless)+" / "+str(limit))
	    return final_key, final_fitness, final_text

	def BackToNormal(TEXT, final_text):
	    final_text = list(final_text)
	    text = list(TEXT)

	    for i in range(0, len(text)):
	        if text[i].islower() :
	            final_text[i] = final_text[i].lower()
	        elif not(text[i] in string.ascii_uppercase):
	            final_text = final_text[:i]+[text[i]]+final_text[i:]
	    return ''.join(final_text)

system("clear")

yn_autocompletion = input("\nDo you want to try the autocompletion? [Y/N] (Default: N) : ").upper()

if yn_autocompletion == "Y" or yn_autocompletion == "YES":

	ALPHABET = list(string.ascii_uppercase)
	lang = ""
	while not(lang=="EN" or lang=="FR") :
		system("clear && printf '\e[3J'")
		lang = (input("\nThe ciphered text is in English/French? [fr/en] : ")).upper()
	if lang=="EN":
		FILE = (open("src/english_quadgrams.txt","r").read()).split("\n")
	elif lang=="FR":
		FILE = (open("src/french_quadgrams.txt","r").read()).split("\n")

	text = autocompletion.RighFormat(original_text)
	QUADGRAMS, N = autocompletion.QuadgramsN(FILE)
	system("clear && printf '\e[3J'")
	limit = input(Color.RED+"\n\n--------------------------------------------------------------\n\n - The more loops you do, the more chances you have to find the clear text\n   (It can take up to several minutes for a long text).\n\n - This script does not have a 100% success rate,\n   you might have to launch it several times before finding your solution\n\n--------------------------------------------------------------"+Color.WHITE+"\n\nHow many loops do you want to make? (Default: 5) : ")
	try:
		limit = int(limit)
	except:
		limit = 5
	key, fitness, text = autocompletion.Break(text, ALPHABET, QUADGRAMS, N, limit)
	text = autocompletion.BackToNormal(original_text, text)

	replaced_letters = key[:]
	for i in range(0, len(replaced_letters)):
		replaced_letters[i] = Color.GREEN+replaced_letters[i]+Color.WHITE

	changed_letters = ALPHABET[:]
	changed_letters_in = key[:]

	for i in range(0, len(text)):
		if text[i] in ALPHABET or text[i] in list(string.ascii_lowercase) :
			changed_index += [i]

menu.clear(text, changed_index, replaced_letters)

while True:
	cmd = input(Color.CYAN+"> "+Color.WHITE)
	if cmd != "" :
		if cmd.lower() == "help" :							# help input
			menu.help()
		elif cmd.lower() == "clear" :						# clear input
			menu.clear(text, changed_index, replaced_letters)
		elif ((cmd.lower()).split())[0] == "replace" :		# replace input
			cmd = ((cmd.lower()).split())
			if len(cmd) == 3:
				if cmd[1].upper() in string.ascii_uppercase and cmd[2].upper() in string.ascii_uppercase :
					cmd[1] = cmd[1].upper()
					cmd[2] = cmd[2].upper()
					if cmd[1] in changed_letters:
						print(Color.WHITE+"You already changed the letter '"+cmd[1].lower()+"' in '"+changed_letters_in[changed_letters.index(cmd[1])].lower()+"'")
						continue
					elif cmd[2] in changed_letters_in:
						print(Color.WHITE+"You already changed the letter '"+changed_letters[changed_letters_in.index(cmd[2])].lower()+"' in '"+cmd[2].lower()+"'")
						continue
					changed_letters += [cmd[1]]
					changed_letters_in += [cmd[2]]
					text, changed_index = menu.replace(cmd[1], cmd[2], text, changed_index)
					replaced_letters[list(string.ascii_uppercase).index(cmd[1].upper())] = Color.GREEN+cmd[2].upper()+Color.WHITE
					if cmd[2].upper() in replaced_letters:
						replaced_letters[replaced_letters.index(cmd[2].upper())] = Color.RED+"?"+Color.WHITE
					menu.clear(text, changed_index, replaced_letters)
				else :
					print(Color.WHITE+"\nReplace usage : replace A B .................... Replace a letter A by a letter B\n")
			else :
				print(Color.WHITE+"\nReplace usage : replace A B .................... Replace a letter A by a letter B\n")
		elif ((cmd.lower()).split())[0] == "swap" :			# swap input
			cmd = ((cmd.lower()).split())
			if len(cmd) == 3:
				if len(cmd[1]) == len(cmd[2]):
					changed_index, changed_letters, changed_letters_in, text = menu.swap(cmd[1], cmd[2], changed_index, changed_letters, changed_letters_in, text)
					menu.clear(text, changed_index, replaced_letters)

		elif cmd.lower() == "frequency":					# frequency input
			menu.frequency(original_text)
		elif ((cmd.lower()).split())[0] == "find" :			# find input
			cmd = ((cmd.lower()).split())
			if len(cmd) == 2:
				found = menu.find(cmd[1].lower(), "")
				print("\nFound : \n")
				for word in found:
					print(word)
				print("\n")
			elif len(cmd) == 3:
				if len(cmd[1]) == len(cmd[2]) :
					found = menu.find(cmd[1].lower(), cmd[2].lower())
					print("\nFound : \n")
					for word in found:
						print(word)
					print("\n")
				else:
					print(Color.WHITE+"\nFind usage : find <cword> <clear_letters> ... Find a ciphered word in a word list\n")
			else:
				print(Color.WHITE+"\nFind usage : find <cword> <clear_letters> ... Find a ciphered word in a word list\n")
		elif cmd.lower() == "original" : 					# original input
				print("\n"+original_text+"\n")
		elif cmd.lower() == "restart":						# restart input
			text = original_text
			changed_index = []
			changed_letters = []
			changed_letters_in = []
			replaced_letters = list(string.ascii_uppercase)
			menu.clear(text, changed_index, replaced_letters)
		elif cmd.lower() == "exit" :						# exit input
			menu.exit()
