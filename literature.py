class LiteratureFinder():
    def __init__(self):

    def get(self, author, name, year):
        text = 'http://opac.kpi.ua/F/BJDAU5Q1KTKSGNTX8EVDP4TB1UBNNFYAPGUTUG93R5X4EGHCJV-18951'

        data = {
            'func': 'find-b',
            'request': author,
            'find_code':'WRD',
            'x':46,
            'y':4,
            'filter_code_1':'WLN1',
            'filter_request_1': '',
            'filter_code_2':'WYR',
            'filter_request_2': year,
            'filter_code_3': 'WFT',
            'filter_request_3': '',
            'filter_code_4':'WSBL',
            'filter_request_4': '',
        }
        r = requests.get(text, params = data)
        soup = BeautifulSoup(r.text, 'html.parser')
        res = soup.find_all(name='td', attrs={'class':'text3'})
        res2 = soup.find_all(name='td', attrs={'id':'bold'})
        if len(res) >= 4:
            return unicode(res[3].text)
        elif res2:
            return unicode(res2[0].text)
        else:
            return None

    def parse_file(self, file_name):
        f = open(file_name)
        self.names = []
        self.years = []
        self.authors = []
        for row in f:
            split_row = row.split()
            for i, el in enumerate(split_row):
                if i != len(split_row) - 2 and el[-1:] != '.' and self._check_name(split_row[i:i+2]):
                    self.names.append(" ".join(split_row[i:i+2]))
                    break

            for i, el in enumerate(split_row):
                if i == 1:
                    self.authors.append(el)
                    break


            for i, el in enumerate(split_row):
                try:
                    if len(el) == 5 and el[-1:] == '.' and int(el[0:4]) or len(el) == 4 and int(el[:8]):
                        self.years.append(el[:4])
                        break
                except:
                    pass

    def _check_name(self, names=[]):
        for n in names:
            if (n[-1] == '.' or n[-1] == ',') and len(n) <= 7:
                return False
        return True

    def run(self):
        if len(self.authors) == len(self.names) and len(self.names) and len(self.years):
            for i, el in enumerate(self.names):
                res = self.get(l.authors[i], self.names[i], self.years[i])
                if res:
                    print self.names[i], ' - ', res.strip()
                else:
                    print self.names[i], ' - ', "nothing"
        else:
            raise Exception('test')


l = LiteratureFinder()
l.parse_file('liter_dos.txt')
l.run()