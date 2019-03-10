import argparse #for parsing command line arguments
import nltk
import os #for checking if file or directory exists
import glob #for finding files in directory
import shutil #for copying files

#inputfiles = []

def main(args_input, args_output, args_names, args_genders, args_dates, args_addresses, args_phones):
    input_files = inputfiles(args_input)
    outputfiles(input_files,args_output)
    print("args_names: " + str(args_names))
    print("args_genders: " + str(args_genders))

def inputfiles(args_input):
    input_files = []
    for input in args_input:
        for file in glob.glob(input):
            #print(file)
            input_files.append(file)
    return input_files

def outputfiles(input_files, args_output):
    cwd = os.getcwd()
    output_directory = cwd + '/' + args_output
    if not os.path.exists(output_directory):
        print("directory NOT exist")
        os.mkdir(output_directory)
    else:
        print("directory exists")
    for file in input_files:
        original_file_path = cwd + '/' + file
        redacted_file_name = os.path.basename(original_file_path) + ".redacted"
        redacted_file_path = output_directory + redacted_file_name
        #print("redacted_file_path = " + redacted_file_path)
        if os.path.exists(original_file_path):
            #print("file exists")
            shutil.copy(original_file_path, redacted_file_path)
        else:
            print("file NOT exist: " + cwd + '/' + file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, action="append",required=True,help="File extension to be read.")
    parser.add_argument("--names", action='store_true',help="Redact names.")
    parser.add_argument("--genders", action='store_true',help="Redact genders.")
    parser.add_argument("--dates", action='store_true',help="Redact dates.")
    parser.add_argument("--addresses", action='store_true',help="Redact addresses.")
    parser.add_argument("--phones", action='store_true',help="Redact phone numbers.")
    parser.add_argument("--concept", type=str,help="Redact concept.")
    parser.add_argument("--output", type=str,help="Output location.")
    parser.add_argument("--stats", type=str,help="Redaction stats.")    
    args = parser.parse_args()
    if args.input:
        main(args.input, args.output, args.names, args.genders, args.dates, args.addresses, args.phones)
