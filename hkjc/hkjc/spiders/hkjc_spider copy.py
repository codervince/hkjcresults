# import re

# import scrapy

# from scrapy.selector import HtmlXPathSelector
# from scrapy.contrib.loader.processor import Join

# import pprint
# from hkjc import items
# from hkjc.utilities import * 
# import operator
# # import scipy.spatial as spat
# from collections import defaultdict
# import itertools
# from itertools import izip_longest
# import numpy as np

# class HorseSpider(scrapy.Spider):

#     name = 'hkjc'

#     def __init__(self, date, racecoursecode, *args, **kwargs):
#         assert racecoursecode in ['ST', 'HV']
#         super(HorseSpider, self).__init__(*args, **kwargs)
#         self.domain = 'hkjc.com'
#         self.racecoursecode = racecoursecode
#         self.racedate = date
#         self.MeetingDrawPlaceCorr = []
#         self.meetingrunners = defaultdict(list)
#         self.sectionalbaseurl = 'http://www.hkjc.com/english/racing/display_sectionaltime.asp?'
#         self.start_urls = [
#             'http://racing.{domain}/racing/Info/Meeting/Results/English/Local/'
#             '{date}/{racecoursecode}/1'.format(domain=self.domain, 
#                 date=date, racecoursecode=racecoursecode),
#         ]

#     def parse(self, response):
#         race_paths = response.xpath('//div[@class="raceNum clearfix"]//'
#             'td[position()!=last()]/a/@href').extract()
#         ##exclude S1 S1 Simulcast
#         ## http://racing.hkjc.com/racing/Info/Meeting/Results/English/Simulcast/20150607/S2/1>

#         race_urls = ['http://racing.{domain}{path}'.format(domain=self.domain, 
#             path=path) for path in race_paths] + self.start_urls
#         for url in race_urls:
#             yield scrapy.Request(url, callback=self.parse_race)

#     def parse_race(self, response):

#         race_text = response.xpath('//div[@class="rowDiv15"]/div[@class='
#             '"boldFont14 color_white trBgBlue"]/text()').extract()
#         racenumber = None
#         raceindex = None
#         if race_text:
#             race_regexp = '^RACE (?P<number>\d+) \((?P<index>\d+)\)$'
#             race_dict = re.match(race_regexp, race_text[0]).groupdict()
#             racenumber = race_dict['number']
#             raceindex = race_dict['index']

#         racecoursecode = self.racecoursecode
#         racedate = datetime.strptime(self.racedate, '%Y%m%d')

#         racename = response.xpath('//div[@class="rowDiv15"]//table[@class='
#             '"tableBorder0 font13"]//tr[2]/td[1]/text()').extract()

#         raceclass = None
#         # raceclass__ = unicode.strip(response.xpath('//td[@class="divWidth"]/text()').extract()[0])
        
#         # raceclass_ = re.match(r'^Class (?P<int>\d+)', raceclass__)
#         # raceclass_ = re.match(r'^Class (?P<int>\d+) - $', raceclass__)

        
#         # raceclass = raceclass_ and raceclass_.groupdict()['int']
   

#         racedistance = None
#         # racedistance_ = response.xpath('//td[@class="divWidth"]/span/text()').extract()[0]
#         # racedistance = re.match(r'^(?P<int>\d+)M.*$', racedistance_).groupdict()['int']

#         racegoing = response.xpath('//td[text() = "Going :"]/'
#             'following-sibling::td/text()').extract()[0]

#         racetrack = response.xpath('//td[text() = "Course :"]/'
#             'following-sibling::td/text()').extract()[0]
#         if u'-' in racetrack: 
#             _racetrack = unicode.strip( racetrack.split('-')[1].replace(u'COURSE', '').replace(u'"', u"'"))
#         else:
#             _racetrack = racetrack

#         ##process this

#         racetime = None
#         _racetimes = response.xpath('//td[text() = "Time :"]/'
#             'following-sibling::td/text()').extract()[0]
#         if len(_racetimes) > 1:
#             racetime = get_hkjc_ftime(_racetimes.split("\t")[-1:][0].replace("(", "").replace(")", ""))


#         # horsecodelist_ = response.xpath('//table[@class="tableBorder trBgBlue'
#         #     ' tdAlignC number12 draggable"]//td[@class="tdAlignL font13'
#         #     ' fontStyle"][1]/text()').extract()
#         # # horsecodelist = [re.match(r'^\((?P<str>.+)\)$', s).groupdict()['str'] for s in horsecodelist_]
#         # pprint.pprint(horsecodelist_)
#         ## add to meeting 
#         # self.meetingrunners[racenumber].append(horsecodelist)
#         # pprint.pprint(self.meetingrunners[racenumber] )
#         # horsecodelist = horsecodelist_
#         racingincidentreport = response.xpath('//tr[td[contains(text(), '
#             '"Racing Incident Report")]]/following-sibling::tr/td/text()'
#             ).extract()[0]

#         sectional_time_url = response.xpath('//div[@class="rowDiv15"]/div['
#             '@class="rowDivRight"]/a/@href').extract()[0]
#         request = scrapy.Request(sectional_time_url, callback=
#             self.parse_sectional_time)
#         meta_dict = {
#             'racecoursecode': racecoursecode,
#             'racedate': racedate,
#             'racetime': racetime,
#             'racenumber': racenumber,
#             'raceindex': raceindex,
#             'racename': racename[0] if racename else None,
#             'raceclass': raceclass,
#             'racedistance': racedistance,
#             'racegoing': racegoing,
#             'racetrack': _racetrack,
#             'racesurface': unicode.strip( racetrack.split('-')[0]),
#             # 'horsecodelist': horsecodelist,
#             'racingincidentreport': racingincidentreport,
#             'results_url': response.url,
#         }
#         request.meta.update(meta_dict)

#         yield request

#     def parse_sectional_time(self, response):

#         horse_lines_selector = response.xpath('//table[@class="bigborder"]//'
#             'table//a/../../..')
#         sectional_time_selector = response.xpath('//table[@class='
#             '"bigborder"]//table//a/../../../following-sibling::tr[1]')
#         for line_selector, time_selector in zip(horse_lines_selector, 
#                 sectional_time_selector):

#             horsenumber = line_selector.xpath('td[1]/div/text()').extract()[0].strip()

#             horse_name_cell = line_selector.xpath('td[3]/div/a/text()').extract()[0]
#             horse_name_regexp = '^(?P<name>[^\(]+)\((?P<code>[^\)]+)\)$'
#             horse_name_dict = re.match(horse_name_regexp, horse_name_cell).groupdict()
#             horsename = horse_name_dict['name']
#             horsecode = horse_name_dict['code']

#             timelist = [time.strip() for time in time_selector.xpath('td/text()').extract()]
#             timelist_len = len(timelist)
#             timelist.extend([None for i in xrange(6-timelist_len)])

#             horse_path = line_selector.xpath('td[3]/div/a/@href').extract()[0]
#             horse_url = 'http://www.{domain}/english/racing/{path}&Option=1#htop'.format(
#                 domain=self.domain, path=horse_path)
#             horse_smartform_url = 'http://racing.hkjc.com/racing/info/horse/smartform/english/{hcode}'.format(
#                 hcode=horsecode)

#             marginsbehindleader = [s.strip('\t\n\r ') for s in line_selector.xpath(
#                 'td//table//td/text()').extract()]
#             marginsbehindleader.extend([None]*(6 - len(marginsbehindleader)))

#             request = scrapy.Request(response.meta['results_url'],
#                 callback=self.parse_results)
#             meta_dict = response.meta
#             meta_dict.update({
#                 'horsenumber': horsenumber,
#                 'horsename': horsename,
#                 'horsecode': horsecode,
#                 'timelist': timelist,
#                 'horse_url': horse_url,
#                 'horse_smartform_url': horse_smartform_url,
#                 'marginsbehindleader': marginsbehindleader,
#             })
#             request.meta.update(meta_dict)

#             yield request

#     def parse_results(self, response):

#         tr = response.xpath('//tr[td[3]/a[text() = "{}"]]'.format(
#             response.meta['horsename']))

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

#         actualwt = tr.xpath('td[6]/text()').extract()[0]

#         declarhorsewt = tr.xpath('td[7]/text()').extract()[0]

#         jockey2horsewt = float(actualwt)/float(declarhorsewt)

#         draw = tr.xpath('td[8]/text()').extract()[0]

#         lbw = tr.xpath('td[9]/text()').extract()[0]

#         runningposition = tr.xpath('td[10]//td/text()').extract()

#         finishtime = tr.xpath('td[11]/text()').extract()[0]

#         winodds = tr.xpath('td[12]/text()').extract()[0]

#         ###WInoddsrank, weight versus average weight, 

#         # winoddsranks = []
#         # try:
#         #     winodds_float = float(winodds)
#         # except ValueError:
#         #     winoddsrank = None
#         # else:
#         #     winoddss = response.xpath('//table[@class="tableBorder trBgBlue '
#         #         'tdAlignC number12 draggable"]//tr[@class="trBgGrey" or @class='
#         #         '"trBgWhite"]/td[12]/text()').extract()
            
#         #     for hc, wo in zip(response.meta['horsecodelist'], winoddss):
#         #         try:
#         #             pprint.pprint(hc)
#         #             pprint.pprint(float(wo))
#         #             winoddsranks.append((hc, float(wo)))
#         #         except ValueError:
#         #             pass
#         #     # sorted_x = sorted(winoddsranks_d.items(), key=operator.itemgetter(1))
#         #     # winoddsrank = sorted_x.index((response.meta['horsecode'],
#         #     #     winodds_float)) + 1
#         #     winoddsranks.sort(key=lambda x: x[1])
#         #     winoddsrank = winoddsranks.index((response.meta['horsecode'],
#         #         winodds_float)) + 1
#         request = scrapy.Request(response.meta['horse_url'],
#             callback=self.parse_horse)
#         # if response.meta['horse_smartform_url']:
#         #     request = scrapy.Request(response.meta['horse_smartform_url'],
#         #     callback=self.parse_horse_smartform)
#         # else:
#         #     request = scrapy.Request(response.meta['horse_url'],
#         #     callback=self.parse_horse)
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
#             # winoddsrank=winoddsrank,
#         )
#         request.meta.update(meta_dict)

#         return request

    

#         ##on regular horse page
#         ##is there a smartform button?
#         # smartf_btn = response.xpath('//a[contains(@href, "smartform")]/font[contains(., "Racing Smart Form")]')
#         # if smartf_btn:
#         #     hcode =  response.meta['horsecode']
#         #     smartf_url = "http://racing.hkjc.com/racing/info/horse/smartform/english/{hcode}".format(hcode=hcode)
#         #     request = scrapy.Request(smartf_url,callback=self.parse_horse_smartform)
#         # else:
#         #     print "no button found"
#         #     pass

    
#     '''
#     switch to nparrays see if all are being picked up 

#     '''

#     ## INCORPORATING AUG 26 HORSES
#     def parse_horse(self, response):

#         ###TOP TABLE###

#         sirename_dirty = response.xpath('//font[text()="Sire"]/../'
#             'following-sibling::td/font/a/text()'
#             ).extract() or response.xpath('//font[text()="Sire"]/../'
#             'following-sibling::td/font/text()').extract()
#         sirename = sirename_dirty[0].strip() if sirename_dirty else None

#         ownername = response.xpath('//td[font[text()="Owner"]]/'
#             'following-sibling::td/font/a/text()').extract()[0].strip()

#         dam = response.xpath('//td[font[text()="Dam"]]/'
#             'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

#         damsire = response.xpath('//td[font[text()="Dam\'s Sire"]]/'
#             'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')


#         ###MAIN TABLE
#         h_racedate = []
#         h_trainer = []
#         h_jockey = []
#         h_place = []
#         h_lbw = []
#         h_rp1 = []
#         h_racelink = []
#         h_track = []
#         h_rc_track_course = []
#         h_racecourse = [] 
#         h_distance = []
#         h_rating = []
#         h_ftime = []
#         h_going = []
#         h_rc = []
#         h_draw = []
#         h_sp = []
#         h_actualwt = []
#         h_raceclass = []
#         h_raceindex = []
#         h_horseweight = []
#         h_gear = []

#         ##wait for indian then incorporate changes
#         hxs = HtmlXPathSelector(response)
#         form = hxs.select("//form[@name='SelHorse']")
#         tables = form.select("table")
#         data_table = tables[3]
#         rows = data_table.select("tr")
#         season = ""

#         for row in rows[1:]:
#             if len(row.select("td")) == 1:
#                 td = row.select("td")[0]
#                 season = " ".join(td.select("*//text()").extract())
#                 season = season.replace(unichr(160),"")
#             else:
#                 item = HkjcItem()
#                 cols = row.select("td")
#                 counter = 0
#             try:
#                 h_raceindex.append(row.select("td")[0].select("*//a/text()").extract()[0])
#                 # item["race_link"] = url_path + "/" + row.select("td")[0].select("*//a/@href").extract()[0]
#             except:
#                 h_raceindex.append(row.select("td")[0].select("*//text()").extract()[0])
#                 # item["race_link"] = "" 
#                 h_place.append(row.select("td")[1].select("*//text()").extract()[0])
#                 h_racedate.append(row.select("td")[2].select("*//text()").extract()[0])
#                 h_rc.append(row.select("td")[3].select("*//text()").extract()[0].replace("/","").replace('"',"").strip())
#                 h_track.append(row.select("td")[3].select("*//text()").extract()[1].replace("/","").replace('"',"").strip())
#             try:
#                 h_racecourse.append(row.select("td")[3].select("*//text()").extract()[2].replace('"',"").strip())
#             except:
#                 # item["racecourse"] = ""
#                 h_distance.append(row.select("td")[4].select("*//text()").extract()[0])
#                 h_trainer.append(" ".join(row.select("td")[9].select("*//text()").extract()).strip())
#                 # item["trainer_link"] = url_path + "/" + row.select("td")[9].select("*/a/@href").extract()[0]
#                 h_jockey.append(" ".join(row.select("td")[10].select("*//text()").extract()).strip())
#                 # h_jockey_link = url_path + "/" + row.select("td")[10].select("*/a/@href").extract()[0]

#         ##TEST THSI FIRST
#         pprint.pprint(h_racedate)
#         assert len(h_raceindex) == len(h_racedate) ==len(h_trainer)== len(h_jockey)

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
#         # h_going = []
#         # h_rc = []
#         # h_draw = []
#         # h_sp = []
#         # h_actualwt = []
#         # h_raceclass = []
#         # h_raceindex = []
#         # h_horseweight = []
#         # h_gear = []

#         '''
#         smart form
#         http://racing.hkjc.com/racing/info/horse/smartform/english/S280
#         ##retired horses have different formats?!


#         '''

#         #what kind of page do we have?
#         #get first row col 3 how long is string?
#         # retiredstyle = False
#         # HISTORICAL_RACES = 0
#         # retiredstyle = bool(response.xpath('//table[@class="bigborder"]//tr[@bgcolor][1]//td[3]/div/font/text()').extract())        
#         # if retiredstyle:
#         #     HISTORICAL_RACES = response.xpath('count(//table[@class="bigborder"]//tr[@bgcolor]//td[3]/div/font/text())').extract()
#         # else:
#         #     HISTORICAL_RACES = response.xpath('count(//table[@class="bigborder"]//tr[@bgcolor]//td[3]/text())').extract()
#         # ##this lopp also needs to make sure all the rows are obtained!!
#         # h_race_counter = 0
#         # for race_raw_sel in race_rows_selector:
#         #     # h_racelink.append(race_raw_sel.xpath('td[position()=1 and text()!="Overseas"]/a/@href').extract()[0])
#         #     try:
#         #         if retiredstyle:
#         #             h_raceindex.append(race_raw_sel.xpath('td[1]//div/font/a[contains(@href, "results")]/text()').extract()[0])
#         #             h_place.append(race_raw_sel.xpath('td[2]//div/font//text()').extract()[0])
#         #             h_racedate.append( race_raw_sel.xpath('td[3]//div/font//text()').extract()[0] )
#         #             h_rc_track_course.append( unicode.strip(u''.join( race_raw_sel.xpath('td[4]//text()|td[4]//div//text()').extract())).replace(u' ', u''))
#         #             h_distance.append(race_raw_sel.xpath('td[5]/div/font//text()').extract()[0])
#         #             h_going.append( race_raw_sel.xpath('td[6]/div/font//text()').extract()[0])
#         #             h_raceclass.append( race_raw_sel.xpath('td[7]/div/font//text()').extract()[0])
#         #             h_draw.append( race_raw_sel.xpath('td[8]/font//text()|td[8]/div/font//text()').extract()[0])
#         #             h_rating.append( race_raw_sel.xpath('td[9]/div/font//text()').extract()[0])
#         #             h_lbw.append(race_raw_sel.xpath('td[12]/div//font/text()').extract())
#         #             h_sp.append(race_raw_sel.xpath('td[13]//text()').extract()[0])
#         #             h_actualwt.append(race_raw_sel.xpath('td[14]//text()').extract()[0])
#         #             h_rp1.append(race_raw_sel.xpath('td[15]//text()').extract()[0]) #should be the same
#         #             h_ftime.append( race_raw_sel.xpath('td[16]/div/font//text()').extract()[0])
#         #             h_horseweight.append( race_raw_sel.xpath('td[17]/div/font//text()').extract()[0])
#         #             h_gear.append( race_raw_sel.xpath('td[18]/div/font//text()').extract()[0])
#         #         else:    
#         #             h_raceindex.append(race_raw_sel.xpath('td[1]//font/a[contains(@href, "results")]/text()').extract()[0])
#         #             h_place.append(race_raw_sel.xpath('td[2]//font//text()|').extract()[0])
#         #             h_racedate.append( race_raw_sel.xpath('td[3]//text()').extract()[0] )
#         #             h_rc_track_course.append( unicode.strip(u''.join( race_raw_sel.xpath('td[4]//text()|td[4]//div//text()').extract())).replace(u' ', u''))
#         #             h_distance.append(race_raw_sel.xpath('td[5]//text()|td[5]/div/font//text()').extract()[0])
#         #             h_going.append( race_raw_sel.xpath('td[6]//text()|td[6]/div/font//text()').extract()[0])
#         #             h_raceclass.append( race_raw_sel.xpath('td[7]//text()').extract()[0])
#         #             h_distance.append(race_raw_sel.xpath('td[5]//text()').extract()[0])
#         #             h_going.append( race_raw_sel.xpath('td[6]//text()').extract()[0])
#         #             h_raceclass.append( race_raw_sel.xpath('td[7]//text()').extract()[0])

#         #             h_draw.append( race_raw_sel.xpath('td[8]/font//text()').extract()[0])
#         #             h_rating.append( race_raw_sel.xpath('td[9]//text()').extract()[0])

#         #             h_lbw.append(race_raw_sel.xpath('td[12]//font/text()').extract())
#         #             h_sp.append(race_raw_sel.xpath('td[13]/center/font//text()').extract()[0])
#         #             h_actualwt.append(race_raw_sel.xpath('td[14]/div/font//text()').extract()[0])
#         #             h_rp1.append(race_raw_sel.xpath('td[15]//text()').extract()[0]) #should be the same
#         #             h_ftime.append( race_raw_sel.xpath('td[16]//text()').extract()[0])
#         #             h_horseweight.append( race_raw_sel.xpath('td[17]//text()').extract()[0])
#         #             h_gear.append( race_raw_sel.xpath('td[18]//text()').extract()[0])
#         #             h_race_counter +=1
#         #     except IndexError, ValueError:
#         #         continue
#         # assert len(h_raceindex) == len(h_place) == len(h_racedate)==len(h_actualwt)


#         ###TESTING
#         # print("I am a horse")
#         # print(h_racedate2, h_racedate)
#         # # print(len(h_raceindex),len(h_place),len(h_racedate),len(h_actualwt),len(h_rc_track_course),
#         # # len(h_distance),len(h_rating),len(h_lbw),len(h_rp1),len(h_ftime),len(h_draw),len(h_sp))
       
#         # # assert len(h_raceindex) == len(h_place)== len(h_racedate)== len(h_actualwt)== len(h_rc_track_course)==len(h_distance)\
#         # # ==len(h_winningratings)==len(h_lbw)==len(h_rp1)==len(h_ftime)==len(h_draw)==len(h_sp)
#         # # # ==len(h_rc_track_course)
#         #  #  == len(h_actualwt) == len(h_sp)
#         #####
        
#         ## DO THIS ON IMPORT
#         # #combine raceindex-racedate=horsecode-hwt-place in table which tracks horses which ran together
#         # # [x for ind, x in enumerate(list1) if 4>ind>0]
#         # # response.meta['racedate'] 
#         ####
#         # print "No historical races " + str(response.meta['horsecode']) + "  "
#         # print(h_race_counter)

#         # todayssurface_ = unicode.strip(response.meta['racetrack'].split(u'/')[0])
#         # # # pprint.pprint(todayssurface_)
#         # # print(len(h_racedate))

#         # valid_race_indexes = []

#         #d is a date string
#         # for ind,dt in enumerate(h_racedate):
#         #     try:
#         #         dt = getdateobject(dt)
#         #         if  dt < response.meta['racedate']:
#         #             valid_race_indexes.append(ind)
#         #     except ValueError:
#         #         continue

#         # # this_season_indexes = []
#         # # for ind,d in enumerate(h_racedate):
#         # #     try:
#         # #         # dt = datetime.strptime(d, '%d/%m/%y')
#         # #         if dt > season_start:
#         # #             this_season_indexes.append(ind)
#         # #     except ValueError:
#         # #         break


#         valid_race_indexes = [ ind for ind,d in enumerate(h_racedate) if getdateobject(d) < response.meta['racedate']]
#         scratch_race_indexes = [ind for ind, p in enumerate(h_place) if processplace(p) == 99]
#         season_start = getseasonstart(response.meta['racedate'])

#         pprint.pprint(valid_race_indexes)
#         # this_season_indexes = [ ind for ind,d in enumerate(h_racedate) if datetime.strptime(d, '%d/%m/%y') > season_start]
#         # runs_this_season = len(this_season_indexes)
#         # print(runs_this_season)


#         h_racedate = [ d for ind,d in enumerate(h_racedate) if ind in valid_race_indexes]

#         h_place = [ processplace(p) for ind, p in enumerate(h_place) if ind in valid_race_indexes and ind not in scratch_race_indexes]

#         # #getdraw(d)
#         h_draw = [ d for ind, d in enumerate(h_draw) if ind in valid_race_indexes]
#         h_sp = [ sp for ind, sp in enumerate(h_sp) if ind in valid_race_indexes and ind not in scratch_race_indexes]
        
#         assert len(h_draw) == len(h_place) == len(h_racedate)
#         # len(h_sp) 
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
#         #     runs_this_season=runs_this_season
#             # h_bestavgspd_season=h_bestavgspd_season,
#             # h_avgspd_season =h_avgspd_season
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