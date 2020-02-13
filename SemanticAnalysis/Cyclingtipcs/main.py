from CrawlCyclingtips import Crawler
from url_list import urls
from Analyse import Analyse
import argparse
import warnings

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    parser = argparse.ArgumentParser()
    parser.add_argument('-F','--from_year',help='From the year you wish to begin analysis',type=int,default='2009')
    parser.add_argument('-T','--to_year',help='To the year you wish to end analysis',type=int,default='2020')
    parser.add_argument('-f','--from_month',help='From the month you wish to begin analysis',type=int,default='01')
    parser.add_argument('-t','--to_month',help='To the month you wish to end analysis',type=int,default='12')
    parser.add_argument('-n','--n_topics',help='Number of topics you wish to model',type=int,default='05')
    args = parser.parse_args()
    # Crawler(urls)
    print('UPDATED AND READY')
    Analyse(args.from_year,args.to_year,args.from_month,args.to_month,args.n_topics)
