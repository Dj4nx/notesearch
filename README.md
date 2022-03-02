# notesearch

Notesearch is a small program that can help index and search notes with different formats.
This is the first fairly functioning version of a personal pet project so more info will come.

As a person who writes a lot of notes and horde training material, i often loose track of where i put this. Therefor i've made a little linux commandline program
that can index and search all my different text files.

With Python and various libraries like PyInuirer, textract and pyfiglet, i've made a simple interface for easy and quick overview of all your notes/"intelligence" data.
With custom coded parsers, called searchers, it will parse an look for search terms. It will then give you are list of the files, and the line in where a search term is found and the option to open this file in a defined program.
The config file will have to be filled out in order to define the name in the menue, the root folder from where a recursive search will be done, file format and a program in which you wish the file to be opened with.
Multiple additions can be made to the config file, just copy the fields.


A custom searcher is easy to make and integrate, with the creation of a small function and a addition if statement in the "file_parser()" function.
For now the program can parse .txt/text files with no file extention, .py and .pdf.

Critique and ideas are always more than welcome.
Dj4nx
