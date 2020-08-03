# coding: utf-8

import sys
import string
from os import system, path

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
replaced_letters = list(string.ascii_uppercase) # New letters + others
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
	def auto():
		print("ok")
	def exit():												# exit function
		print("\n")
		exit()

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
				if cmd[1].lower() in string.ascii_lowercase and cmd[2].lower() in string.ascii_lowercase :
					if cmd[1] in changed_letters:
						print(Color.WHITE+"You already changed the letter '"+cmd[1].lower()+"' in '"+changed_letters_in[changed_letters.index(cmd[1])]+"'")
						continue
					elif cmd[2] in changed_letters_in:
						print(Color.WHITE+"You already changed the letter '"+changed_letters[changed_letters_in.index(cmd[2])]+"' in '"+cmd[2].lower()+"'")
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
