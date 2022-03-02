from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator, color_print
import subprocess as sp
import os
from pyfiglet import Figlet
import textract
import subprocess


custom_style_1 = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def reader(path):
    file_path = open(path,"r")
#    print(path)
    file_read = file_path.read()
    file_split = file_read.split("\n")
    return(file_split)

    #config_parse = input a config field Ea. "Menu name", and will output
    #list of result after the =, Ea. ["Menu 1","Menu 2"]
def config_parser(pick):
    #Might need to change this to the absolute path to the config
    config_list = reader("/config")
    pick_list = []
    for i in range(len(config_list)):
        if pick in config_list[i]:
            pick_list.append(config_list[i].split("=")[1])
    return(pick_list)
#file_search= input str file path, and file format.
#Output at list of files with path.
#Ea. in= ~/Desktop/notes,".py" , out= ["../Destop/notes/script.py","...]

#Extract all fields from config file for use in run_table
#extra fields can be added, field_name = config[i+3...(n+1)].split("=")[1]
#will split from = in config and put value on ŕun_table
#return value and dict value will need to be added
def config_extract(pick):
    #Might need to change this to the absolute path to the config
    config = reader("/config")
    for i in range(len(config)):
        if "=" in config[i]:
            if pick == config[i].split("=")[1]:
                path = config[i+1].split("=")[1]
                format = config[i+2].split("=")[1]
                program = config[i+3].split("=")[1]
    return(path,format,program)


#parses for files from root folder stated in config
#input: "~/Desktop/notes",".txt"
def file_search(folder_path,file_format):
    f = (folder_path)
    file_list = []
    filenames= []
    for root,dirs,files in os.walk(f):
        for filename in files:

            if filename[len(filename)-len(file_format):] == file_format:
                file_list.append(os.path.join(root, filename))
            #check if files are text files, using cmd files.
            if filename.find(".") == -1 and file_format == ".txt":
                #print(root+"/"+filename)
                process = subprocess.Popen(["file",root+"/"+filename], stdout=subprocess.PIPE)
                out,err = process.communicate()
                conv = str(out,"UTF-8")
                tester = conv[conv.find(":"):]
                if "text" in tester:
                    file_list.append(os.path.join(root, filename))
                    #print(os.path.join(root, filename))
#                file_list.append(root+"/"+files[i])
    return(file_list)
#output: ["~/Desktop/notes/file1.txt","~/Desktop/notes/file1.txt",...]

#input: "~/Desktop/notes/note.txt","xed"
def file_open(file_name,program):
    sp.Popen(program,file_name)

#file_parser is where the parser is chosen, based on file format extension.
#input: "../Desktop/notes/notefile.txt",".txt","i want to find"
def file_parser(file_path,format,search_frase):
    if format == ".txt":
        parse_result = txt_searcher(file_path,search_frase)
    if format == ".py":
        parse_result = universal_searcher(file_path,search_frase)
    if format == ".pdf":
        parse_result = pdf_searcher(file_path,search_frase)

#---^-------Insert new parsers here--------^-------
#output needs to be a list with strings containing search word
    result_encode = [{"name":"%s"%file_path}]
    for i in range(len(parse_result)):
        result_encode.append(Separator(parse_result[i]))
    return(result_encode)
#output: Ex. [{"name":"path/and/filename.txt"},Separator("line_fom_search"),Separator("line_fom_search")]
#amount of 'Separator("line_fom_search")' is dependent on results.

def pdf_searcher(file_path,search_frase):
    hit_list = []
    r_file = textract.process(file_path)
    parsed_file = str(r_file,"utf-8").split("\n")
    for i in range(len(parsed_file)):
        if search_frase.lower() in parsed_file[i].lower():
            hit_list.append("%s: "%i+parsed_file[i])
#    r_file.close()
    return(hit_list)

def txt_searcher(path,search_frase):
    hit_list = []
    file_path = open(path,"rb")
    file_read = file_path.read()
    try:
        parsed_file = str(file_read, "raw_unicode_escape").split("\n")
    except:
        parsed_file = "**"
        print("read error:"+path)
    for i in range(len(parsed_file)):
        if search_frase.lower() in parsed_file[i].lower():
            hit_list.append("%s: "%i+parsed_file[i])
    return(hit_list)

#universal_searcher is the regular file open(,"r") function with the made reader() function.
#input: "../Desktop/notes/notefile.py","i want to find"
def universal_searcher(file_path,search_frase):
    hit_list = []
    parsed_file = reader(file_path)
    for i in range(len(parsed_file)):
        if search_frase.lower() in parsed_file[i].lower():
            print(parsed_file[i])
            hit_list.append("%s: "%i+parsed_file[i])
    return(hit_list)
#output: ["34: i want to find this in one of my note files","45: i want to find this also"]

def menu_start():
    menu_list = config_parser("Menu name")
    menu_index = [
        {
            "type": "list",
            "name": "choice",
            "message": "What category of notes are you searching?",
            "choices": menu_list,
        }
    ]
    return(menu_index)

def menu_pick(path,file_format):
    file_list = file_search(path,file_format)
    for i in range(len(file_list)):
        file_list[i] = "%s: "%(i+1)+file_list[i]
    file_list[:0] = ["[:.Search.:]","[:.Back.:]"]
    menu_check = [
        {
            "type": "list",
            "name": "choice",
            "message": "%s %s files were found. Press Enter to select." % (len(file_list)-2, file_format),
            "choices": file_list,
        }
    ]
    return(menu_check)

#input: Ex. "../Desktop/notes",".txt". Path to root folder and file format_pick
#Taken previous choice.
def menu_search(path,file_format):
    search = input("Search{}:")
    file_list = file_search(path,file_format)
    result_list = []
    file_counter = 0
    for i in range(len(file_list)):
        print(len(file_list),"/",i,"scanning: "+file_list[i][file_list[i].rfind("/"):],end="\r")
        file_parsed = file_parser(file_list[i],file_format,search)
        if len(file_parsed) != 1:
            file_counter += 1
            file_parsed[0]["name"] = "%s: "%file_counter+file_parsed[0]["name"]
            for y in range(len(file_parsed)):
                result_list.append(file_parsed[y])
    if len(result_list) == 0:
        type = "list"
        message = "0 %s files with '%s' was found" % (file_format,search)
        result_list[:0] = ["[:.Search.:]","[:.Back.:]"]
#        result_list.append("[:.Search.:]")
#        result_list.append("[:.Back.:]")
    else:
        result_list.append(Separator(" "))
        type = "checkbox"
        message = "%s %s files with '%s' was found" %(file_counter,file_format,search)
        result_list[:0] = {"name":"[:.Search.:]"},{"name":"[:.Back.:]"}
    menu_check = [
        {
            "type": type,
            "name": "choice",
            "message": message,
            "choices": result_list,
        }
    ]
#    print(menu_check)
    return(menu_check)
#output: if for checkbox, Ex. [{"name":"path/and/filename.txt"},Separator("line_fom_search")]
#output: if for list, Ex.["Regular","list","object"]

print("By Dj4anx")
titelF = Figlet(font="slant")
print(titelF.renderText("{Oo} |Note              '''''    |Search"))

#----Main loop-----
run_table = {"pick":"","file_path":"","format":"","program":""}
while True:
    if len(run_table["pick"]) == 0:
        start_run = prompt(menu_start(), style=custom_style_1)
        pprint(start_run)
        run_table["file_path"],run_table["format"],run_table["program"] = config_extract(start_run["choice"])
        run_table["pick"] = start_run["choice"]
    if len(run_table["pick"]) != 0:
        if run_table["pick"] == "[:.Search.:]":
            search_run = prompt(menu_search(run_table["file_path"],run_table["format"]), style=custom_style_1)
#            print(search_run["choice"])
            if search_run["choice"] == "[:.Search.:]" or search_run["choice"] == "[:.Back.:]":
                run_table["pick"] = search_run["choice"]
            else:
                run_table["pick"] = search_run["choice"][0]
                for i in range(len(search_run["choice"])):
                    if search_run["choice"][i] == "[:.Search.:]" or search_run["choice"][i] == "[:.Back.:]":
                        trash = "nothing"
                    else:
                        sp.Popen([run_table["program"],search_run["choice"][i][search_run["choice"][i].find("/"):]])
#                        print(search_run["choice"][i][search_run["choice"][i].find("/"):])
        elif run_table["pick"] == "[:.Back.:]":
            run_table = {"pick":"","file_path":"","format":"","program":""}
        else:
            pick_run = prompt(menu_pick(run_table["file_path"],run_table["format"]), style=custom_style_1)
            pprint(pick_run)
            run_table["pick"] = pick_run["choice"]
