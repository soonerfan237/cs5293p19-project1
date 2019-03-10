import argparse
import nltk
import os
import glob

def main(inputs):
    #cwd = os.getcwd()
    #for file in os.listdir(cwd):
    #    if file.endswith():
    #        print(os.path.join(cwd, file))
    #print(input)
    for input in inputs:
        for file in glob.glob(input):
            print(file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, action="append",required=True,help="File extension to be read.")
    parser.add_argument("--names", type=str,help="Redact names.")
    parser.add_argument("--dates", type=str,help="Redact dates.")
    parser.add_argument("--addressess", type=str,help="Redact addresses.")
    parser.add_argument("--phones", type=str,help="Redact phone numbers.")
    parser.add_argument("--concept", type=str,help="Redact concept.")
    parser.add_argument("--output", type=str,help="Output location.")
    parser.add_argument("--stats", type=str,help="Redaction stats.")    
    args = parser.parse_args()
    if args.input:
        main(args.input)
