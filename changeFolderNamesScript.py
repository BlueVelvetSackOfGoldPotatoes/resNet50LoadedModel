import re
import os

def main():
    for root, dirs, files in os.walk('Images'):
        for dir in dirs:
            # Get directory name
            # Remove every character except letters
            new_string = re.sub(r'^.*?-', '', dir)

            # Rename the directory
            os.rename('Images/' + dir, 'Images/' + new_string) 

if __name__ == '__main__':
    main()
