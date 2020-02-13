from CrawlCyclingtips import Crawler
from url_list import urls
from Analyse import Analyse
import argparse
import warnings
import colorama
from colorama import Fore, Style

def main():
    # texts
    print(Fore.BLUE + 'ENDUCO' + Style.RESET_ALL + "----" + Fore.RED + 'CRAWLER')
    print(Style.RESET_ALL)
    print(Fore.GREEN)

    parser = argparse.ArgumentParser()
    parser.add_argument('-F','--from_year',help='From the year you wish to begin analysis',type=int,default='2009')
    parser.add_argument('-T','--to_year',help='To the year you wish to end analysis',type=int,default='2020')
    parser.add_argument('-f','--from_month',help='From the month you wish to begin analysis',type=int,default='01')
    parser.add_argument('-t','--to_month',help='To the month you wish to end analysis',type=int,default='12')
    parser.add_argument('-n','--n_topics',help='Number of topics you wish to model',type=int,default='05')
    args = parser.parse_args()
    warnings.filterwarnings('ignore')
    Crawler(urls)
    print('UPDATED AND READY')
    Analyse(args.from_year,args.to_year,args.from_month,args.to_month,args.n_topics)

if __name__ == "__main__":

    # Pyinstaller fix
    multiprocessing.freeze_support()

    # ready
    main()
