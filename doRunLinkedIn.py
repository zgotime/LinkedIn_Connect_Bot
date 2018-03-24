import pandas as pd
import subprocess, sys, os
import argparse
import re
import time


# Bot for getting friends in LinkedIn.
# Author: Austin
# Requirements: Python 3+, iMacros, and Firefox on Windows


def inicio():
    os.system("cls")
    print(' ----------------------------- Help --------------------------------------')
    print('  # ')
    print('  # ')
    print('  # usage: --version {v1, v2} (specify the version for different running mode.')
    print('  # usage: --file fileName (the input csv file from crunbase.')
    print('  # usage: --help (more info about the usage)')
    print('  # ')
    print(' -------------------------------------------------------------------------')


# replace URL in iMacro file
def replaceCompany(version, company):
    filepath = r"C:\Users\username\Documents\iMacros\Macros\MacroLinkedinV1.iim"

    with open(filepath) as f:
        lines = f.readlines()

    # prepare new link
    newLink1 = r"""https://www.linkedin.com/search/results/people/?company="""
    if version == 'v1':
        newLink2 = r"""&facetGeoRegion=%5B%22us%3A0%22%5D&facetNetwork=%5B%22S%22%2C%22O%22%5D&origin=FACETED_SEARCH"""
    if version == 'v2':
        newLink2 = r"""&facetGeoRegion=%5B%22us%3A0%22%5D&facetNetwork=%5B%22S%22%2C%22O%22%5D&origin=FACETED_SEARCH&title=CEO"""
    companyName = re.sub(" ", "%20", company)
    newLink = newLink1 + companyName + newLink2

    print("company name: " + company)

    # replace
    regex = re.compile(r'https://www.linkedin.com.*')
    for i in range(5, 19):
        lines[i] = regex.sub(newLink, lines[i])

    # save back to file
    with open(filepath, 'w') as fo:
        for line in lines:
            fo.write(line)


try:
    # parsing arguments
    parser = argparse.ArgumentParser(description='Bot for adding friends in LinkedIn.')
    parser.add_argument('-v', '--version', choices=['v1', 'v2'], default='v1', help='version is either v1 or v2.')
    parser.add_argument('-t', '--time', default=300, help='adding time for each company.')
    #    parser.add_argument('-p', '--position', default='CEO', help='the positiion or title.')
    parser.add_argument('-f', '--file', help='the input csv file from crunbase.')

    args = parser.parse_args()

    #    curFilePath = os.path.dirname(os.path.realpath(vars(args)['file'])) + "/" + vars(args)['file']
    curFilePath = os.path.dirname(os.path.realpath(vars(args)['file'])) + "\\" + vars(args)['file']
    #    print (curPath)

    # read csv
    data = pd.read_csv(curFilePath, sep=",")
    df = pd.DataFrame(data=data)

    size = df['Organization Name'].size

    # loop for calling sub-process
    for i in range(0, size):
        companyName = df.at[i, 'Organization Name']
        replaceCompany(vars(args)['version'], companyName)



        proc = subprocess.call([r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe', '-new-tab',
                                    'imacros://run/?m=MacroLinkedinV1.iim'])
            #time.sleep(30)
            #subprocess.Popen.kill(proc)

        # version 2
        #if vars(args)['version'] == 'v2':
        #    # replace position
        #    replacePosition(vars(args)['position'], curFilePath)
        #    proc = subprocess.call([r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe', '-new-tab',
        #                            'imacros://run/?m=MacroLinkedinV2.iim'])
        #    time.sleep(vars(args)['time'])
        #    subprocess.Popen.kill(proc)

except IndexError:
    inicio()


