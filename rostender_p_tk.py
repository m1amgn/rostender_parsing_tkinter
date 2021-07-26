import requests
import csv
import re
import tkinter as tk

from bs4 import BeautifulSoup as bs
from tkinter import *



root = tk.Tk()

root['bg'] = "#fafafa"
root.title("Парсинг rostender")
root.geometry("300x100")

# make headers for safe parsing
headers = {'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}

# urls for href in write file function
url_for_href = 'http://rostender.info/'

# urls for url constructor
kwd_reagent = '%F0%E5%E0%E3%E5%ED%F2'
kwd_nalco = 'nalco'
kwd_nalco_ru = '%ED%E0%EB%EA%EE'
kwd_purotech = 'purotech'
kwd_puro_tech = 'puro tech'
kwd_inhibitor = '%E8%ED%E3%E8%E1%E8%F2%EE%F0'
kwd_biocide = '%E1%E8%EE%F6%E8%E4'
kwd_option = '%EE%EF%F2%E8%EE%ED'
kwd_ektoskeil = '%FD%EA%F2%EE%F1%EA%E5%E9%EB'
kwd_aminat = '%E0%EC%E8%ED%E0%F2'


# function wich makes urls list if there is pagination on web site
def url_constructor(kwd, actual_date):
    base_url = f'http://rostender.info/extsearch.php?pgsearch=0&extsearch=2&branch134=on&branch234=on&branch239=on&kwd={kwd}&from={actual_date}&to=&pfrom=&pto='
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('div', attrs={'class': 'b-paging'})
            for integer in pagination:
                integer = integer.find('strong').text
                count = int(integer)
                for i in range(count):
                    url = f'http://rostender.info/extsearch.php?pgsearch={i+1}&extsearch=2&branch134=on&branch234=on&branch239=on&kwd={kwd}&from={actual_date}&to=&pfrom=&pto='
                    if url not in urls:
                        urls.append(url)
            print(f'Количество найденных страниц {len(urls)}')
        except Exception as e:
            print(e)
            pass
    else:
        print(f'ERROR{request.status_code}')
    return urls

# parse function for web site rostender.info which find need information filter information and make dictionary
def rostender_parse(urls, headers):
    tenders_info = []
    for url in urls:
        session = requests.Session()
        request = session.get(url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            try:
                divs = soup.find_all('div', attrs={'class': 'tender-info'})
                for div in divs:
                    title = div.find('a', attrs={'target': '_blank'}).text
                    href_title = div.find('a', attrs={'target': '_blank'})['href']
                    date_information = div.find('div', attrs={'class': 'col-lg-6 text-right'}).text
                    title = ' '.join(title.split())
                    title = title.lower()
                    href_title = ' '.join(href_title.split())
                    date_information = ' '.join(date_information.split())
                    if re.search(r'лед|мед|лёд|бассейн|лаб|анализ|реактив|хозяйственные', title):
                        print(f'Отфильтровано {title}')
                    else:
                        tenders_info.append({
                            'description': title,
                            'href': href_title,
                            'end_date': date_information
                        })
            except Exception as e:
                print(e)
                pass
        else:
            print(f'ERROR {request.status_code}')
    print(f'Статус {request.status_code}')
    print(f'Количество найденных тендеров {len(tenders_info)}')
    return tenders_info

# function which write new csv file every using
def files_writer(tenders_info, file_name):
    with open(f'{file_name}.csv', 'w') as file:
        a_pen = csv.writer(file)
        for info in tenders_info:
            a_pen.writerow((info['description'], url_for_href+info['href'], info['end_date']))



def get_date():
    actual_date = actual_date_str.get()
    print('---------------------------------------\nЗанимаюсь ключевым словом реагент')
    url_reagent = url_constructor(kwd_reagent, actual_date)
    tenders_info = rostender_parse(url_reagent, headers)
    files_writer(tenders_info, 'reagent')

    print('---------------------------------------\nЗанимаюсь ключевым словом Nalco')
    url_nalco = url_constructor(kwd_nalco, actual_date)
    tenders_info = rostender_parse(url_nalco, headers)
    files_writer(tenders_info, 'nalco')

    print('---------------------------------------\nЗанимаюсь ключевым словом Налко')
    url_nalco_ru = url_constructor(kwd_nalco_ru, actual_date)
    tenders_info = rostender_parse(url_nalco_ru, headers)
    files_writer(tenders_info, 'nalco_ru')

    print('---------------------------------------\nЗанимаюсь ключевым словом purotech')
    url_purotech = url_constructor(kwd_purotech, actual_date)
    tenders_info = rostender_parse(url_purotech, headers)
    files_writer(tenders_info, 'purotech')

    print('---------------------------------------\nЗанимаюсь ключевым словом puro tech')
    url_purotech = url_constructor(kwd_puro_tech, actual_date)
    tenders_info = rostender_parse(url_purotech, headers)
    files_writer(tenders_info, 'puro_tech')

    print('---------------------------------------\nЗанимаюсь ключевым словом ингибитор')
    url_inhibitor = url_constructor(kwd_inhibitor, actual_date)
    tenders_info = rostender_parse(url_inhibitor, headers)
    files_writer(tenders_info, 'inhibitor')

    print('---------------------------------------\nЗанимаюсь ключевым словом биоцид')
    url_biocide = url_constructor(kwd_biocide, actual_date)
    tenders_info = rostender_parse(url_biocide, headers)
    files_writer(tenders_info, 'biocide')

    print('---------------------------------------\nЗанимаюсь ключевым словом оптион')
    url_option = url_constructor(kwd_option, actual_date)
    tenders_info = rostender_parse(url_option, headers)
    files_writer(tenders_info, 'option')

    print('---------------------------------------\nЗанимаюсь ключевым словом эктоскейл')
    url_ektoskail = url_constructor(kwd_ektoskeil, actual_date)
    tenders_info = rostender_parse(url_ektoskail, headers)
    files_writer(tenders_info, 'ektoskeil')

    print('---------------------------------------\nЗанимаюсь ключевым словом аминат')
    url_aminat = url_constructor(kwd_aminat, actual_date)
    tenders_info = rostender_parse(url_aminat, headers)
    files_writer(tenders_info, 'aminat')


date_str = Label(root, text='Введи дату в формате 06.03.2021', bg='#fafafa', font=("Arial", 10)).pack()
actual_date_str = StringVar()
date_field = Entry(root, textvariable=actual_date_str).pack()
date_btn = Button(root, text='Отправить', command=get_date).pack()


if __name__ == '__main__':
    root.mainloop()



