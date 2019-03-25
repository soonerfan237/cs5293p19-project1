import argparse #for parsing command line arguments
import nltk #for text processing
import os #for checking if file or directory exists
import glob #for finding files in directory
import shutil #for copying files
import re #for regular expressions
#import numpy
import sys #used for stderr output

redacted_names = []
redacted_genders = []
redacted_dates = []
redacted_addresses = []
redacted_phones = []
redacted_concepts = []
redacted_files = [] #array of all files processed 

def main(args_input, args_output, args_names, args_genders, args_dates, args_addresses, args_phones, args_stats):
    input_files = inputfiles(args_input)
    file_count = 0
    for input_file in input_files:
        original_file_path = os.getcwd() + '/' + input_file
        #redacted_stats.append(original_file_path)
        #print("FILE: " + original_file_path)
        with open(original_file_path, 'r') as originalfile:
            originaltext = originalfile.read()
            redactedtext = originaltext
            if len(redactedtext) > 1:
                #print(originaltext)
                #print(str("file_count = " + str(file_count)))
                redacted_files.append(original_file_path)
                redacted_names.append(0)
                redacted_genders.append(0)
                redacted_dates.append(0)
                redacted_addresses.append(0)
                redacted_phones.append(0)
                redacted_concepts.append(0)
                print("FILE: " + original_file_path)
                if (args_names):
                    redactedtext = redact_names(redactedtext,file_count)
                if(args_genders):
                    redactedtext = redact_genders(redactedtext,file_count)
                if(args_dates):
                    redactedtext = redact_dates(redactedtext,file_count)
                if(args_addresses):
                    redactedtext = redact_addresses(redactedtext,file_count)
                if(args_phones):
                    redactedtext = redact_phones(redactedtext,file_count)
                file_count = file_count + 1
        outputfile(input_file,args_output, redactedtext)
    #print("args_stats = " + args_stats)
    if(args_stats == 'stdout'):
        outputstats_stdout()
    elif(args_stats == 'stderr'):
        outputstats_stderr()
    elif(len(args_stats) > 0):
        outputstats_file(args_stats)

def inputfiles(args_input):
    input_files = []
    for input in args_input:
        for file in glob.glob(input):
            #print(file)
            input_files.append(file)
    return input_files

def replace(match):
    #print("match.group() = " + match.group())
    redacted_string = ""
    for i in range(0,len(match.group())):
        if match.group()[i] == " ":
            redacted_string = redacted_string + " "
        else:
            redacted_string = redacted_string + "X"
    return redacted_string

def redact_names(input_string,file_count):
    print("REDACTING NAMES...")
    #print("file_count = " + str(file_count))
    redacted_names[file_count] = 0
    output_string = input_string
    sentences = nltk.sent_tokenize(output_string)
    for sentence in sentences:
        #print("SENTENCE: " + sentence)
        redacted_sentence = sentence
        words = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(words)
        chunks = nltk.ne_chunk(tags)
        for chunk in chunks:
            if isinstance(chunk,nltk.tree.Tree): 
                if chunk.label() == 'PERSON':
                    #print(chunk)
                    redacted_names[file_count] = redacted_names[file_count] + 1
                    for wordtag in chunk:
                        #print(wordtag[0])
                        redacted_sentence = redacted_sentence.replace(wordtag[0],'X' * len(wordtag[0]))
                        #sentence = redacted_sentence
                        output_string = output_string.replace(sentence,redacted_sentence)
        #print("REDACTED: " + redacted_sentence)
    return output_string

def redact_genders(input_string,file_count):
    print("REDACTING GENDERS...")
    redacted_genders[file_count] = 0
    output_string = input_string
    matches = re.findall(r'male|female|\bboy\b|\bgirl\b|\bman\b|woman|father|mother|\bson\b|daughter|niece|nephew|grandpa|grandma|uncle|aunt', output_string,flags=re.I)
    redacted_genders[file_count] = redacted_genders[file_count] + len(matches)
    output_string = re.sub(r'male|female|\bboy\b|\bgirl\b|\bman\b|woman|father|mother|\bson\b|daughter|niece|nephew|grandpa|grandma|uncle|aunt',replace,output_string,flags=re.I)
    matches = re.findall(r'\bhis\b|\bhim\b|\bher\b|\bhe\b|\bshe\b|\bmr.|\bmrs.|\bms.', output_string,flags=re.I)
    redacted_genders[file_count] = redacted_genders[file_count] + len(matches)
    output_string = re.sub(r'\bhis\b|\bhim\b|\bher\b|\bhe\b|\bshe\b|\bmr.|\bmrs.|\bms.',replace,output_string,flags=re.I)
    return output_string

def redact_dates(input_string,file_count):
    print("REDACTING DATES...")
    redacted_dates[file_count] = 0
    output_string = input_string
    matches = re.findall(r'\d\d?[/\-]\d\d?[/\-]\d\d\d?\d?',output_string)
    redacted_dates[file_count] = redacted_dates[file_count] + len(matches)
    output_string = re.sub(r'\d\d?[/\-]\d\d?[/\-]\d\d\d?\d?',replace,output_string)

    matches = re.findall(r'monday|tuesday|wednesday|thursday|friday|saturday|sunday',output_string, flags=re.I)
    redacted_dates[file_count] = redacted_dates[file_count] + len(matches)
    output_string = re.sub(r'monday|tuesday|wednesday|thursday|friday|saturday|sunday',replace,output_string, flags=re.I)
    
    matches = re.findall(r'\d?\d? ?(january|february|march|april|may|june|july|august|september|october|november|december|\bjan\b|\bfeb\b|\bmar\b|\bapr\b|\bmay\b|\bjun\b|\bjul\b|\baug\b|\bsep\b|\boct\b|\bnov\b|\bdec\b) ?\d?\d?,? ?\d?\d?\d?\d?',output_string,flags=re.I)
    redacted_dates[file_count] = redacted_dates[file_count] + len(matches)
    output_string = re.sub(r'\d?\d? ?(january|february|march|april|may|june|july|august|september|october|november|december|\bjan\b|\bfeb\b|\bmar\b|\bapr\b|\bmay\b|\bjun\b|\bjul\b|\baug\b|\bsep\b|\boct\b|\bnov\b|\bdec\b) ?\d?\d?,? ?\d?\d?\d?\d?',replace,output_string,flags=re.I)
    
    matches = re.findall(r'january|february|march|april|may|june|july|august|september|october|november|december',output_string, flags=re.I)
    redacted_dates[file_count] = redacted_dates[file_count] + len(matches)
    output_string = re.sub(r'january|february|march|april|may|june|july|august|september|october|november|december',replace,output_string, flags=re.I)
    
    return output_string

def redact_addresses(input_string,file_count):
    print("REDACTING ADDRESSES...")
    redacted_addresses[file_count] = 0
    output_string = input_string
    matches = re.findall(r'\b\d\d?\d?\d?\d? \w+ (street|st|hill|avenue|ave|way|boulevard|blvd|road|rd|drive|dr|lane|ln|grove|place|pl|square|sq)\b',output_string,flags=re.I)
    #print(matches)
    redacted_addresses[file_count] = redacted_addresses[file_count] + len(matches)
    output_string = re.sub(r'\b\d\d?\d?\d?\d? \w+ (street|st|hill|avenue|ave|way)\b',replace,output_string,flags=re.I)
    return output_string

def redact_phones(input_string,file_count):
    print("REDACTING PHONES...")
    redacted_phones[file_count] = 0
    output_string = input_string
    matches = re.findall(r'\(?\d?\d?\d?\)? ?\d\d\d-\d\d\d\d',output_string)
    #print(matches)
    redacted_phones[file_count] = redacted_phones[file_count] + len(matches)
    output_string = re.sub(r'\(?\d?\d?\d?\)? ?\d\d\d-\d\d\d\d',replace,output_string)
    return output_string

def outputfile(original_file, args_output, redactedtext):
    #print("REDACTED:")
    print(redactedtext)
    cwd = os.getcwd()
    output_directory = cwd + '/' + args_output
    if not os.path.exists(output_directory):
        #print("directory NOT exist")
        os.mkdir(output_directory)
    #else:
        #print("directory exists")
    original_file_path = cwd + '/' + original_file
    redacted_file_name = os.path.basename(original_file_path) + ".redacted"
    redacted_file_path = output_directory + redacted_file_name
    with open(redacted_file_path, 'w') as redacted_file:
        redacted_file.write(redactedtext)

def outputstats_file(file_name):
    print("SAVING STATS TO FILE: " + file_name)
    cwd = os.getcwd()
    outputstats_directory = cwd + '/' + file_name
    #if not os.path.isfile(outputstats_directory):
        #print("directory NOT exist")
        #os.mkdir(outputstats_directory)
    with open(outputstats_directory, 'w') as outputstats_file:
        outputstats_file.write("") #clearing file contents
    with open(outputstats_directory, 'a+') as outputstats_file:
        outputstats_file.write("==============REDACTION STATISTICS================\n")
        total_redacted_names = 0
        total_redacted_genders = 0
        total_redacted_dates = 0
        total_redacted_addresses = 0
        total_redacted_phones = 0
        total_redacted_concepts = 0
        for i in range(0,len(redacted_files)):
            total_redacted_names = total_redacted_names + redacted_names[i]
            total_redacted_genders = total_redacted_genders + redacted_genders[i]
            total_redacted_dates = total_redacted_dates + redacted_dates[i]
            total_redacted_addresses = total_redacted_addresses + redacted_addresses[i]
            total_redacted_phones = total_redacted_phones + redacted_phones[i]
            total_redacted_concepts = total_redacted_concepts + redacted_concepts[i]
            outputstats_file.write("FILE: " + redacted_files[i] + "\n")
            outputstats_file.write(str(redacted_names[i]) + " names redacted.\n")
            outputstats_file.write(str(redacted_genders[i]) + " gender words redacted.\n")
            outputstats_file.write(str(redacted_dates[i]) + " dates redacted.\n")
            outputstats_file.write(str(redacted_addresses[i]) + " addresses redacted.\n")
            outputstats_file.write(str(redacted_phones[i]) + " phone numbers redacted.\n")
            outputstats_file.write(str(redacted_concepts[i]) + " concepts redacted.\n")
            outputstats_file.write("==============================================\n")
        outputstats_file.write("TOTALS:\n")
        outputstats_file.write(str(total_redacted_names) + " names redacted.\n")
        outputstats_file.write(str(total_redacted_genders) + " gender words redacted.\n")
        outputstats_file.write(str(total_redacted_dates) + " dates redacted.\n")
        outputstats_file.write(str(total_redacted_addresses) + " addresses redacted.\n")
        outputstats_file.write(str(total_redacted_phones) + " phone numbers redacted.\n")
        outputstats_file.write(str(total_redacted_concepts) + " concepts redacted.\n")

def outputstats_stderr():
    print(" ",file=sys.stderr)
    print(" ",file=sys.stderr)
    print("==============REDACTION STATISTICS================",file=sys.stderr)
    total_redacted_names = 0
    total_redacted_genders = 0
    total_redacted_dates = 0
    total_redacted_addresses = 0
    total_redacted_phones = 0
    total_redacted_concepts = 0
    for i in range(0,len(redacted_files)):
        total_redacted_names = total_redacted_names + redacted_names[i]
        total_redacted_genders = total_redacted_genders + redacted_genders[i]
        total_redacted_dates = total_redacted_dates + redacted_dates[i]
        total_redacted_addresses = total_redacted_addresses + redacted_addresses[i]
        total_redacted_phones = total_redacted_phones + redacted_phones[i]
        total_redacted_concepts = total_redacted_concepts + redacted_concepts[i]
        print("FILE: " + redacted_files[i],file=sys.stderr)
        print (str(redacted_names[i]) + " names redacted.",file=sys.stderr)
        print (str(redacted_genders[i]) + " gender words redacted.",file=sys.stderr)
        print (str(redacted_dates[i]) + " dates redacted.",file=sys.stderr)
        print (str(redacted_addresses[i]) + " addresses redacted.",file=sys.stderr)
        print (str(redacted_phones[i]) + " phone numbers redacted.",file=sys.stderr)
        print (str(redacted_concepts[i]) + " concepts redacted.",file=sys.stderr)
        print("==============================================",file=sys.stderr)
    print("TOTALS:",file=sys.stderr)
    print (str(total_redacted_names) + " names redacted.",file=sys.stderr)
    print (str(total_redacted_genders) + " gender words redacted.",file=sys.stderr)
    print (str(total_redacted_dates) + " dates redacted.",file=sys.stderr)
    print (str(total_redacted_addresses) + " addresses redacted.",file=sys.stderr)
    print (str(total_redacted_phones) + " phone numbers redacted.",file=sys.stderr)
    print (str(total_redacted_concepts) + " concepts redacted.",file=sys.stderr)

def outputstats_stdout():
    print(" ")
    print(" ")
    print("==============REDACTION STATISTICS================")
    total_redacted_names = 0
    total_redacted_genders = 0
    total_redacted_dates = 0
    total_redacted_addresses = 0
    total_redacted_phones = 0
    total_redacted_concepts = 0
    for i in range(0,len(redacted_files)):
        total_redacted_names = total_redacted_names + redacted_names[i]
        total_redacted_genders = total_redacted_genders + redacted_genders[i]
        total_redacted_dates = total_redacted_dates + redacted_dates[i]
        total_redacted_addresses = total_redacted_addresses + redacted_addresses[i]
        total_redacted_phones = total_redacted_phones + redacted_phones[i]
        total_redacted_concepts = total_redacted_concepts + redacted_concepts[i]
        print("FILE: " + redacted_files[i])
        print (str(redacted_names[i]) + " names redacted.")
        print (str(redacted_genders[i]) + " gender words redacted.")
        print (str(redacted_dates[i]) + " dates redacted.")
        print (str(redacted_addresses[i]) + " addresses redacted.")
        print (str(redacted_phones[i]) + " phone numbers redacted.")
        print (str(redacted_concepts[i]) + " concepts redacted.")
        print("==============================================")
    print("TOTALS:")
    print (str(total_redacted_names) + " names redacted.")
    print (str(total_redacted_genders) + " gender words redacted.")
    print (str(total_redacted_dates) + " dates redacted.")
    print (str(total_redacted_addresses) + " addresses redacted.")
    print (str(total_redacted_phones) + " phone numbers redacted.")
    print (str(total_redacted_concepts) + " concepts redacted.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, action="append",required=True,help="File extension to be read.")
    parser.add_argument("--names", action='store_true',help="Redact names.")
    parser.add_argument("--genders", action='store_true',help="Redact genders.")
    parser.add_argument("--dates", action='store_true',help="Redact dates.")
    parser.add_argument("--addresses", action='store_true',help="Redact addresses.")
    parser.add_argument("--phones", action='store_true',help="Redact phone numbers.")
    parser.add_argument("--concept", type=str,help="Redact concept.")
    parser.add_argument("--output", type=str,required=True,help="Output location.")
    parser.add_argument("--stats", type=str,help="Redaction stats.")    
    args = parser.parse_args()
    if args.input:
        main(args.input, args.output, args.names, args.genders, args.dates, args.addresses, args.phones, args.stats)
