import re

import scrapy
import pprint
from hkjc import items
from hkjc.utilities import * 
import operator
import scipy.spatial as spat


class HorseSpider(scrapy.Spider):

    name = 'hkjc'

    def __init__(self, date, racecoursecode, *args, **kwargs):
        assert racecoursecode in ['ST', 'HV']
        super(HorseSpider, self).__init__(*args, **kwargs)
        self.domain = 'hkjc.com'
        self.racecoursecode = racecoursecode
        self.racedate = date
        self.MeetingDrawPlaceCorr = []
        self.sectionalbaseurl = 'http://www.hkjc.com/english/racing/display_sectionaltime.asp?'
        self.start_urls = [
            'http://racing.{domain}/racing/Info/Meeting/Results/English/Local/'
            '{date}/{racecoursecode}/1'.format(domain=self.domain, 
                date=date, racecoursecode=racecoursecode),
        ]

    def parse(self, response):
        race_paths = response.xpath('//div[@class="raceNum clearfix"]//'
            'td[position()!=last()]/a/@href').extract()
        race_urls = ['http://racing.{domain}{path}'.format(domain=self.domain, 
            path=path) for path in race_paths] + self.start_urls
        for url in race_urls:
            yield scrapy.Request(url, callback=self.parse_race)

    def parse_race(self, response):

        race_text = response.xpath('//div[@class="rowDiv15"]/div[@class='
            '"boldFont14 color_white trBgBlue"]/text()').extract()
        racenumber = None
        raceindex = None
        if race_text:
            race_regexp = '^RACE (?P<number>\d+) \((?P<index>\d+)\)$'
            race_dict = re.match(race_regexp, race_text[0]).groupdict()
            racenumber = race_dict['number']
            raceindex = race_dict['index']

        racecoursecode = self.racecoursecode
        racedate = datetime.strptime(self.racedate, '%Y%m%d')

        racename = response.xpath('//div[@class="rowDiv15"]//table[@class='
            '"tableBorder0 font13"]//tr[2]/td[1]/text()').extract()

        raceclass = None
        raceclass__ = unicode.strip(response.xpath('//td[@class="divWidth"]/text()').extract()[0])
        raceclass_ = re.match(r'^[cC]lass (?P<int>\d+) - $', raceclass__)
        raceclass = raceclass_ and raceclass_.groupdict()['int']

        racedistance_ = response.xpath('//td[@class="divWidth"]/span/text()'
            ).extract()[0]
        racedistance = re.match(r'^(?P<int>\d+)M.*$', racedistance_).groupdict()['int']

        racegoing = response.xpath('//td[text() = "Going :"]/'
            'following-sibling::td/text()').extract()[0]

        racetrack = response.xpath('//td[text() = "Course :"]/'
            'following-sibling::td/text()').extract()[0]

        horsecodelist_ = response.xpath('//table[@class="tableBorder trBgBlue'
            ' tdAlignC number12 draggable"]//td[@class="tdAlignL font13'
            ' fontStyle"][1]/text()').extract()
        horsecodelist = [re.match(r'^\((?P<str>.+)\)$', s).groupdict()['str'] for s in horsecodelist_]
        

        racingincidentreport = response.xpath('//tr[td[contains(text(), '
            '"Racing Incident Report")]]/following-sibling::tr/td/text()'
            ).extract()[0]

        sectional_time_url = response.xpath('//div[@class="rowDiv15"]/div['
            '@class="rowDivRight"]/a/@href').extract()[0]
        request = scrapy.Request(sectional_time_url, callback=
            self.parse_sectional_time)
        meta_dict = {
            'racecoursecode': racecoursecode,
            'racedate': racedate,
            'racenumber': racenumber,
            'raceindex': raceindex,
            'racename': racename[0] if racename else None,
            'raceclass': raceclass,
            'racedistance': racedistance,
            'racegoing': racegoing,
            'racetrack': unicode.strip( racetrack.split('-')[1].replace(u'COURSE', '').replace(u'"', u"'")),
            'racesurface': unicode.strip( racetrack.split('-')[0]),
            'horsecodelist': horsecodelist,
            'racingincidentreport': racingincidentreport,
            'results_url': response.url,
        }
        request.meta.update(meta_dict)

        yield request

    def parse_sectional_time(self, response):

        horse_lines_selector = response.xpath('//table[@class="bigborder"]//'
            'table//a/../../..')
        sectional_time_selector = response.xpath('//table[@class='
            '"bigborder"]//table//a/../../../following-sibling::tr[1]')
        for line_selector, time_selector in zip(horse_lines_selector, 
                sectional_time_selector):

            horsenumber = line_selector.xpath('td[1]/div/text()').extract()[0].strip()

            horse_name_cell = line_selector.xpath('td[3]/div/a/text()').extract()[0]
            horse_name_regexp = '^(?P<name>[^\(]+)\((?P<code>[^\)]+)\)$'
            horse_name_dict = re.match(horse_name_regexp, horse_name_cell).groupdict()
            horsename = horse_name_dict['name']
            horsecode = horse_name_dict['code']

            timelist = [time.strip() for time in time_selector.xpath('td/text()').extract()]
            timelist_len = len(timelist)
            timelist.extend([None for i in xrange(6-timelist_len)])

            horse_path = line_selector.xpath('td[3]/div/a/@href').extract()[0]
            horse_url = 'http://www.{domain}/english/racing/{path}&Option=1#htop'.format(
                domain=self.domain, path=horse_path)

            marginsbehindleader = [s.strip('\t\n\r ') for s in line_selector.xpath(
                'td//table//td/text()').extract()]
            marginsbehindleader.extend([None]*(6 - len(marginsbehindleader)))

            request = scrapy.Request(response.meta['results_url'],
                callback=self.parse_results)
            meta_dict = response.meta
            meta_dict.update({
                'horsenumber': horsenumber,
                'horsename': horsename,
                'horsecode': horsecode,
                'timelist': timelist,
                'horse_url': horse_url,
                'marginsbehindleader': marginsbehindleader,
            })
            request.meta.update(meta_dict)

            yield request

    def parse_results(self, response):

        tr = response.xpath('//tr[td[3]/a[text() = "{}"]]'.format(
            response.meta['horsename']))

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

        actualwt = tr.xpath('td[6]/text()').extract()[0]

        declarhorsewt = tr.xpath('td[7]/text()').extract()[0]

        jockey2horsewt = float(actualwt)/float(declarhorsewt)

        draw = tr.xpath('td[8]/text()').extract()[0]

        lbw = tr.xpath('td[9]/text()').extract()[0]

        runningposition = tr.xpath('td[10]//td/text()').extract()

        finishtime = tr.xpath('td[11]/text()').extract()[0]

        winodds = tr.xpath('td[12]/text()').extract()[0]
        # winoddsranks = []
        # try:
        #     winodds_float = float(winodds)
        # except ValueError:
        #     winoddsrank = None
        # else:
        #     winoddss = response.xpath('//table[@class="tableBorder trBgBlue '
        #         'tdAlignC number12 draggable"]//tr[@class="trBgGrey" or @class='
        #         '"trBgWhite"]/td[12]/text()').extract()
            
        #     for hc, wo in zip(response.meta['horsecodelist'], winoddss):
        #         try:
        #             pprint.pprint(hc)
        #             pprint.pprint(float(wo))
        #             winoddsranks.append((hc, float(wo)))
        #         except ValueError:
        #             pass
        #     # sorted_x = sorted(winoddsranks_d.items(), key=operator.itemgetter(1))
        #     # winoddsrank = sorted_x.index((response.meta['horsecode'],
        #     #     winodds_float)) + 1
        #     winoddsranks.sort(key=lambda x: x[1])
        #     winoddsrank = winoddsranks.index((response.meta['horsecode'],
        #         winodds_float)) + 1

        request = scrapy.Request(response.meta['horse_url'],
            callback=self.parse_horse)
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
            # winoddsrank=winoddsrank,
        )
        request.meta.update(meta_dict)

        return request

    def parse_horse(self, response):

        sirename_dirty = response.xpath('//font[text()="Sire"]/../'
            'following-sibling::td/font/a/text()'
            ).extract() or response.xpath('//font[text()="Sire"]/../'
            'following-sibling::td/font/text()').extract()
        sirename = sirename_dirty[0].strip() if sirename_dirty else None
        race_rows_selector = response.xpath('//table[@class="bigborder"]//'
            'tr[@bgcolor]')
        
        ##HISTORICAL RUNS - get all then filter by valid dates

        h_racedate = []
        h_place = []
        h_lbw = []
        h_rp1 = []
        h_racelink = []
        h_rc_track_course = [] 
        h_distance = []
        h_rating = []
        h_ftime = []
        h_rc = []
        h_draw = []
        h_sp = []
        h_actualwt = []
        h_raceclass = []

        for race_raw_sel in race_rows_selector:
            h_racelink.append(race_raw_sel.xpath('td[position()=1 and not(text()="Overseas")]/a/@href').extract()[0])
            h_racedate.append(race_raw_sel.xpath('td[3]/text()').extract()[0])
            h_place.append(race_raw_sel.xpath('td[2]//font/text()').extract()[0])
            h_lbw.append(race_raw_sel.xpath('td[12]//font/text()').extract())
            h_rp1.append(race_raw_sel.xpath('td[15]//text()').extract())
            h_rc_track_course.append(  unicode.strip(u''.join( race_raw_sel.xpath('td[4]//text()').extract())).replace(u' ', u''))
            h_distance.append( race_raw_sel.xpath('td[5]//text()').extract()[0])
            h_rating.append( race_raw_sel.xpath('td[9]//text()').extract()[0])
            h_ftime.append( race_raw_sel.xpath('td[16]//text()').extract()[0])
            h_draw.append( race_raw_sel.xpath('td[9]//text()').extract()[0])
            h_sp.append(race_raw_sel.xpath('td[13]//text()').extract()[0])
            h_actualwt.append(race_raw_sel.xpath('td[14]//text()').extract()[0])
            h_raceclass.append(race_raw_sel.xpath('td[7]//text()').extract()[0])
        

        # [x for ind, x in enumerate(list1) if 4>ind>0]
        # response.meta['racedate'] 

        todayssurface_ = unicode.strip(response.meta['racetrack'].split(u'/')[0])
        pprint.pprint(todayssurface_)

        valid_race_indexes = [ ind for ind,d in enumerate(h_racedate) if datetime.strptime(d, '%d/%m/%y') < response.meta['racedate']]
        scratch_race_indexes = [ind for ind, p in enumerate(h_place) if processplace(p) != 99]

        h_racedate = [ datetime.strptime(d, '%d/%m/%y') for ind,d in enumerate(h_racedate) if ind in valid_race_indexes]
        h_place = [ processplace(p) for ind, p in enumerate(h_place) if ind in valid_race_indexes]
        h_draw = [ getdraw(d) for ind, d in enumerate(h_draw) if ind in valid_race_indexes]
        h_sp = [ float(sp) for ind, sp in enumerate(h_sp) if ind in valid_race_indexes and ind not in scratch_race_indexes]
        h_actualwt = [ int(w) for ind, w in enumerate(h_actualwt) if ind in valid_race_indexes]
        h_lbw = [ horselengthprocessor(l) for ind, l in enumerate(h_lbw) if ind in valid_race_indexes ]
        h_rp1 = [ processrp(''.join(rp)) for ind,rp in enumerate(h_rp1) if ind in valid_race_indexes ]
        h_racelink = [ self.sectionalbaseurl+ re.match(r'^results\.asp\?(.*)&venue=.*$', rl).group(1) for ind,rl in enumerate(h_racelink) if ind in valid_race_indexes ]
        h_distance = [ int(d) for ind, d in enumerate(h_distance) if ind in valid_race_indexes ]
        h_raceclass = [ cleanstring(rc) for ind, rc in enumerate(h_raceclass) if ind in valid_race_indexes ]
        h_rating = [ int(r) for ind, r in enumerate(h_rating) if ind in valid_race_indexes ]
        h_ftime = [ get_hkjc_ftime(s, u's') for ind, s in enumerate(h_ftime) if ind in valid_race_indexes ]


        h_avgspd = [ round(float(a) / float(b),3) for a,b in zip(h_distance, h_ftime)]
        h_d_indexes = [ ind for ind, d in enumerate(h_distance) if d == response.meta['racedistance']]

        h_win_indexes = [ ind for ind, p in enumerate(h_place) if p == 1]
        
        h_rc_track_course_ = [ r for ind, r in enumerate(h_rc_track_course) if ind in valid_race_indexes]
        h_rc = [ rc.split('/')[0].replace(u'"', '') for rc in h_rc_track_course_]
        h_surface = [ (rc.split('/')[1]).replace(u'"', '') for rc in h_rc_track_course_]
        h_course = [ rc.split('/')[2].replace(u'"', '') for rc in h_rc_track_course_]
        h_rc_indexes = [ ind for ind, rc in enumerate(h_rc) if rc == response.meta['racecoursecode']]
        h_d_indexes = [ ind for ind, d in enumerate(h_distance) if d == response.meta['racedistance']]
        h_surface_indexes = [ ind for ind, s in enumerate(h_surface) if s == response.meta['racesurface'] ]
        # h_rtodayc h_todayd = 
        h_winningspeeds = None
        h_winningratings = None
        h_avgwinninglbw = None

        if len(h_win_indexes) >0:
            h_winningspeeds = [ s for ind,s in enumerate(h_avgspd) if ind in h_win_indexes]
            h_winningratings = [ r for ind,r in enumerate(h_rating) if ind in h_win_indexes]
            h_avgwinninglbw = sum([l for ind, l in enumerate(h_lbw) if ind in h_win_indexes])/float(len(h_win_indexes))
        

        h_avgspd_surface = None
        if h_surface_indexes is not None:
            h_avgspd_surface = sum([s for ind,s in enumerate(h_avgspd) if ind in h_surface_indexes]) / float(len(h_avgspd)) 
        ##GET MBLs and RP1s for qualifying races
        #slice place, lbw based on valid dates

        ##get sectionals for each past race for MBW
        
        #CORRELATIONS
        
        corr_draw_place = round(spat.distance.correlation(h_draw,h_place),2)
        corr_sp_place = round(spat.distance.correlation(h_sp,h_place),2)
        corr_avgspd_place = round(spat.distance.correlation(h_avgspd,h_place),2)
        # corr_actualwt_place = round(spat.distance.correlation(h_actualwt,h_place),2)
        self.MeetingDrawPlaceCorr.append(corr_sp_place)


        ownername = response.xpath('//td[font[text()="Owner"]]/'
            'following-sibling::td/font/a/text()').extract()[0].strip()

        dam = response.xpath('//td[font[text()="Dam"]]/'
            'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

        damsire = response.xpath('//td[font[text()="Dam\'s Sire"]]/'
            'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

        yield items.HkjcHorseItem(
            racecoursecode = response.meta['racecoursecode'],
            racedate = response.meta['racedate'],
            racenumber=try_int(response.meta['racenumber']),
            raceindex=try_int(response.meta['raceindex']),
            racename=response.meta['racename'],
            raceclass=response.meta['raceclass'],
            racedistance=try_int(response.meta['racedistance']),
            racegoing=response.meta['racegoing'],
            racetrack=response.meta['racetrack'],
            racesurface=response.meta['racesurface'],
            horsecodelist=response.meta['horsecodelist'],
            racingincidentreport=cleanstring(response.meta['racingincidentreport']),
            horsenumber=try_int(response.meta['horsenumber']),
            horsename=response.meta['horsename'],
            horsecode=response.meta['horsecode'],
            timelist=response.meta['timelist'],
            zero2finish = getsplits(response.meta['racedistance'], response.meta['timelist']),
            jockeyname=response.meta['jockeyname'],
            jockeycode=response.meta['jockeycode'],
            trainername=response.meta['trainername'],
            trainercode=response.meta['trainercode'],
            actualwt=try_int(response.meta['actualwt']),
            declarhorsewt=try_int(response.meta['declarhorsewt']),
            jockey2horsewt=round(response.meta['jockey2horsewt'],2),
            draw=try_int(response.meta['draw']),
            lbw=horselengthprocessor(response.meta['lbw']),
            position=processplace(response.meta['runningposition'][-1]),
            horsereport=getHorseReport(response.meta['racingincidentreport'],response.meta['horsename']),
            runningposition=map(int, response.meta['runningposition']),
            finishtime=response.meta['finishtime'],
            # winoddsrank=response.meta['winoddsrank'],
            marginsbehindleader=map(horselengthprocessor, response.meta['marginsbehindleader']),
            earlypacepoints = getearlypacepoints( issprint(response.meta['racecoursecode'],response.meta['racedistance']),
                response.meta['marginsbehindleader'][0], response.meta['runningposition'][0]),
            sirename=sirename,
            h_racedate=h_racedate,
            h_lbw = h_lbw,
            h_rp= h_rp1,
            h_place=h_place,
            h_racelink=h_racelink,
            h_rating=h_rating,
            h_distance=h_distance,
            h_raceclass=h_raceclass,
            h_rc_track_course= h_rc_track_course,
            h_rc = h_rc,
            h_surface = h_surface,
            h_course = h_course,
            h_ftime = h_ftime,
            h_avgspd= h_avgspd,
            h_winningspeeds=h_winningspeeds,
            h_winningratings=h_winningratings,
            h_avgwinninglbw =h_avgwinninglbw,
            ownername=ownername,
            dam=dam,
            damsire=damsire,
            corr_draw_place=corr_draw_place,
            corr_sp_place=corr_sp_place,
            corr_avgspd_place=corr_avgspd_place,
            h_avgspd_surface=h_avgspd_surface,
            dayssincelastrun= (response.meta['racedate']- h_racedate[0]).days
        )

    def parse_horse2(self, response):

        sirename = response.xpath('//th[text()="Sire"]/following-sibling::td/'
            'a/text()').extract()[0]
        race_rows_selector = response.xpath('(//tr[@class="even"] | //tr['
            '@class="even"]/preceding-sibling::tr[1])[position()<6]')
        racedate = []
        place = []
        final_sec_time = []
        for race_raw_sel in race_rows_selector:
            racedate.append(race_raw_sel.xpath('td[3]/text()').extract()[0])
            place.append(race_raw_sel.xpath('td[2]/text()').extract()[0])
            final_sec_time.append(race_raw_sel.xpath('td[17]/text()').extract()[0])

        ownername = response.xpath('//td[font[text()="Owner"]]/'
            'following-sibling::td/font/a/text()').extract()[0].strip()

        dam = response.xpath('//td[font[text()="Dam"]]/'
            'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

        damsire = response.xpath('//td[font[text()="Dam\'s Sire"]]/'
            'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

        yield items.HkjcHorseItem(
            racenumber=try_int(response.meta['racenumber']),
            raceindex=try_int(response.meta['raceindex']),
            racename=response.meta['racename'],
            raceclass=response.meta['raceclass'],
            racedistance=try_int(response.meta['racedistance']),
            racegoing=response.meta['racegoing'],
            racetrack=response.meta['racetrack'],
            horsecodelist=response.meta['horsecodelist'],
            racingincidentreport=response.meta['racingincidentreport'],
            horsenumber=try_int(response.meta['horsenumber']),
            horsename=response.meta['horsename'],
            horsecode=response.meta['horsecode'],
            position=processplace(response.meta['runningposition'][-1]),
            horsereport=getHorseReport(response.meta['racingincidentreport'],response.meta['horsename']),
            timelist=response.meta['timelist'],
            jockeyname=response.meta['jockeyname'],
            jockeycode=response.meta['jockeycode'],
            trainername=response.meta['trainername'],
            trainercode=response.meta['trainercode'],
            actualwt=try_int(response.meta['actualwt']),
            declarhorsewt=try_int(response.meta['declarhorsewt']),
            jockey2horsewt=round(response.meta['jockey2horsewt'],2),
            draw=try_int(response.meta['draw']),
            lbw=response.meta['lbw'],
            runningposition=map(int, response.meta['runningposition']),
            finishtime=get_scmp_ftime(response.meta['finishtime']),
            # winoddsrank=response.meta['winoddsrank'],
            marginsbehindleader=map(processmargins, response.meta['marginsbehindleader']),
            sirename=sirename,
            racedate=racedate,
            place=place,
            final_sec_time=final_sec_time,
            ownername=ownername,
            dam=dam,
            damsire=damsire,
        )
