import scrapy
from urllib.parse import urlsplit

class WikiAwardSpider(scrapy.Spider):
# Создаем таблицу со следующими данными для каждого фильма - победителя Оскара: 
# Название, Режиссёр, Исполнители главных ролей, Дата выхода фильма, Продолжительность
# title, director, starring, release_date, running_time
  name = "wiki-award" # имя spider'а
  start_urls = ['https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture']

  def base_url(self, url, with_path=False):
  # Получаем основную часть (протокол и имя сайта из URL)
    parsed = urlsplit(url)
    path   = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
    parsed = parsed._replace(path=path)
    parsed = parsed._replace(query='')
    parsed = parsed._replace(fragment='')
    return parsed.geturl()

  def parse(self, response):
  # Основная функция crawling'а
    self.logger.info('Hello ! This is my first spider.') 
    
    rows   =  response.css('table[class="wikitable"] tr') # строки таблиц класса 'wikitable', содержащие оскароносные фильмы 
    # если указать "table.wikitable" , то еще добавиться лишня таблица (с классами "wikitable sortable plainrowheaders jquery-tablesorter"")
    site = self.base_url (self.start_urls[0]) # адрес сайта с протоколом без пути
    oskar_no  = ''
    for row in rows:
        if row.css('td').get() == None: # пропускаем заголовки таблиц ( т.к. в scrapy не реализована поддержка ':has(> td)' )
          continue

        cell_award = "".join(row.css("td[rowspan] ::text").getall()).strip()
        oskar_no   = cell_award if cell_award != '' else oskar_no # ячейки с номерами конкурсов
        movie_url = row.css('td:not([rowspan]):nth-child(1) * ::attr("href")').get()  # берем первую ссылку в ячейке с фильмом
        if cell_award == '': # если это строка без ячейки с названием конкурса
          main_dict = { 
            'award':  oskar_no, 
            'title':  "".join(row.css('td:not([rowspan]):nth-child(1) ::text').getall()).strip(), # ячейки с названиями фильмов
            'producer/studio': "".join(row.css('td:not([rowspan]):nth-child(2) ::text').getall()).strip(), # ячейки с названиями студии / продюсеров
            'winner': True if row.css('[style="background:#FAEB86"]').get() != None else False, # строки выделенные как победители в номинации
            'url_page': site + movie_url if movie_url != None else '' 
          } 

          if movie_url != None:
            # в url ! можно передавать относительный URL  
            # в параметре meta можно передавать произвольные данные
            yield response.follow(movie_url, callback=self.parse_film_page, meta={'main_dict': main_dict})  
          else:
            yield self.main_dict

# метод парсинга страницы с фильмом
  def parse_film_page(self, response):
    # обработка страницы, содержащей информацию о фильме
    table = response.css('table[class="infobox vevent"]')
    film_title = table.css('th[class="infobox-above summary"] ::text').get() # название фильма (в фильм Judas and the Black Messiah - он выделен курсивом <i></i>, в Отце невесты - <tr>)

    main_dict = response.meta.get('main_dict') # можно также обратиться к элементам словаря 

    film_director = "\n".join(table.css('th:contains("Directed by") + td[class="infobox-data"] ::text').getall()).strip() # режиссёр (может быть несколько)
    film_country =  "\n".join(table.css('th:contains("Country") + td[class="infobox-data"] ::text').getall()).strip() # страна
    film_countries =  "\n".join(table.css('th:contains("Countries") + td[class="infobox-data"] ::text').getall()).strip() # страна
    
    film_starring = "\n".join(table.css('th:contains("Starring") + td[class="infobox-data"] ::text').getall()).strip() # исполнители главных ролей
    film_year = "\n".join(table.css('th:contains("Release date") + td[class="infobox-data"] ::text').getall()).strip() # год выхода
    film_time = "\n".join(table.css('th:contains("Running time") + td[class="infobox-data"] ::text').getall()).strip() # продолжительность фильма (м.б. киноверсии и ТВ-версии)
    detailed_dict = dict(main_dict,  \
      ** { 
          'film':      film_title, 
          'director':  film_director,
          'film_starring': film_starring,
          'country':   film_country if film_country != '' else film_countries,
          'film_year': film_year, 
          'film_time': film_time
        }
    )
    yield detailed_dict

