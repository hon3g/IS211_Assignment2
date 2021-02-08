import argparse
import urllib.request
import logging
import datetime
import ssl
import sys


def downloadData(url):
    """Downloads the data"""
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        return urllib.request.urlopen(url).read()
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit()


def processData(content, logger):
    content = content.decode('utf-8').split('\n')[1:-1]
    clean_data = dict()

    for i in range(len(content)):
        line_num = i + 2
        content[i] = content[i].split(',')
        try:
            content[i][2] = datetime.datetime.strptime(content[i][2], '%m/%d/%Y')
            clean_data[content[i][0]] = (content[i][1], content[i][2])
        except ValueError:
            logger.error(f"Error processing line #{line_num} for ID #{content[i][0]}")

    return clean_data


def displayPerson(id, personData):
    try:
        name, date = personData[id]
        print(f'Person #{id} is {name} with a birthday of {date.strftime("%Y-%m-%d")}')
    except KeyError:
        print('No user found with that id')


def main(url):
    print(f"Running main with URL = {url}...")

    logger = logging.getLogger('assignment2')
    logging.basicConfig(filename='error.log', level=logging.ERROR, format='')

    csvData = downloadData(url)
    personData = processData(csvData, logger)

    val = True
    while val > 0:
        try:
            val = int(input('Enter a lookup ID: '))
        except ValueError:
            print('Number only')
            continue
        if val < 1:
            sys.exit()
        displayPerson(str(val), personData)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
