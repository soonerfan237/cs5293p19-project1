import argparse #for parsing command line arguments
import nltk
import os #for checking if file or directory exists
import glob #for finding files in directory
import shutil #for copying files

def main(args_input, args_output, args_names, args_genders, args_dates, args_addresses, args_phones):
    input_files = inputfiles(args_input)
    for input_file in input_files:
        original_file_path = os.getcwd() + '/' + input_file
        print("FILE: " + original_file_path)
        with open(original_file_path, 'r') as originalfile:
            originaltext = originalfile.read()
            redactedtext = originaltext
            if len(redactedtext) > 1:
                #print(originaltext)
                if (args_names):
                    redactedtext = redact_names(redactedtext)
                if(args_genders):
                    redactedtext = redact_genders(redactedtext)
                if(args_dates):
                    redactedtext = redact_genders(redactedtext)
                if(args_addresses):
                    redactedtext = redact_genders(redactedtext)
                if(args_phones):
                    redactedtext = redact_genders(redactedtext)
        outputfile(input_file,args_output, redactedtext)

def inputfiles(args_input):
    input_files = []
    for input in args_input:
        for file in glob.glob(input):
            #print(file)
            input_files.append(file)
    return input_files

def redact_names(input_string):
    print("REDACTING NAMES...")
    output_string = input_string
    tokens = nltk.word_tokenize(output_string)
    #tokens
    tagged = nltk.pos_tag(tokens)
    for tag in tagged:
        print(tag)
    return output_string

def redact_genders(input_string):
    print("REDACTING GENDERS...")
    output_string = input_string
    return output_string

def redact_dates(input_string):
    print("REDACTING DATES...")
    output_string = input_string
    return output_string

def redact_addresses(input_string):
    print("REDACTING ADDRESSES...")
    output_string = input_string
    return output_string

def redact_phones(input_string):
    print("REDACTING PHONES...")
    output_string = input_string
    return output_string

def outputfile(original_file, args_output, redactedtext):
    cwd = os.getcwd()
    output_directory = cwd + '/' + args_output
    if not os.path.exists(output_directory):
        print("directory NOT exist")
        os.mkdir(output_directory)
    else:
        print("directory exists")
    original_file_path = cwd + '/' + original_file
    redacted_file_name = os.path.basename(original_file_path) + ".redacted"
    redacted_file_path = output_directory + redacted_file_name
    with open(redacted_file_path, 'w') as redacted_file:
        redacted_file.write(redactedtext)

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
        main(args.input, args.output, args.names, args.genders, args.dates, args.addresses, args.phones)
