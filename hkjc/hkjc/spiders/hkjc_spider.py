# import re

# import scrapy
# import pprint
# from hkjc import items
# from hkjc.utilities import * 
# import operator
# import scipy.spatial as spat
# from collections import defaultdict
# import itertools
# from itertools import izip_longest
# import numpy as np
# import scipy.stats as ss

# #Example - http://www.hkjc.com/english/racing/horse.asp?horseno=S379&Option=1%0A
# # http://www.hkjc.com/english/racing/horse.asp?horseno=N208
# def extract_data_from_row_v1(response, season, row):
#     url_path = os.path.dirname(response.url)
#     item = {}
#     print "Extracting v1"
#     try:
#         item["h_raceindexes"] = row.xpath("td")[0].xpath("a/text()").extract()[0]
#         race_link = url_path + "/" + row.xpath("td")[0].xpath("a/@href").extract()[0]
#     except:
#         pass
#     item["h_raceurls"] = row.xpath("td")[0].xpath("a/@href").extract()[0]
#     item["h_places"] = row.xpath("td")[1].xpath("*//text()").extract()[0].strip()
#     item["h_racedates"] = datetime.datetime.strptime(
#                     row.xpath("td")[2].xpath("text()").extract()[0].strip(),
#                     "%d/%m/%y")        
#     item["h_distances"] = row.xpath("td")[4].xpath("text()").extract()[0].strip()
#     item["h_goings"] = row.xpath("td")[5].xpath("text()").extract()[0].strip()
#     item["h_raceclasses"] =  row.xpath("td")[6].xpath("text()").extract()[0].strip()
#     item["h_draws"] = row.xpath("td")[7].xpath("font").xpath("text()").extract()[0].strip()
#     item["h_ratings"] =  row.xpath("td")[8].xpath("text()").extract()[0].strip()
#     item["h_trainers"] = " ".join(row.xpath("td")[9].xpath("*//text()").extract()).strip()
#     item["h_jockeys"] = " ".join(row.xpath("td")[10].xpath("*//text()").extract()).strip()
    
#     item["h_lbws"] =  row.xpath("td")[11].xpath("*/text()| text()").extract()[0].strip()
    
#     item["h_winoddss"] =  row.xpath("td")[12].xpath("text()").extract()[0].strip()
#     item["h_actwts"] =  row.xpath("td")[13].xpath("text()").extract()[0].strip()
#     item["h_rps"] = " ".join(row.xpath("td")[14].xpath("*//text()").extract()).strip().replace(unichr(160), "")
#     item["h_finishtimes"] = row.xpath("td")[15].xpath("text()").extract()[0].strip()
#     item["h_horseweights"] = row.xpath("td")[16].xpath("text()").extract()[0].strip()
#     item["h_gears"] = row.xpath("td")[17].xpath("text()").extract()[0].strip()
#     meta_dict = response.meta
#     meta_dict.update(
#             h_raceindexes = h_raceindexes,
#             h_places=h_places,
#             h_racedates=h_racedates,
#             h_goings=h_goings,
#             h_distances=h_distances,
#             h_raceclasses=h_raceclasses,
#             h_draws=h_draws,
#             h_ratings= h_ratings,
#             h_trainers=h_trainers,
#             h_jockeys=h_jockeys,
#             h_lbws = h_lbws,
#             h_winodds=h_winodds,
#             h_rps=h_rps,
#             h_finishtimes=h_finishtimes,
#             h_horseweights=h_horseweights,
#             h_gears=h_gears
#     )
#     return item

# #Example - http://www.hkjc.com/english/racing/OtherHorse.asp?HorseNo=N159

# def extract_data_from_row_v2(response, season, row):
#     url_path = os.path.dirname(response.url)

#     item = {}
#     try:
#         item["h_raceindex"] = row.xpath("td")[0].xpath("*/font/a/text()").extract()[0]
#         race_link = url_path + "/" + row.xpath("td")[0].xpath("*/font/a/@href").extract()[0]
#     except:
#         pass
    
#     item["h_place"] = row.xpath("td")[1].xpath("*//text()").extract()[0].strip()
#     item["h_racedate"] = datetime.datetime.strptime(
#             row.xpath("td")[2].xpath("*/font").xpath("text()").extract()[0].strip(),
#             "%d/%m/%Y")
#     item["h_distance"] = row.xpath("td")[4].xpath("*/font").xpath("text()").extract()[0].strip()
#     item["h_going"] = row.xpath("td")[5].xpath("*/font").xpath("text()").extract()[0].strip()
#     item["h_raceclass"] =  row.xpath("td")[6].xpath("*/font").xpath("text()").extract()[0].strip()
#     #item["h_draw"] = row.xpath("td")[7].xpath("*/font").xpath("text()").extract()[0].strip()
#     item["h_draw"] = row.xpath("td")[7].xpath("*//text()").extract()[0]
    
#     item["h_rating"] =  row.xpath("td")[8].xpath("*/font").xpath("text()").extract()[0].strip()
#     item["h_trainer"] = " ".join(row.xpath("td")[9].xpath("*//text()").extract()).strip()
#     item["h_jockey"] = " ".join(row.xpath("td")[10].xpath("*//text()").extract()).strip()
#     item["h_lbw"] =  row.xpath("td")[11].xpath("*/font").xpath("text()").extract()[0].strip()

#     item["h_winodds"] =  row.xpath("td")[12].xpath("*/font").xpath("text()").extract()[0].strip()
#     item["h_actwt"] =  row.xpath("td")[13].xpath("*/font").xpath("text()").extract()[0].strip()
#     item["h_rp"] = " ".join(row.xpath("td")[14].xpath("*//text()").extract()).strip().replace(unichr(160), "")
#     item["h_finishtime"] = row.xpath("td")[15].xpath("*/font").xpath("text()").extract()[0].strip()
#     item["h_horseweight"] = row.xpath("td")[16].xpath("*/font").xpath("text()").extract()[0].strip()
#     item["h_gear"] = row.xpath("td")[17].xpath("*/font").xpath("text()").extract()[0].strip()

#     yield item



# class HorseSpider(scrapy.Spider):

#     name = 'hkjcsep'

#     '''
#     localresultspage
#     result page
#     sectionals
#     <--result page 
#     ---> horse
#     oldrace 

#     '''

#     def __init__(self, date, racecoursecode, **kwargs):
#         assert racecoursecode in ['ST', 'HV']
#         super(HorseSpider, self).__init__(**kwargs)
#         self.domain = 'hkjc.com'
#         self.racecoursecode = racecoursecode
#         self.racedate = date
#         self.racedateobj = datetime.strptime(date, "%Y%m%d")
#         self.MeetingDrawPlaceCorr = []
#         self.meetingrunners = defaultdict(list)
#         self.sectionalbaseurl = 'http://www.hkjc.com/english/racing/display_sectionaltime.asp?'
#         self.start_urls = [
#             'http://racing.{domain}/racing/Info/Meeting/Results/English/Local/'
#             '{date}/{racecoursecode}/1'.format(domain=self.domain, 
#                 date=date, racecoursecode=racecoursecode),
#         ]

#     def parse(self, response):
#         #the races 
#         race_paths = response.xpath('//div[@class="raceNum clearfix"]//'
#             'td[position()!=last()]/a/@href').extract()
#         ##exclude S1 S1 Simulcast
#         ## http://racing.hkjc.com/racing/Info/Meeting/Results/English/Simulcast/20150607/S2/1>
#         regex = re.compile('http://racing.hkjc.com/racing/Info/Meeting/Results/English/Simulcast/.*')
        
#         race_urls = ['http://racing.{domain}{path}'.format(domain=self.domain, 
#             path=path) for path in race_paths] + self.start_urls
#         race_urls = [i for i in race_urls if not regex.match(i)]
#         # print race_urls
#         for url in race_urls:
#             yield scrapy.Request(url, callback=self.parse_race)

#     def parse_race(self, response):
#         '''
#         racedate = Column(db.Date, nullable=False)
#         racecoursecode = db.Column(db.String(2))
#         racenumber = db.Column(db.Integer)
#         racegoing = db.Column(db.String(10))
#         '''
#         _racedate = getdateobject(self.racedate)
#         _racecoursecode = self.racecoursecode
#         _racenumber = try_int(response.url.split('/')[-1])
#         race_text = response.xpath('//div[@class="rowDiv15"]/div[@class="boldFont14 color_white trBgBlue"]/text()').extract()
#         _raceindex= None
#         if race_text:
#             race_regexp = '^RACE (?P<number>\d+) \((?P<index>\d+)\)$'
#             race_dict = re.match(race_regexp, race_text[0]).groupdict()
#             _raceindex = try_int(race_dict['index'])
#         ## [u'Class 4 - ', u'1400M - (60-40)', u'Going :', u'GOOD']
#         raceinfo =  response.xpath('//div[@class="rowDiv15"]/div[@class="boldFont14 color_white trBgBlue"]/following-sibling::div/table/tr[1]//td//text()').extract()
#         raceclass = racedistance = None
#         if raceinfo:
#             race_class = unicode.strip(raceinfo[0].replace(u'-', u''))
#             race_distance = unicode.strip(raceinfo[0].split(u'-')[0]).replace(u'm', u'')

#         #3get distance, class

#         #     '"boldFont14 color_white trBgBlue"]/text()').extract()

#         _racegoing = response.xpath('//td[text() = "Going :"]/'
#             'following-sibling::td/text()').extract()[0]

#         _racingincidentreport = response.xpath('//tr[td[contains(text(), '
#             '"Racing Incident Report")]]/following-sibling::tr/td/text()'
#             ).extract()[0]

#         ##dividend always present
#         # WIN PLACEDIV, QN, QNP, TIERCE TRIO,


#         div_table = response.xpath("//td[@class='trBgBlue1 tdAlignL boldFont14 color_white']")
#         isdividend = response.xpath("//td[text() = 'Dividend']/text()").extract()[0]

#         if isdividend == u'Dividend':
#             div_info = defaultdict(list)
#             markets = [ 'WIN', 'PLACE', 'QUINELLA', 'QUINELLA PLACE', 'TIERCE', 'TRIO', 'FIRST 4', 'QUARTET','9TH DOUBLE', 'TREBLE', '3RD DOUBLE TRIO' , 'SIX UP', 'JOCKEY CHALLENGE',
#             '8TH DOUBLE', '8TH DOUBLE', '2ND DOUBLE TRIO', '6TH DOUBLE', 'TRIPLE TRIO(Consolation)', 'TRIPLE TRIO', '5TH DOUBLE', '5TH DOUBLE', '1ST DOUBLE TRIO', '3RD DOUBLE' ,
#             '2ND DOUBLE', '1ST DOUBLE']
#             for m in markets:
#                 try:
#                     xpathstr = str("//tr[td/text() = 'Dividend']/following-sibling::tr[td/text()=")
#                     xpathstr2 = str("]/td/text()")
#                     win_divs =response.xpath(xpathstr + "'" + str(m) + "'" + xpathstr2).extract()
#                     div_info[win_divs[0]] = [ win_divs[1],win_divs[2] ] 
#                     print div_info
#                 except:
#                     div_info[m] = None
#             # response.xpath("//tr[td/text() = 'Dividend']/following-sibling::tr[2]").extract()[0]

#         _sectional_time_url = response.xpath('//div[@class="rowDiv15"]/div['
#             '@class="rowDivRight"]/a/@href').extract()[0]
#         request = scrapy.Request(_sectional_time_url, callback=
#             self.parse_sectional_time)

#         meta_dict = {
#             'racenumber': _racenumber,
#             'racedate': _racedate,
#             'racecoursecode': _racecoursecode,
#             'raceindex': _raceindex,
#             'racegoing': _racegoing,
#             'racingincidentreport': cleanstring(_racingincidentreport),
#             'results_url': response.url,
#             'win_combo_div': div_info['WIN'],
#             'place_combo_div': div_info['PLACE'],
#             'qn_combo_div' : div_info['QUINELLA'],
#             'qnp_combo_div' : div_info['QUINELLA PLACE'],
#             'tce_combo_div' : div_info['TIERCE'],
#             'trio_combo_div' : div_info['TRIO'],
#             'f4_combo_div' : div_info['FIRST 4'],
#             'qtt_combo_div' : div_info['QUARTET'],
#             'dbl9_combo_div' : div_info['9TH DOUBLE'],
#             'dbl8_combo_div' : div_info['8TH DOUBLE'],
#             'dbl7_combo_div' : div_info['7TH DOUBLE'],
#             'dbl6_combo_div' : div_info['6TH DOUBLE'],
#             'dbl5_combo_div' : div_info['5TH DOUBLE'],
#             'dbl4_combo_div' : div_info['4TH DOUBLE'],
#             'dbl3_combo_div' : div_info['3RD DOUBLE'],
#             'dbl2_combo_div' : div_info['2ND DOUBLE'],
#             'dbl1_combo_div' : div_info['1ST DOUBLE'],
#             'dbl10_combo_div' : div_info['10TH DOUBLE'],
#             'dbltrio1_combo_div' : div_info['1ST DOUBLE TRIO'],
#             'dbltrio2_combo_div' : div_info['2ND DOUBLE TRIO'],
#             'dbltrio3_combo_div' : div_info['3RD DOUBLE TRIO'],
#             'raceclass': race_class, 
#             'racedistance': race_distance

#         }
        
#         request.meta.update(meta_dict)

#         yield request
#         # return meta_dict

#     def parse_sectional_time(self, response):
#         '''
#         horsenumber, horsename, horsecode
        
#         marginsbehindleader = db.Column(postgresql.ARRAY(Float)) #floats
        
#         sec_timelist= db.Column(postgresql.ARRAY(Float))
#         '''

 
#         horse_lines_selector = response.xpath('//table[@class="bigborder"]//'
#             'table//a/../../..')
#         sectional_time_selector = response.xpath('//table[@class='
#             '"bigborder"]//table//a/../../../following-sibling::tr[1]')
#         for line_selector, time_selector in zip(horse_lines_selector, 
#                 sectional_time_selector):

#             horsenumber = try_int(line_selector.xpath('td[1]/div/text()').extract()[0].strip())

#             horse_name_cell = line_selector.xpath('td[3]/div/a/text()').extract()[0]
#             horse_name_regexp = '^(?P<name>[^\(]+)\((?P<code>[^\)]+)\)$'
#             horse_name_dict = re.match(horse_name_regexp, horse_name_cell).groupdict()
#             horsename = horse_name_dict['name']
#             horsecode = horse_name_dict['code']
#             horsereport = getHorseReport(response.meta['racingincidentreport'], horsename)
#             sec_timelist = [time.strip() for time in time_selector.xpath('td/text()').extract()]
#             sec_timelist_len = len(sec_timelist)
#             sec_timelist.extend([None for i in xrange(6-sec_timelist_len)])
#             sec_timelist = map(get_sec_in_secs, sec_timelist)

#             horse_path = line_selector.xpath('td[3]/div/a/@href').extract()[0]
#             horse_url = 'http://www.{domain}/english/racing/{path}&Option=1#htop'.format(
#                 domain=self.domain, path=horse_path)

#             horse_smartform_url = 'http://racing.hkjc.com/racing/info/horse/smartform/english/{hcode}'.format(
#                 hcode=horsecode)

#             marginsbehindleader = [s.strip('\t\n\r ') for s in line_selector.xpath(
#                 'td//table//td/text()').extract()]
#             marginsbehindleader.extend([None]*(6 - len(marginsbehindleader)))
#             marginsbehindleader = map(horselengthprocessor, marginsbehindleader)

#             request = scrapy.Request(response.meta['results_url'],
#                 callback=self.parse_results)
#             meta_dict = response.meta
#             meta_dict.update({
#                 'horsenumber': horsenumber,
#                 'horsename': horsename,
#                 'horsecode': horsecode,
#                 'horsereport': horsereport,
#                 'sec_timelist': sec_timelist,
#                 'horse_url': horse_url,
#                 'horse_smartform_url': horse_smartform_url,
#                 'marginsbehindleader': marginsbehindleader,
#             })
#             request.meta.update(meta_dict)
 
#             # print meta_dict
#             yield request



#     def parse_results(self, response):

#         '''
#         parse_results
#         parse_horse
#         parse_past_race
#         finish_time = db.Column(db.Float) #seconds
#         positions = db.Column(postgresql.ARRAY(Integer)) #ints
#         horsenumber = db.Column(db.Integer)
#         horsecode = Column(String(6), nullable=False)
#         declarhorsewt= Column(Integer, nullable=True)
#         actualwt= Column(Integer, nullable=True)
#         placenum = Column(Integer)
#         place = Column(String(10)) #includes scratched
#         isScratched = db.Column(db.Boolean)
#         lbw= Column(Float, nullable=True)
#         jockey2horsewt= Column(Float, nullable=True)
#         jockeyname = Column(String(255), nullable=False)
#         jockeycode = Column(String(6), nullable=False)

#         runningposition=db.Column(postgresql.ARRAY(String(100)))
#         racingincidentreport = Column(Text, nullable=True)
#         horsereport = Column(Text, nullable=True)
#         winodds= Column(Float, nullable=True)
#         earlypacepoints_this = Column(Integer)
#         '''
#         ##all horsecodes
#         # horsecodes_ = response.xpath('//table[@class="tableBorder trBgBlue tdAlignC number12 draggable"]/tbody/tr/td[3]/a/@href').extract()[0]
#         # horsecodes = re.match(r'http://www.hkjc.com/english/racing/'
#         #     'horse.asp?.*horseno=(?P<str>[^&]*)(&.*$|$)', horsecodes_
#         #     ).groupdict()['str']

#         winodds = response.xpath('//table[@class="tableBorder trBgBlue '
#                 'tdAlignC number12 draggable"]//tr[@class="trBgGrey" or @class='
#                 '"trBgWhite"]/td[12]/text()').extract()
#         horsecodes = response.xpath('//table[@class="tableBorder trBgBlue '
#                 'tdAlignC number12 draggable"]//tr[@class="trBgGrey" or @class='
#                 '"trBgWhite"]/td[3]/a/@href').extract()

#         def filterPick(list,filter):
#             return [ ( l, m.group(1) ) for l in list for m in (filter(l),) if m]

#         searchRegex = re.compile(r'http://www.hkjc.com/english/racing/'
#             'horse.asp?.*horseno=(?P<str>[^&]*)(&.*$|$)').search
#         horsecodes = filterPick(horsecodes,searchRegex)
#         horsecodes = [i[1] for i in horsecodes]
#         # [m.group(1) for l in lines for m in [regex.search(l)] if m]
#         # horsecodes = map(re.match(, horsecodes))
#         # # print horsecodes, winodds

#         # sorted([map(getodds, winodds)])
#         #remove bad winodds
#         def try_winodds(winodds):
#             if winodds == u'---':
#                 return None
#             else:
#                 return try_float(winodds)

#         winodds = [ try_winodds(i) for i in winodds]
#         winoddsranks = ss.rankdata(winodds)

#         tr = response.xpath('//tr[td[3]/a[text() = "{}"]]'.format(
#             response.meta['horsename']))


#         horse_url_from_result = tr.xpath('td[3]/a/@href').extract()[0]
        
#         jockeyname = tr.xpath('td[4]/a/text()').extract()[0]

#         jockeycode_ = tr.xpath('td[4]/a/@href').extract()[0]
#         jockeycode = re.match(r'^http://www.hkjc.com/english/racing/'
#             'jockeyprofile.asp?.*jockeycode=(?P<str>[^&]*)(&.*$|$)', jockeycode_
#             ).groupdict()['str']

#         trainername = tr.xpath('td[5]/a/text()').extract()[0]

#         trainercode_ = tr.xpath('td[5]/a/@href').extract()[0]
#         trainercode = re.match(r'http://www.hkjc.com/english/racing/'
#             'trainerprofile.asp?.*trainercode=(?P<str>[^&]*)(&.*$|$)', trainercode_
#             ).groupdict()['str']

#         winoddsrank = winoddsranks[response.meta['horsenumber']-1]

#         actualwt = try_int(tr.xpath('td[6]/text()').extract()[0])

#         declarhorsewt = try_int(tr.xpath('td[7]/text()').extract()[0])

#         jockey2horsewt = round(float(actualwt)/float(declarhorsewt),2)

#         draw = getdraw(tr.xpath('td[8]/text()').extract()[0])
#         lbw = getlbw(tr.xpath('td[9]/text()').extract()[0])

#         #this is wrong
#         runningposition = tr.xpath('td[10]//td/text()').extract() #needs to be an array of strings all tds

#         finishtime = get_hkjc_ftime(tr.xpath('td[11]/text()').extract()[0]) #float seconds

#         winodds = getodds(tr.xpath('td[12]/text()').extract()[0])

#         #place, placenum, isScratched
#         isScratched = False
#         _placeraw = tr.xpath('td[1]/text()').extract()[0]
#         if _placeraw == u'':
#             isScratched = True
#             placenum = 99
#         else:
#             placenum = try_int(_placeraw)


#         meta_dict = response.meta
#         meta_dict.update(
#             jockeyname=jockeyname,
#             jockeycode=jockeycode,
#             trainername=trainername,
#             trainercode=trainercode,
#             actualwt=actualwt,
#             declarhorsewt=declarhorsewt,
#             jockey2horsewt=jockey2horsewt,
#             draw=draw,
#             lbw=lbw,
#             runningposition=runningposition,
#             finishtime=finishtime,
#             winodds = winodds,
#             isScratched= isScratched,
#             placenum = placenum,
#             place = _placeraw,
#             winoddsrank=winoddsrank,
#             runners_list= horsecodes

#             # winoddsrank=winoddsrank,
#         )
#         # print horse_url_from_result
#         # request = scrapy.Request(response.meta['horse_url'],callback=self.parse_horse)
#         # request.meta.update(meta_dict)

#         # return request

#         yield items.RaceItem(
#             racenumber = response.meta['racenumber'],
#             racedate = response.meta['racedate'],
#             racegoing = response.meta['racegoing'],
#             racecoursecode = response.meta['racecoursecode'],
#             raceindex = response.meta['raceindex'],
#             racingincidentreport = response.meta['racingincidentreport'],
#             horsereport=response.meta['horsereport'],
#             results_url = response.meta['results_url'],
#             horsenumber = response.meta['horsenumber'],
#             horsename = response.meta['horsename'],
#             horsecode = response.meta['horsecode'],
#             sec_timelist = response.meta['sec_timelist'],
#             horse_url =  response.meta['horse_url'],
#             horse_smartform_url=  response.meta['horse_smartform_url'],
#             marginsbehindleader=response.meta['marginsbehindleader'],
#             jockeyname=response.meta['jockeyname'],
#             jockeycode=response.meta['jockeycode'],
#             trainername=response.meta['trainername'],
#             trainercode=response.meta['trainercode'],
#             actualwt=response.meta['actualwt'],
#             declarhorsewt=response.meta['declarhorsewt'],
#             jockey2horsewt=response.meta['jockey2horsewt'],
#             draw=response.meta['draw'],
#             lbw=response.meta['lbw'],
#             runningposition=response.meta['runningposition'],
#             finishtime=response.meta['finishtime'],
#             winodds = response.meta['winodds'],
#             isScratched = response.meta['isScratched'],
#             placenum = response.meta['placenum'],
#             place = response.meta['place'],
#             winoddsrank= response.meta['winoddsrank'],
#             runners_list=response.meta['runners_list'],
#             win_combo_div=response.meta['win_combo_div'],
#             place_combo_div = response.meta['win_combo_div'],
#             qn_combo_div = response.meta['win_combo_div'],
#             qnp_combo_div = response.meta['qnp_combo_div'],
#             tce_combo_div = response.meta['tce_combo_div'],
#             trio_combo_div = response.meta['trio_combo_div'],
#             f4_combo_div = response.meta['f4_combo_div'],
#             qtt_combo_div = response.meta['qtt_combo_div'],
#             dbl9_combo_div = response.meta['dbl9_combo_div'],
#             dbl8_combo_div = response.meta['dbl8_combo_div'],
#             dbl7_combo_div = response.meta['dbl7_combo_div'],
#             dbl6_combo_div = response.meta['dbl6_combo_div'],
#             dbl5_combo_div = response.meta['dbl5_combo_div'],
#             dbl4_combo_div = response.meta['dbl4_combo_div'],
#             dbl3_combo_div = response.meta['dbl3_combo_div'],
#             dbl2_combo_div = response.meta['dbl2_combo_div'],
#             dbl1_combo_div = response.meta['dbl1_combo_div'],
#             dbl10_combo_div = response.meta['dbl10_combo_div'],
#             dbltrio1_combo_div = response.meta['dbltrio1_combo_div'],
#             dbltrio2_combo_div = response.meta['dbltrio2_combo_div'],
#             dbltrio3_combo_div = response.meta['dbltrio3_combo_div']
#                     )    

#     ##each parse horse , parse race

#     def parse_horse(self, response):
#         '''
#             careerwinpc = db.Column(db.Float) 
#             h_avgspd = db.Column(Float)
#             h_avgspd_n= db.Column(Integer)
#             h_passedlsec_L123= db.Column(Integer)
#             h_avgspeeds =db.Column(postgresql.ARRAY(Float))
#             h_winodds = db.Column(postgresql.ARRAY(Float))
#             h_places = db.Column(postgresql.ARRAY(String(10)))
#             ranks_avgspeeds=db.Column(postgresql.ARRAY(Integer))
#             h_winning_lbw =db.Column(postgresql.ARRAY(Float))
#             h_winning_ftimes=db.Column(postgresql.ARRAY(Float))
#             h_winning_raceclasses=db.Column(postgresql.ARRAY(String(10)))
#             h_winning_oddsranks =db.Column(postgresql.ARRAY(Integer))
#             h_season_racenumbers =db.Column(postgresql.ARRAY(String(50)))
#             h_competition=db.Column(postgresql.ARRAY(String(100))) #all horses, selfweight, position, code, other jockeywhorseweight, position, rating
#             h_subsequentwinnersl1 = Column(Integer)
#             h_subsequentwinnersl2 = Column(Integer)
#             h_subsequentwinnersl3 = Column(Integer)
#             corr_ftime_place= db.Column(Float)
#             corr_winodds_place = db.Column(Float)
#             dayssincelastrun= db.Column(Integer)

                
#             VARIANTS: 
#             http://www.hkjc.com/english/racing/horse.asp?horseno=S379&Option=1%0A 
#             has 4 tables
#         '''
#             # hxs = Selector(response)
#         form = response.xpath("//form[@name='SelHorse']")
#         sirename_dirty = response.xpath('//font[text()="Sire"]/../'
#         'following-sibling::td/font/a/text()'
#         ).extract() or response.xpath('//font[text()="Sire"]/../'
#         'following-sibling::td/font/text()').extract()
    
#         sirename = sirename_dirty[0].strip() if sirename_dirty else None

#         ownername = response.xpath('//td[font[text()="Owner"]]/'
#         'following-sibling::td/font/a/text()').extract()[0].strip()

#         damname = response.xpath('//td[font[text()="Dam"]]/'
#         'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

#         damsire = response.xpath('//td[font[text()="Dam\'s Sire"]]/'
#         'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

#         meta_dict = response.meta
#         meta_dict.update(
#                     sirename=sirename,
#                     ownername=ownername,
#                     damname=damname,
#                     damsire=damsire
#                 )

#             # tables = form.xpath("table")
#             # if len(tables) < 4:
#             #     print "No such Horse - " + response.url
#             #     # raise Exception("No Such horse")
#             # else:
#             #     #print "Real Horse - " + response.url
#             #     #two versions
#             #     if "OtherHorse.asp" in response.url:
#             #         print "im other horse"
#             #         pass
#             #         # data_table = form.xpath("table//tr//td//font[contains(text(),'Pla')]")[0].xpath("../../..")[0]
#             #         # format_version = 2
#             #     else:
#             #         data_table = form.xpath("table//tr//td//font[contains(text(),'Pla')]")[0].xpath("../../..")[0]
#             #         format_version = 1
#             #         url_path = os.path.dirname(response.url)
#             #         # item = {}
#             #         print "Extracting v1"

#                     # item["h_raceindexes"] = row.xpath("td")[0].xpath("a/text()").extract()[0]
#                         # race_link = url_path + "/" + row.xpath("td")[0].xpath("a/@href").extract()[0]
            
#                     # item["h_raceurls"] = row.xpath("td")[0].xpath("a/@href").extract()[0]
#                     # item["h_places"] = row.xpath("td")[1].xpath("*//text()").extract()[0].strip()
#                     # item["h_racedates"] = datetime.datetime.strptime(
#                     #                 row.xpath("td")[2].xpath("text()").extract()[0].strip(),
#                     #                 "%d/%m/%y")        
#                     # item["h_distances"] = row.xpath("td")[4].xpath("text()").extract()[0].strip()
#                     # item["h_goings"] = row.xpath("td")[5].xpath("text()").extract()[0].strip()
#                     # item["h_raceclasses"] =  row.xpath("td")[6].xpath("text()").extract()[0].strip()
#                     # item["h_draws"] = row.xpath("td")[7].xpath("font").xpath("text()").extract()[0].strip()
#                     # item["h_ratings"] =  row.xpath("td")[8].xpath("text()").extract()[0].strip()
#                     # item["h_trainers"] = " ".join(row.xpath("td")[9].xpath("*//text()").extract()).strip()
#                     # item["h_jockeys"] = " ".join(row.xpath("td")[10].xpath("*//text()").extract()).strip()
                    
#                     # item["h_lbws"] =  row.xpath("td")[11].xpath("*/text()| text()").extract()[0].strip()
                    
#                     # item["h_winoddss"] =  row.xpath("td")[12].xpath("text()").extract()[0].strip()
#                     # item["h_actwts"] =  row.xpath("td")[13].xpath("text()").extract()[0].strip()
#                     # item["h_rps"] = " ".join(row.xpath("td")[14].xpath("*//text()").extract()).strip().replace(unichr(160), "")
#                     # item["h_finishtimes"] = row.xpath("td")[15].xpath("text()").extract()[0].strip()
#                     # item["h_horseweights"] = row.xpath("td")[16].xpath("text()").extract()[0].strip()
#                     # item["h_gears"] = row.xpath("td")[17].xpath("text()").extract()[0].strip()
                    
#                     # meta_dict.update(
#                     #         h_raceindexes = h_raceindexes,
#                     #         h_places=h_places,
#                     #         h_racedates=h_racedates,
#                     #         h_goings=h_goings,
#                     #         h_distances=h_distances,
#                     #         h_raceclasses=h_raceclasses,
#                     #         h_draws=h_draws,
#                     #         h_ratings= h_ratings,
#                     #         h_trainers=h_trainers,
#                     #         h_jockeys=h_jockeys,
#                     #         h_lbws = h_lbws,
#                     #         h_winodds=h_winodds,
#                     #         h_rps=h_rps,
#                     #         h_finishtimes=h_finishtimes,
#                     #         h_horseweights=h_horseweights,
#                     #         h_gears=h_gears
#                     # )

#         yield items.RaceItem(
#             racenumber = response.meta['racenumber'],
#             racedate = response.meta['racedate'],
#             racegoing = response.meta['racegoing'],
#             racecoursecode = response.meta['racecoursecode'],
#             raceindex = response.meta['raceindex'],
#             racingincidentreport = response.meta['racingincidentreport'],
#             horsereport=response.meta['horsereport'],
#             results_url = response.meta['results_url'],
#             horsenumber = response.meta['horsenumber'],
#             horsename = response.meta['horsename'],
#             horsecode = response.meta['horsecode'],
#             sec_timelist = response.meta['sec_timelist'],
#             horse_url =  response.meta['horse_url'],
#             horse_smartform_url=  response.meta['horse_smartform_url'],
#             marginsbehindleader=response.meta['marginsbehindleader'],
#             jockeyname=response.meta['jockeyname'],
#             jockeycode=response.meta['jockeycode'],
#             trainername=response.meta['trainername'],
#             trainercode=response.meta['trainercode'],
#             actualwt=response.meta['actualwt'],
#             declarhorsewt=response.meta['declarhorsewt'],
#             jockey2horsewt=response.meta['jockey2horsewt'],
#             draw=response.meta['draw'],
#             lbw=response.meta['lbw'],
#             runningposition=response.meta['runningposition'],
#             finishtime=response.meta['finishtime'],
#             winodds = response.meta['winodds'],
#             isScratched = response.meta['isScratched'],
#             placenum = response.meta['placenum'],
#             place = response.meta['place'],
#             winoddsrank= response.meta['winoddsrank'],
#             runners_list=response.meta['runners_list'],
#             sirename=response.meta['sirename'],
#             ownername=response.meta['ownername'],
#             damname=response.meta['damname'],
#             damsire=response.meta['damsire']

#                      # h_raceindexes = h_raceindexes,
#                         # h_places=h_places,
#                         # h_racedates=h_racedates,
#                         # h_goings=h_goings,
#                         # h_distances=h_distances,
#                         # h_raceclasses=h_raceclasses,
#                         # h_draws=h_draws,
#                         # h_ratings= h_ratings,
#                         # h_trainers=h_trainers,
#                         # h_jockeys=h_jockeys,
#                         # h_lbws = h_lbws,
#                         # h_winodds=h_winodds,
#                         # h_rps=h_rps,
#                         # h_finishtimes=h_finishtimes,
#                         # h_horseweights=h_horseweights,
#                         # h_gears=h_gears

#         )



#                 # print "Found %d rows" % len(rows)


#                 # meta_dict = response.meta
#                 # meta_dict.update(
#                 #     sirename=sirename,
#                 #     ownername=ownername,
#                 #     damname=damname,
#                 #     damsire=damsire
#                 # )
#                 # print sirename, ownername, damname, damsire

#                 # season = ""
#                 # # url = response.url
#                 # # url_path = os.path.dirname(url)
#                 # rows = data_table.xpath("tr")
#                 # if format_version == 1:
#                 # # # Skip the 0th row as it contains headers
#                 #     counter = 2
#                 #     for row in rows[1:]:
#                 #         item = {}
#                 #         print row.xpath("td")[1].xpath("*//text()").extract()[0].strip()
#                         # print row.xpath("td")[0].xpath("a/text()").extract()[0]
#                 #     # If the row only contains one td, it indicates a season sub heading
#                 #     # Season stays the same until we find another seasons a few rows later
#                 #     #print "Processing row %s" % counter
#                 #     if len(row.xpath("td")) == 1:
#                 #         td = row.xpath("td")[0]
#                 #         season = " ".join(td.xpath("*//text()").extract())
#                 # # #         # remove Non-breaking white spaces 
#                 #         season = season.replace(unichr(160), "")
#                 #         print "row %d contains season subheading %s" % (counter, season)
#                 #         counter += 1
#                 #     else:
#                 # # #         # New Format Page 
                        
#                 #             item["h_raceindex"] = row.xpath("td")[0].xpath("*/font/a/text()").extract()[0]
#                 #             print item["h_raceindex"]
#                             # try:
#                                 # item = extract_data_from_row_v1(response, season, row)
#                                 # return item

#                 # #                 # We are done processing the row. Append the values to the elements of 
#                 # #                 # horse dict
#                 #                 if item["h_racedate"] < self.racedateobj:
#                 #                     for key in item.keys():
#                 #                         if key not in horse.keys():
#                 #                             horse[key] = []
#                 #                         horse[key].append(item[key])
#                 #                     # num_races_processed += 1
#                             # except:
#                             #     print "Suppressed row %d" % ( counter )
#                 #         else:
#                 #             pass
#                 # #             # New Format Page 
#                 # #             try:
#                 # #                 item = extract_data_from_row_v1(response, season, row)
#                 # #                 # We are done processing the row. Append the values to the elements of 
#                 # #                 # horse dict
#                 # #                 if item["h_racedate"] <= self.racedateobj:
#                 # #                     for key in item.keys():
#                 # #                         if key not in horse.keys():
#                 # #                             horse[key] = []
#                 # #                         horse[key].append(item[key])
#                 # #                         num_races_processed += 1
#                 # #             except:
#                 # #                 # print "Suppressed row %d" % ( counter )
#                 # #                 # print '-'*60
#                 # #                 traceback.print_exc(file=sys.stdout)
#                 # #                 # print '-'*60
#                 # #         # counter += 1
#         # except:
#         #     print "Unknown error" 
#         #     print '-'*60
#         #     # traceback.print_exc(file=sys.stdout)
#         #     print '-'*60
#         #both versions?







#         ###ONTO MAIN TABLE##
#         # race_rows_selector = response.xpath('//table[@class="bigborder"]//tr[@bgcolor]')
        
#         # ##HISTORICAL RUNS - get all then filter by valid dates

#         # # h_racedate2 = np.array([], dtype=(str,50))
#         # h_racedate = []
#         # h_place = []
#         # h_lbw = []
#         # h_rp1 = []
#         # h_racelink = []
#         # h_rc_track_course = [] 
#         # h_distance = []
#         # h_rating = []
#         # h_ftime = []
#         # h_rc = []
#         # h_draw = []
#         # h_sp = []
#         # h_actualwt = []
#         # h_raceclass = []
#         # h_raceindex = []

#         # '''
#         # smart form
#         # http://racing.hkjc.com/racing/info/horse/smartform/english/S280

#         # ''' 
#         # ##critical columns are racedate, place, rating, distance, draw, sp, raceclass, ftime
#         # for race_raw_sel in race_rows_selector:
#         #     # h_racelink.append(race_raw_sel.xpath('td[position()=1 and text()!="Overseas"]/a/@href').extract()[0])
#         #     try:
#         #         #RACEINDEX, Place, Racedate, 
#         #         h_raceindex.append(race_raw_sel.xpath('td[1]//font/a[contains(@href, "results")]/text()').extract()[0])
#         #         h_place.append(race_raw_sel.xpath('td[2]//div/font/text()').extract()[0])
#         #         # np.append(h_racedate2, race_raw_sel.xpath('td[3]/div/font/text()[not(contains(.,"\r\n"))]').extract())
#         #         h_racedate.append(
#         #             race_raw_sel.xpath('td[3]/div/font/text()[not(contains(.," "))]').extract()[0]
#         #             )
#         #         # ##fix blanks
#         #         # h_racedate = np.array(filter(lambda x: x != '' and x is not None, h_racedate))
#         #         h_actualwt.append(race_raw_sel.xpath('td[14]/div/font//text()').extract()[0])
#         #         # h_rc_track_course.append( unicode.strip(u''.join( race_raw_sel.xpath('td[4]//text()').extract())).replace(u' ', u''))
#         #         h_distance.append(race_raw_sel.xpath('td[5]//text()').extract()[0])
#         #         h_rating.append( race_raw_sel.xpath('td[9]//text()').extract()[0])
#         #         h_lbw.append(race_raw_sel.xpath('td[12]//font/text()').extract())
#         #         h_ftime.append( race_raw_sel.xpath('td[16]//text()').extract()[0])
#         #         h_draw.append( race_raw_sel.xpath('td[8]//text()').extract()[0])
#         #         # h_sp.append(race_raw_sel.xpath('td[13]/center/font//text()').extract()[0])
            
#         #         # h_lbw.append(race_raw_sel.xpath('td[12]//font/text()').extract())
#         #         # h_rp1.append(race_raw_sel.xpath('td[15]//text()').extract())
#         #         # h_ftime.append( race_raw_sel.xpath('td[16]//text()').extract()[0])
#         #         # h_draw.append( race_raw_sel.xpath('td[8]//text()').extract()[0])
#         #         # h_sp.append(race_raw_sel.xpath('td[13]//text()').extract()[0])
#         #     except IndexError, ValueError:
#         #         continue
#         # assert len(h_raceindex) == len(h_place) == len(h_racedate)==len(h_actualwt)

#         # print("I am a horse")
#         # print(h_racedate2, h_racedate)
#         # # print(len(h_raceindex),len(h_place),len(h_racedate),len(h_actualwt),len(h_rc_track_course),
#         # # len(h_distance),len(h_rating),len(h_lbw),len(h_rp1),len(h_ftime),len(h_draw),len(h_sp))
       
#         # # assert len(h_raceindex) == len(h_place)== len(h_racedate)== len(h_actualwt)== len(h_rc_track_course)==len(h_distance)\
#         # # ==len(h_winningratings)==len(h_lbw)==len(h_rp1)==len(h_ftime)==len(h_draw)==len(h_sp)
#         # # # ==len(h_rc_track_course)
#         #  #  == len(h_actualwt) == len(h_sp)
#         # # ri_racedate_place_wt = map(lambda a, b,c,d: a + "_" + b + "_" + c + "_"+d, h_raceindex, h_racedate, h_actualwt,h_place)



#         # #combine raceindex-racedate=horsecode-hwt-place in table which tracks horses which ran together
#         # # [x for ind, x in enumerate(list1) if 4>ind>0]
#         # # response.meta['racedate'] 

#         # todayssurface_ = unicode.strip(response.meta['racetrack'].split(u'/')[0])
#         # # pprint.pprint(todayssurface_)

#         # season_start = getseasonstart(response.meta['racedate'])

#         # # season_start = datetime.datetime.strptime('24052010', "%d%m%Y").date()
#         # #clean h_racedate
#         # ##convert to objects
#         # h_racedate = [ datetime.strptime(t, '%d/%m/%y') for t in h_racedate]
#         # # todays_racedate = 


#         # valid_race_indexes = []
#         # valid_race_indexes = [ ind for ind,d in enumerate(h_racedate) if d < response.meta['racedate']]


#         # # #d is a date string
#         # # for ind,dt in enumerate(h_racedate):
#         # #     try:
#         # #         # dt = datetime.strptime(d, '%d/%m/%y')
#         # #         if  dt < response.meta['racedate']:
#         # #             valid_race_indexes.append(ind)
#         # #     except ValueError:
#         # #         continue

#         # # this_season_indexes = []
#         # # for ind,d in enumerate(h_racedate):
#         # #     try:
#         # #         # dt = datetime.strptime(d, '%d/%m/%y')
#         # #         if dt > season_start:
#         # #             this_season_indexes.append(ind)
#         # #     except ValueError:
#         # #         break


#         # # valid_race_indexes = [ ind for ind,d in enumerate(h_racedate) if datetime.strptime(try_dateobj(d), '%d/%m/%y') < response.meta['racedate']]
#         # scratch_race_indexes = [ind for ind, p in enumerate(h_place) if processplace(p) == 99]
#         # season_start = getseasonstart(response.meta['racedate'])
#         # this_season_indexes = [ ind for ind,d in enumerate(h_racedate) if d > season_start]
#         # runs_this_season = len(this_season_indexes)
#         # # this_season_indexes = [ ind for ind,d in enumerate(h_racedate) if datetime.strptime(try_dateobj(d), '%d/%m/%y') > season_start]
#         # # pprint.pprint(this_season_indexes)


#         # h_racedate = [ d for ind,d in enumerate(h_racedate) if ind in valid_race_indexes]
#         # ##NEED TO REMOVE SCRATCHES
#         # h_place = [ processplace(p) for ind, p in enumerate(h_place) if ind in valid_race_indexes and ind not in scratch_race_indexes]

#         # #getdraw(d)
#         # h_draw = [ d for ind, d in enumerate(h_draw) if ind in valid_race_indexes]
#         # h_sp = [ sp for ind, sp in enumerate(h_sp) if ind in valid_race_indexes and ind not in scratch_race_indexes]
        

#         # h_actualwt = [ int(w) for ind, w in enumerate(h_actualwt) if ind in valid_race_indexes]
#         # h_lbw = [ horselengthprocessor(l) for ind, l in enumerate(h_lbw) if ind in valid_race_indexes ]
#         # h_rp1 = [ processrp(''.join(rp)) for ind,rp in enumerate(h_rp1) if ind in valid_race_indexes ]
        
#         # #how many horses horse passed (-)

#         # h_passedlsec = [ i.split(u'-')[-1] + (-1)*i.split(u'-')[-2]  for i in h_rp1]

#         # # h_racelink = [ self.sectionalbaseurl+ re.match(r'^results\.asp\?(.*)&venue=.*$', rl).group(1) for ind,rl in enumerate(h_racelink) if ind in valid_race_indexes ]
#         # h_distance = [ int(d) for ind, d in enumerate(h_distance) if ind in valid_race_indexes ]
#         # h_raceclass = [ cleanstring(rc) for ind, rc in enumerate(h_raceclass) if ind in valid_race_indexes ]
#         # h_rating = [ valueordash(r) for ind, r in enumerate(h_rating) if ind in valid_race_indexes ]
#         # h_ftime = [ get_hkjc_ftime(s, u's') for ind, s in enumerate(h_ftime) if ind in valid_race_indexes ]


#         # h_avgspd = np.array([ round(float(a) / float(b),3) for a,b in zip(h_distance, h_ftime) if a is not None and b is not None])
#         # h_avgspd_n = len(h_avgspd)
#         # # h_bestavgspd_season = h_avgspd_season = None
        
#         # # h_bestavgspd_season = h_avgspd_season = None

#         # # if len(this_season_indexes) > 1 and len(h_avgspd) >0:
#         # #     _h_avgspd_season = [ s for ind,s in h_avgspd if ind in this_season_indexes]
#         # #     h_avgspd_season = round(np.mean(np.array(_h_avgspd_season)),2)
#         # #     h_bestavgspd_season = np.amax(np.array(_h_avgspd_season))
#         # # else:
#         # #     ##array one or zero
#         # #     h_avgspd_season = h_avgspd
#         # #     h_bestavgspd_season = h_avgspd
        
        
        
#         # # h_d_indexes = [ ind for ind, d in enumerate(h_distance) if d == response.meta['racedistance']]

#         # h_win_indexes = [ ind for ind, p in enumerate(h_place) if p == 1]
        
#         # h_rc_track_course_ = [ r for ind, r in enumerate(h_rc_track_course) if ind in valid_race_indexes]
#         # h_rc = [ rc.split('/')[0].replace(u'"', '') for rc in h_rc_track_course_]
#         # h_surface = [ (rc.split('/')[1]).replace(u'"', '').upper() for rc in h_rc_track_course_]
#         # h_course = [ rc.split('/')[2].replace(u'"', '') for rc in h_rc_track_course_]
#         # h_rc_indexes = [ ind for ind, rc in enumerate(h_rc) if rc == response.meta['racecoursecode']]
#         # h_d_indexes = [ ind for ind, d in enumerate(h_distance) if d == response.meta['racedistance']]
#         # h_surface_indexes = [ ind for ind, s in enumerate(h_surface) if s == response.meta['racesurface'] ]
#         # # h_rtodayc h_todayd = 
#         # h_winningspeeds = None
#         # h_winningratings = None
#         # h_avgwinninglbw = None

#         # if len(h_win_indexes) >0:
#         #     h_winningspeeds = [ s for ind,s in enumerate(h_avgspd) if ind in h_win_indexes]
#         #     h_winningratings = [ r for ind,r in enumerate(h_rating) if ind in h_win_indexes]
#         #     h_avgwinninglbw = sum([l for ind, l in enumerate(h_lbw) if ind in h_win_indexes])/float(len(h_win_indexes))
        

#         # h_avgspd_surface = h_avgspd_surface_n= None
#         # if (h_surface_indexes is not None) and len(h_avgspd) != 0:
#         #     _avspdsurface_sum = sum([s for ind,s in enumerate(h_avgspd) if ind in h_surface_indexes])
#         #     h_avgspd_surface = round(_avspdsurface_sum  / float(len(h_avgspd)),3)
#         #     h_avgspd_surface_n = len(h_surface_indexes) 

#         # h_avgspd_distance = h_avgspd_distance_n= None
#         # if (h_d_indexes is not None) and len(h_d_indexes) !=0:
#         #     _avspddistance_sum = sum([s for ind,s in enumerate(h_avgspd) if ind in h_d_indexes])
#         #     h_avgspd_distance = round(_avspddistance_sum  / float(len(h_avgspd)),3)
#         #     h_avgspd_distance_n = len(h_d_indexes) 
#         # ##GET MBLs and RP1s for qualifying races
#         # #slice place, lbw based on valid dates

#         # ##get sectionals for each past race for MBW



#         # corr_draw_place = corr_sp_place = corr_avgspd_place = None
#         # # try:
#         # # corr_draw_place = round(spat.distance.correlation(h_draw,h_place),2)
#         # try:
#         #     assert len(h_draw) == len(h_place)
#         #     corr_draw_place = round(np.corrcoef(h_draw,h_place)[1][0],2)
#         # except:
#         #     pass

#         # if len(h_sp) == len(h_place) and len(h_sp)>0:
#         # #     # corr_sp_place = round(spat.distance.correlation(h_sp,h_place),2)
#         #     corr_sp_place = round(np.corrcoef(h_sp,h_place)[1][0],2)

#         # ##is this race a slow/fast race if pos position correlation?
#         # ##use database to store all racetimes

#         # ### LOOKS AT WHETHER HORSE DOES WELL IN FAST PACE RACES
#         # corr_ftime_place = corr_avgspd_place = None
#         # if len(h_ftime) == len(h_place) and len(h_ftime) > 0:
#         #     corr_ftime_place = round(np.corrcoef(h_ftime,h_place)[1][0],2)

#         # if len(h_avgspd) == len(h_place) and len(h_avgspd) >0:
#         #     # corr_avgspd_place = round(spat.distance.correlation(h_avgspd,h_place),2)
#         #     corr_avgspd_place = round(np.corrcoef(h_avgspd,h_place)[1][0],2)
#         # # except:
#         # #     pass
#         # # corr_actualwt_place = round(spat.distance.correlation(h_actualwt,h_place),2)
#         # # self.MeetingDrawPlaceCorr.append(corr_sp_place)



#         # dayssincelastrun_ = None
#         # if len(h_racedate) >0:
#         #     dayssincelastrun_ = (response.meta['racedate']- h_racedate[0]).days

#         # # pprint.pprint(h_racedate)
#         # ## text[]
#         # yield items.HkjcHorseItem(
#         #     racecoursecode = response.meta['racecoursecode'],
#         #     racedate = response.meta['racedate'],
#         #     racenumber=try_int(response.meta['racenumber']),
#         #     raceindex=try_int(response.meta['raceindex']),
#         #     racename=response.meta['racename'],
#         #     racetime=response.meta['racetime'],
#         #     # raceclass=response.meta['raceclass'],
#         #     racedistance=try_int(response.meta['racedistance']),
#         #     racegoing=response.meta['racegoing'],
#         #     racetrack=response.meta['racetrack'],
#         #     racesurface=response.meta['racesurface'],
#         #     ##DIVIDEND DATA HERE




#         #     # horsecodelist=response.meta['horsecodelist'],
#         #     racingincidentreport=cleanstring(response.meta['racingincidentreport']),
#         #     horsenumber=try_int(response.meta['horsenumber']),
#         #     horsename=response.meta['horsename'],
#         #     horsecode=response.meta['horsecode'],
#         #     timelist=response.meta['timelist'],
#         #     # zero2finish = getsplits(response.meta['racedistance'], response.meta['timelist']),
#         #     jockeyname=response.meta['jockeyname'],
#         #     jockeycode=response.meta['jockeycode'],
#         #     trainername=response.meta['trainername'],
#         #     trainercode=response.meta['trainercode'],
#         #     actualwt=try_int(response.meta['actualwt']),
#         #     declarhorsewt=try_int(response.meta['declarhorsewt']),
#         #     jockey2horsewt=round(response.meta['jockey2horsewt'],2),
#         #     draw=try_int(response.meta['draw']),
#         #     lbw=horselengthprocessor(response.meta['lbw']),
#         #     position=processplace(response.meta['runningposition'][-1]),
#         #     horsereport=getHorseReport(response.meta['racingincidentreport'],response.meta['horsename']),
#         #     runningposition=map(int, response.meta['runningposition']),
#         #     finishtime=response.meta['finishtime'],
#         #     # winoddsrank=response.meta['winoddsrank'],
#         #     marginsbehindleader=map(horselengthprocessor, response.meta['marginsbehindleader']),
#         #     earlypacepoints = getearlypacepoints( issprint(response.meta['racecoursecode'],response.meta['racedistance']),
#         #         response.meta['marginsbehindleader'][0], response.meta['runningposition'][0]),
#         #     sirename=sirename,
#         #     h_racedate=h_racedate,
#         #     h_lbw = h_lbw,
#         #     h_rp= h_rp1,
#         #     h_place=h_place,
#         #     # h_racelink=h_racelink,
#         #     h_rating=h_rating,
#         #     h_distance=h_distance,
#         #     h_raceclass=h_raceclass,
#         #     # h_rc_track_course= h_rc_track_course,
#         #     h_rc = h_rc,
#         #     h_surface = h_surface,
#         #     h_sp= h_sp,
#         #     h_course = h_course,
#         #     h_ftime = h_ftime,
#         #     h_avgspd= h_avgspd,
#         #     h_avgspd_n=h_avgspd_n,
#         #     h_winningspeeds=h_winningspeeds,
#         #     h_winningratings=h_winningratings,
#         #     h_avgwinninglbw =h_avgwinninglbw,
#         #     ownername=ownername,
#         #     dam=dam,
#         #     damsire=damsire,
#         #     corr_draw_place=corr_draw_place,
#         #     corr_ftime_place=corr_ftime_place,
#         #     corr_sp_place=corr_sp_place,
#         #     corr_avgspd_place=corr_avgspd_place,
#         #     h_avgspd_surface=h_avgspd_surface,
#         #     h_avgspd_surface_n=h_avgspd_surface_n,
#         #     h_avgspd_distance=h_avgspd_distance,
#         #     h_avgspd_distance_n=h_avgspd_distance_n,
#         #     dayssincelastrun= dayssincelastrun_,
#         #     h_passedlsec=h_passedlsec,
#         #     runs_this_season=runs_this_season,
#         #     h_bestavgspd_season=h_bestavgspd_season,
#         #     h_avgspd_season =h_avgspd_season
#         # )

#     # def parse_horse2(self, response):

#     #     sirename = response.xpath('//th[text()="Sire"]/following-sibling::td/'
#     #         'a/text()').extract()[0]
#     #     race_rows_selector = response.xpath('(//tr[@class="even"] | //tr['
#     #         '@class="even"]/preceding-sibling::tr[1])[position()<6]')


#         # yield items.HkjcHorseItem(
#         #     racenumber=try_int(response.meta['racenumber']),
#         #     raceindex=try_int(response.meta['raceindex']),
#         #     racename=response.meta['racename'],
#         #     raceclass=response.meta['raceclass'],
#         #     racedistance=try_int(response.meta['racedistance']),
#         #     racegoing=response.meta['racegoing'],
#         #     racetrack=response.meta['racetrack'],
#         #     # horsecodelist=response.meta['horsecodelist'],
#         #     racingincidentreport=response.meta['racingincidentreport'],
#         #     horsenumber=try_int(response.meta['horsenumber']),
#         #     horsename=response.meta['horsename'],
#         #     horsecode=response.meta['horsecode'],
#         #     position=processplace(response.meta['runningposition'][-1]),
#         #     horsereport=getHorseReport(response.meta['racingincidentreport'],response.meta['horsename']),
#         #     timelist=response.meta['timelist'],
#         #     jockeyname=response.meta['jockeyname'],
#         #     jockeycode=response.meta['jockeycode'],
#         #     trainername=response.meta['trainername'],
#         #     trainercode=response.meta['trainercode'],
#         #     actualwt=try_int(response.meta['actualwt']),
#         #     declarhorsewt=try_int(response.meta['declarhorsewt']),
#         #     jockey2horsewt=round(response.meta['jockey2horsewt'],2),
#         #     draw=try_int(response.meta['draw']),
#         #     lbw=response.meta['lbw'],
#         #     runningposition=map(int, response.meta['runningposition']),
#         #     finishtime=get_scmp_ftime(response.meta['finishtime']),
#         #     # winoddsrank=response.meta['winoddsrank'],
#         #     marginsbehindleader=map(processmargins, response.meta['marginsbehindleader']),
#         #     sirename=sirename,
#         #     racedate=racedate,
#         #     place=place,
#         #     final_sec_time=final_sec_time,
#         #     ownername=ownername,
#         #     dam=dam,
#         #     damsire=damsire,
#         # )

#     def parse_horse_smartform(self,response):
   
#         ## OWNER SIRENAME, DAMNAME, DAMSIRE
#         owner = response.xpath('//a[contains(@href, "horseowner")]/text()').extract()[0].strip()
#         sire = response.xpath('//a[contains(@href, "SameSire")]/text()').extract()[0].strip()
#         dam = response.xpath('//tr[position()=15]/td').extract()[0].split()
#         damsire = response.xpath('//tr[position()=16]/td').extract()[0].split()

#         ##main table
#         race_rows_selector = response.xpath("//table[@class='infoTable']/tr[not(contains(@class, 'header')) and position()>2]")

#         h_raceindex = np.array([], dtype=(int))
#         h_place = np.array([], dtype=int)
#         h_racedate = np.array([], dtype=(str,50))
#         h_rc_track_course = np.array([], dtype=(str,50))
#         h_distance = np.array([], dtype=int)
#         h_going = np.array([], dtype=(str,3))
#         h_raceclass = np.array([], dtype=(str,3))
#         h_draw = np.array([], dtype=int)
#         h_actualweight = np.array([], dtype=int)
#         # h_jockey = np.array([], dtype=(str,50))
#         # h_lbw = np.array([], dtype=(str,50))
#         # h_sp = np.array([], dtype=(str,50))
#         # h_rp = np.array([], dtype=(str,50))
#         # h_ftime= np.array([], dtype=(str,50))
#         # h_finalsec =np.array([], dtype=(str,50))
#         # h_horseweight = np.array([], dtype=int)
#         # h_gear =np.array([], dtype=(str,50))



#         for race_raw_sel in race_rows_selector:
#             np.append(h_raceindex, race_raw_sel.xpath('td[1]/a[contains(@href, "results")]/text()').extract()[0])
#             np.append(h_place, race_raw_sel.xpath('td[2]/text()').extract()[0])
#             np.append(h_racedate, race_raw_sel.xpath('td[3]/text()').extract()[0])
#             np.append(h_rc_track_course, race_raw_sel.xpath('td[4]/text()').extract()[0])
#             np.append(h_distance, race_raw_sel.xpath('td[5]/text()').extract()[0])
#             np.append(h_going, race_raw_sel.xpath('td[6]/text()').extract()[0])
#             np.append(h_raceclass, race_raw_sel.xpath('td[7]/text()').extract()[0])
#             np.append(h_draw, race_raw_sel.xpath('td[8]/text()').extract()[0])
#             np.append(h_actualweight, race_raw_sel.xpath('td[13]/text()').extract()[0])

#         assert len(h_raceindex) == len(h_place) == len(h_racedate) == len(h_rc_track_course)==len(h_distance)==len(h_actualweight)== len(h_draw)

#         #use date objects
#         h_racedates = [ datetime.strptime(t, '%d/%m/%y') for t in h_racedate ]
#         valid_race_indexes = np.array([])
#         valid_race_indexes = [ ind for ind,d in enumerate(h_racedate) if d < response.meta['racedate']]
#         pprint.pprint(h_racedates)
#         ## from raceindex-racedate=horsecode-hwt-place in table which tracks horses which ran together
#         # h_runnertrack = np.array([], dtype=(str,50))
#         # np.append(h_runnertrack, h_raceindex, "|", h_place, "|", h_actualweight, hcode)

#         # pprint.pprint(h_runnertrack)
        


#         yield items.HkjcHorseItem(
#             racecoursecode = response.meta['racecoursecode'],
#             racedate = response.meta['racedate'],
#             racenumber=try_int(response.meta['racenumber']),
#             raceindex=try_int(response.meta['raceindex']),
#             racename=response.meta['racename'],
#             racetime=response.meta['racetime'],
#             # raceclass=response.meta['raceclass'],
#             racedistance=try_int(response.meta['racedistance']),
#             racegoing=response.meta['racegoing'],
#             racetrack=response.meta['racetrack'],
#             racesurface=response.meta['racesurface'],
#             ##DIVIDEND DATA HERE




#             # horsecodelist=response.meta['horsecodelist'],
#             racingincidentreport=cleanstring(response.meta['racingincidentreport']),
#             horsenumber=try_int(response.meta['horsenumber']),
#             horsename=response.meta['horsename'],
#             horsecode=response.meta['horsecode'],
#             timelist=response.meta['timelist'],
#             # zero2finish = getsplits(response.meta['racedistance'], response.meta['timelist']),
#             jockeyname=response.meta['jockeyname'],
#             jockeycode=response.meta['jockeycode'],
#             trainername=response.meta['trainername'],
#             trainercode=response.meta['trainercode'],
#             actualwt=try_int(response.meta['actualwt']),
#             declarhorsewt=try_int(response.meta['declarhorsewt']),
#             jockey2horsewt=round(response.meta['jockey2horsewt'],2),
#             draw=try_int(response.meta['draw']),
#             lbw=horselengthprocessor(response.meta['lbw']),
#             position=processplace(response.meta['runningposition'][-1]),
#             horsereport=getHorseReport(response.meta['racingincidentreport'],response.meta['horsename']),
#             runningposition=map(int, response.meta['runningposition']),
#             finishtime=response.meta['finishtime'],
#             # winoddsrank=response.meta['winoddsrank'],
#             marginsbehindleader=map(horselengthprocessor, response.meta['marginsbehindleader']),
#             earlypacepoints = getearlypacepoints( issprint(response.meta['racecoursecode'],response.meta['racedistance']),
#                 response.meta['marginsbehindleader'][0], response.meta['runningposition'][0]),
#             sirename=sirename,
#             h_racedate=h_racedate,
#             h_lbw = h_lbw,
#             h_rp= h_rp1,
#             h_place=h_place,
#             # h_racelink=h_racelink,
#             h_rating=h_rating,
#             h_distance=h_distance,
#             h_raceclass=h_raceclass,
#             # h_rc_track_course= h_rc_track_course,
#             h_rc = h_rc,
#             h_surface = h_surface,
#             h_sp= h_sp,
#             h_course = h_course,
#             h_ftime = h_ftime,
#             h_avgspd= h_avgspd,
#             h_avgspd_n=h_avgspd_n,
#             h_winningspeeds=h_winningspeeds,
#             h_winningratings=h_winningratings,
#             h_avgwinninglbw =h_avgwinninglbw,
#             ownername=ownername,
#             dam=dam,
#             damsire=damsire,
#             corr_draw_place=corr_draw_place,
#             corr_ftime_place=corr_ftime_place,
#             corr_sp_place=corr_sp_place,
#             corr_avgspd_place=corr_avgspd_place,
#             h_avgspd_surface=h_avgspd_surface,
#             h_avgspd_surface_n=h_avgspd_surface_n,
#             h_avgspd_distance=h_avgspd_distance,
#             h_avgspd_distance_n=h_avgspd_distance_n,
#             dayssincelastrun= dayssincelastrun_,
#             h_passedlsec=h_passedlsec,
#             runs_this_season=runs_this_season
#             # h_bestavgspd_season=h_bestavgspd_season,
#             # h_avgspd_season =h_avgspd_season
#         )