import re

import scrapy
import pprint
from hkjc import items
from hkjc.utilities import * 
import operator
# import scipy.spatial as spat
from collections import defaultdict
import itertools
from itertools import izip_longest
import numpy as np
import scipy.stats as ss

'''
Simple HKJC Results Spider
s
'''

class HorseSpider(scrapy.Spider):

    name = 'hkjcsep2'
    

    def __init__(self, date, racecoursecode, **kwargs):
        assert racecoursecode in ['ST', 'HV']
        super(HorseSpider, self).__init__(**kwargs)
        self.domain = 'hkjc.com'
        self.racecoursecode = racecoursecode
        self.racedate = date
        self.racedateobj = datetime.strptime(date, "%Y%m%d")
        self.MeetingDrawPlaceCorr = []
        self.meetingrunners = defaultdict(list)
        self.sectionalbaseurl = 'http://www.hkjc.com/english/racing/display_sectionaltime.asp?'
        self.start_urls = [
            'http://racing.{domain}/racing/Info/Meeting/Results/English/Local/'
            '{date}/{racecoursecode}/1'.format(domain=self.domain, 
                date=date, racecoursecode=racecoursecode),
        ]

    def parse(self, response):
        #the races 
        race_paths = response.xpath('//div[@class="raceNum clearfix"]//'
            'td[position()!=last()]/a/@href').extract()
        ##exclude S1 S1 Simulcast
        ## http://racing.hkjc.com/racing/Info/Meeting/Results/English/Simulcast/20150607/S2/1>
        regex = re.compile('http://racing.hkjc.com/racing/Info/Meeting/Results/English/Simulcast/.*')
        
        race_urls = ['http://racing.{domain}{path}'.format(domain=self.domain, 
            path=path) for path in race_paths] + self.start_urls
        race_urls = [i for i in race_urls if not regex.match(i)]
        # print race_urls
        for url in race_urls:
            yield scrapy.Request(url, callback=self.parse_race)

    def parse_race(self, response):
        '''
        racedate = Column(db.Date, nullable=False)
        racecoursecode = db.Column(db.String(2))
        racenumber = db.Column(db.Integer)
        racegoing = db.Column(db.String(10))
        '''
        _racedate = getdateobject(self.racedate)
        _racecoursecode = self.racecoursecode
        _racenumber = try_int(response.url.split('/')[-1])
        race_text = response.xpath('//div[@class="rowDiv15"]/div[@class="boldFont14 color_white trBgBlue"]/text()').extract()
        _raceindex= None
        if race_text:
            race_regexp = '^RACE (?P<number>\d+) \((?P<index>\d+)\)$'
            race_dict = re.match(race_regexp, race_text[0]).groupdict()
            _raceindex = try_int(race_dict['index'])
        ## [u'Class 4 - ', u'1400M - (60-40)', u'Going :', u'GOOD']
        raceinfo =  response.xpath('//div[@class="rowDiv15"]/div[@class="boldFont14 color_white trBgBlue"]/following-sibling::div/table/tr[1]//td//text()').extract()
        raceclass = racedistance = None
        if raceinfo:
            race_class = unicode.strip(raceinfo[0].replace(u'-', u''))
            race_distance = unicode.strip(raceinfo[0].split(u'-')[0]).replace(u'm', u'')

        #3get distance, class

        #     '"boldFont14 color_white trBgBlue"]/text()').extract()

        _racegoing = response.xpath('//td[text() = "Going :"]/'
            'following-sibling::td/text()').extract()[0]

        _racingincidentreport = response.xpath('//tr[td[contains(text(), '
            '"Racing Incident Report")]]/following-sibling::tr/td/text()'
            ).extract()[0]

        ##dividend always present
        # WIN PLACEDIV, QN, QNP, TIERCE TRIO,


        div_table = response.xpath("//td[@class='trBgBlue1 tdAlignL boldFont14 color_white']")
        isdividend = response.xpath("//td[text() = 'Dividend']/text()").extract()[0]

        if isdividend == u'Dividend':
            div_info = defaultdict(list)
            markets = [ 'WIN', 'PLACE', 'QUINELLA', 'QUINELLA PLACE', 'TIERCE', 'TRIO', 'FIRST 4', 'QUARTET','9TH DOUBLE', 'TREBLE', '3RD DOUBLE TRIO' , 'SIX UP', 'JOCKEY CHALLENGE',
            '8TH DOUBLE', '8TH DOUBLE', '2ND DOUBLE TRIO', '6TH DOUBLE', 'TRIPLE TRIO(Consolation)', 'TRIPLE TRIO', '5TH DOUBLE', '5TH DOUBLE', '1ST DOUBLE TRIO', '3RD DOUBLE' ,
            '2ND DOUBLE', '1ST DOUBLE']
            for m in markets:
                try:
                    xpathstr = str("//tr[td/text() = 'Dividend']/following-sibling::tr[td/text()=")
                    xpathstr2 = str("]/td/text()")
                    win_divs =response.xpath(xpathstr + "'" + str(m) + "'" + xpathstr2).extract()
                    div_info[win_divs[0]] = [ win_divs[1],win_divs[2] ] 
                    print div_info
                except:
                    div_info[m] = None
            # response.xpath("//tr[td/text() = 'Dividend']/following-sibling::tr[2]").extract()[0]

        _sectional_time_url = response.xpath('//div[@class="rowDiv15"]/div['
            '@class="rowDivRight"]/a/@href').extract()[0]
        request = scrapy.Request(_sectional_time_url, callback=
            self.parse_sectional_time)

        meta_dict = {
            'racenumber': _racenumber,
            'racedate': _racedate,
            'racecoursecode': _racecoursecode,
            'raceindex': _raceindex,
            'racegoing': _racegoing,
            'racingincidentreport': cleanstring(_racingincidentreport),
            'results_url': response.url,
            'win_combo_div': div_info['WIN'],
            'place_combo_div': div_info['PLACE'],
            'qn_combo_div' : div_info['QUINELLA'],
            'qnp_combo_div' : div_info['QUINELLA PLACE'],
            'tce_combo_div' : div_info['TIERCE'],
            'trio_combo_div' : div_info['TRIO'],
            'f4_combo_div' : div_info['FIRST 4'],
            'qtt_combo_div' : div_info['QUARTET'],
            'dbl9_combo_div' : div_info['9TH DOUBLE'],
            'dbl8_combo_div' : div_info['8TH DOUBLE'],
            'dbl7_combo_div' : div_info['7TH DOUBLE'],
            'dbl6_combo_div' : div_info['6TH DOUBLE'],
            'dbl5_combo_div' : div_info['5TH DOUBLE'],
            'dbl4_combo_div' : div_info['4TH DOUBLE'],
            'dbl3_combo_div' : div_info['3RD DOUBLE'],
            'dbl2_combo_div' : div_info['2ND DOUBLE'],
            'dbl1_combo_div' : div_info['1ST DOUBLE'],
            'dbl10_combo_div' : div_info['10TH DOUBLE'],
            'dbltrio1_combo_div' : div_info['1ST DOUBLE TRIO'],
            'dbltrio2_combo_div' : div_info['2ND DOUBLE TRIO'],
            'dbltrio3_combo_div' : div_info['3RD DOUBLE TRIO'],
            'raceclass': race_class, 
            'racedistance': race_distance

        }
        
        request.meta.update(meta_dict)

        yield request
        # return meta_dict

    def parse_sectional_time(self, response):
        '''
        horsenumber, horsename, horsecode
        
        marginsbehindleader = db.Column(postgresql.ARRAY(Float)) #floats
        
        sec_timelist= db.Column(postgresql.ARRAY(Float))
        '''

 
        horse_lines_selector = response.xpath('//table[@class="bigborder"]//'
            'table//a/../../..')
        sectional_time_selector = response.xpath('//table[@class='
            '"bigborder"]//table//a/../../../following-sibling::tr[1]')
        for line_selector, time_selector in zip(horse_lines_selector, 
                sectional_time_selector):

            horsenumber = try_int(line_selector.xpath('td[1]/div/text()').extract()[0].strip())

            horse_name_cell = line_selector.xpath('td[3]/div/a/text()').extract()[0]
            horse_name_regexp = '^(?P<name>[^\(]+)\((?P<code>[^\)]+)\)$'
            horse_name_dict = re.match(horse_name_regexp, horse_name_cell).groupdict()
            horsename = horse_name_dict['name']
            horsecode = horse_name_dict['code']
            horsereport = getHorseReport(response.meta['racingincidentreport'], horsename)
            sec_timelist = [time.strip() for time in time_selector.xpath('td/text()').extract()]
            sec_timelist_len = len(sec_timelist)
            sec_timelist.extend([None for i in xrange(6-sec_timelist_len)])
            sec_timelist = map(get_sec_in_secs, sec_timelist)

            horse_path = line_selector.xpath('td[3]/div/a/@href').extract()[0]
            horse_url = 'http://www.{domain}/english/racing/{path}&Option=1#htop'.format(
                domain=self.domain, path=horse_path)

            horse_smartform_url = 'http://racing.hkjc.com/racing/info/horse/smartform/english/{hcode}'.format(
                hcode=horsecode)

            marginsbehindleader = [s.strip('\t\n\r ') for s in line_selector.xpath(
                'td//table//td/text()').extract()]
            marginsbehindleader.extend([None]*(6 - len(marginsbehindleader)))
            marginsbehindleader = map(horselengthprocessor, marginsbehindleader)

            request = scrapy.Request(response.meta['results_url'],
                callback=self.parse_results)
            meta_dict = response.meta
            meta_dict.update({
                'horsenumber': horsenumber,
                'horsename': horsename,
                'horsecode': horsecode,
                'horsereport': horsereport,
                'sec_timelist': sec_timelist,
                'horse_url': horse_url,
                'horse_smartform_url': horse_smartform_url,
                'marginsbehindleader': marginsbehindleader,
            })
            request.meta.update(meta_dict)
 
            # print meta_dict
            yield request



    def parse_results(self, response):

        '''
        parse_results
        parse_horse
        parse_past_race
        finish_time = db.Column(db.Float) #seconds
        positions = db.Column(postgresql.ARRAY(Integer)) #ints
        horsenumber = db.Column(db.Integer)
        horsecode = Column(String(6), nullable=False)
        declarhorsewt= Column(Integer, nullable=True)
        actualwt= Column(Integer, nullable=True)
        placenum = Column(Integer)
        place = Column(String(10)) #includes scratched
        isScratched = db.Column(db.Boolean)
        lbw= Column(Float, nullable=True)
        jockey2horsewt= Column(Float, nullable=True)
        jockeyname = Column(String(255), nullable=False)
        jockeycode = Column(String(6), nullable=False)

        runningposition=db.Column(postgresql.ARRAY(String(100)))
        racingincidentreport = Column(Text, nullable=True)
        horsereport = Column(Text, nullable=True)
        winodds= Column(Float, nullable=True)
        earlypacepoints_this = Column(Integer)
        '''
        ##all horsecodes
        # horsecodes_ = response.xpath('//table[@class="tableBorder trBgBlue tdAlignC number12 draggable"]/tbody/tr/td[3]/a/@href').extract()[0]
        # horsecodes = re.match(r'http://www.hkjc.com/english/racing/'
        #     'horse.asp?.*horseno=(?P<str>[^&]*)(&.*$|$)', horsecodes_
        #     ).groupdict()['str']

        winodds = response.xpath('//table[@class="tableBorder trBgBlue '
                'tdAlignC number12 draggable"]//tr[@class="trBgGrey" or @class='
                '"trBgWhite"]/td[12]/text()').extract()
        horsecodes = response.xpath('//table[@class="tableBorder trBgBlue '
                'tdAlignC number12 draggable"]//tr[@class="trBgGrey" or @class='
                '"trBgWhite"]/td[3]/a/@href').extract()

        def filterPick(list,filter):
            return [ ( l, m.group(1) ) for l in list for m in (filter(l),) if m]

        searchRegex = re.compile(r'http://www.hkjc.com/english/racing/'
            'horse.asp?.*horseno=(?P<str>[^&]*)(&.*$|$)').search
        horsecodes = filterPick(horsecodes,searchRegex)
        horsecodes = [i[1] for i in horsecodes]
        # [m.group(1) for l in lines for m in [regex.search(l)] if m]
        # horsecodes = map(re.match(, horsecodes))
        # # print horsecodes, winodds

        # sorted([map(getodds, winodds)])
        #remove bad winodds
        def try_winodds(winodds):
            if winodds == u'---':
                return None
            else:
                return try_float(winodds)

        winodds = [ try_winodds(i) for i in winodds]
        winoddsranks = ss.rankdata(winodds)

        tr = response.xpath('//tr[td[3]/a[text() = "{}"]]'.format(
            response.meta['horsename']))


        horse_url_from_result = tr.xpath('td[3]/a/@href').extract()[0]
        
        jockeyname = tr.xpath('td[4]/a/text()').extract()[0]

        jockeycode_ = tr.xpath('td[4]/a/@href').extract()[0]
        jockeycode = re.match(r'^http://www.hkjc.com/english/racing/'
            'jockeyprofile.asp?.*jockeycode=(?P<str>[^&]*)(&.*$|$)', jockeycode_
            ).groupdict()['str']

        trainername = tr.xpath('td[5]/a/text()').extract()[0]

        trainercode_ = tr.xpath('td[5]/a/@href').extract()[0]
        trainercode = re.match(r'http://www.hkjc.com/english/racing/'
            'trainerprofile.asp?.*trainercode=(?P<str>[^&]*)(&.*$|$)', trainercode_
            ).groupdict()['str']

        winoddsrank = winoddsranks[response.meta['horsenumber']-1]

        actualwt = try_int(tr.xpath('td[6]/text()').extract()[0])

        declarhorsewt = try_int(tr.xpath('td[7]/text()').extract()[0])

        jockey2horsewt = round(float(actualwt)/float(declarhorsewt),2)

        draw = getdraw(tr.xpath('td[8]/text()').extract()[0])
        lbw = getlbw(tr.xpath('td[9]/text()').extract()[0])

        #this is wrong
        runningposition = tr.xpath('td[10]//td/text()').extract() #needs to be an array of strings all tds

        finishtime = get_hkjc_ftime(tr.xpath('td[11]/text()').extract()[0]) #float seconds

        winodds = getodds(tr.xpath('td[12]/text()').extract()[0])

        #place, placenum, isScratched
        isScratched = False
        _placeraw = tr.xpath('td[1]/text()').extract()[0]
        if _placeraw == u'':
            isScratched = True
            placenum = 99
        else:
            placenum = try_int(_placeraw)


        meta_dict = response.meta
        meta_dict.update(
            jockeyname=jockeyname,
            jockeycode=jockeycode,
            trainername=trainername,
            trainercode=trainercode,
            actualwt=actualwt,
            declarhorsewt=declarhorsewt,
            jockey2horsewt=jockey2horsewt,
            draw=draw,
            lbw=lbw,
            runningposition=runningposition,
            finishtime=finishtime,
            winodds = winodds,
            isScratched= isScratched,
            placenum = placenum,
            place = _placeraw,
            winoddsrank=winoddsrank,
            runners_list= horsecodes

            # winoddsrank=winoddsrank,
        )
        # print horse_url_from_result
        # request = scrapy.Request(response.meta['horse_url'],callback=self.parse_horse)
        # request.meta.update(meta_dict)

        # return request

        yield items.RaceItem(
            racenumber = response.meta['racenumber'],
            racedate = response.meta['racedate'],
            racegoing = response.meta['racegoing'],
            racecoursecode = response.meta['racecoursecode'],
            raceindex = response.meta['raceindex'],
            racingincidentreport = response.meta['racingincidentreport'],
            horsereport=response.meta['horsereport'],
            results_url = response.meta['results_url'],
            horsenumber = response.meta['horsenumber'],
            horsename = response.meta['horsename'],
            horsecode = response.meta['horsecode'],
            sec_timelist = response.meta['sec_timelist'],
            horse_url =  response.meta['horse_url'],
            horse_smartform_url=  response.meta['horse_smartform_url'],
            marginsbehindleader=response.meta['marginsbehindleader'],
            jockeyname=response.meta['jockeyname'],
            jockeycode=response.meta['jockeycode'],
            trainername=response.meta['trainername'],
            trainercode=response.meta['trainercode'],
            actualwt=response.meta['actualwt'],
            declarhorsewt=response.meta['declarhorsewt'],
            jockey2horsewt=response.meta['jockey2horsewt'],
            draw=response.meta['draw'],
            lbw=response.meta['lbw'],
            runningposition=response.meta['runningposition'],
            finishtime=response.meta['finishtime'],
            winodds = response.meta['winodds'],
            isScratched = response.meta['isScratched'],
            placenum = response.meta['placenum'],
            place = response.meta['place'],
            winoddsrank= response.meta['winoddsrank'],
            runners_list=response.meta['runners_list'],
            win_combo_div=response.meta['win_combo_div'],
            place_combo_div = response.meta['win_combo_div'],
            qn_combo_div = response.meta['win_combo_div'],
            qnp_combo_div = response.meta['qnp_combo_div'],
            tce_combo_div = response.meta['tce_combo_div'],
            trio_combo_div = response.meta['trio_combo_div'],
            f4_combo_div = response.meta['f4_combo_div'],
            qtt_combo_div = response.meta['qtt_combo_div'],
            dbl9_combo_div = response.meta['dbl9_combo_div'],
            dbl8_combo_div = response.meta['dbl8_combo_div'],
            dbl7_combo_div = response.meta['dbl7_combo_div'],
            dbl6_combo_div = response.meta['dbl6_combo_div'],
            dbl5_combo_div = response.meta['dbl5_combo_div'],
            dbl4_combo_div = response.meta['dbl4_combo_div'],
            dbl3_combo_div = response.meta['dbl3_combo_div'],
            dbl2_combo_div = response.meta['dbl2_combo_div'],
            dbl1_combo_div = response.meta['dbl1_combo_div'],
            dbl10_combo_div = response.meta['dbl10_combo_div'],
            dbltrio1_combo_div = response.meta['dbltrio1_combo_div'],
            dbltrio2_combo_div = response.meta['dbltrio2_combo_div'],
            dbltrio3_combo_div = response.meta['dbltrio3_combo_div']
                    )   