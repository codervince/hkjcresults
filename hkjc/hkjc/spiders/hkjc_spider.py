import re

import scrapy

from hkjc import items


class HorseSpider(scrapy.Spider):

    name = 'hkjc'

    def __init__(self, date, racecoursecode, *args, **kwargs):
        assert racecoursecode in ['ST', 'HV']
        super(HorseSpider, self).__init__(*args, **kwargs)
        self.domain = 'hkjc.com'
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

        racename = response.xpath('//div[@class="rowDiv15"]//table[@class='
            '"tableBorder0 font13"]//tr[2]/td[1]/text()').extract()

        raceclass__ = response.xpath('//td[@class="divWidth"]/text()').extract()[0]
        raceclass_ = re.match(r'^Class (?P<int>\d+) - $', raceclass__)
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
        horsecodelist = [re.match(r'^\((?P<str>.+)\)$', s).groupdict()['str']
            for s in horsecodelist_]

        racingincidentreport = response.xpath('//tr[td[contains(text(), '
            '"Racing Incident Report")]]/following-sibling::tr/td/text()'
            ).extract()[0]

        sectional_time_url = response.xpath('//div[@class="rowDiv15"]/div['
            '@class="rowDivRight"]/a/@href').extract()[0]
        request = scrapy.Request(sectional_time_url, callback=
            self.parse_sectional_time)
        meta_dict = {
            'racenumber': racenumber,
            'raceindex': raceindex,
            'racename': racename[0] if racename else None,
            'raceclass': raceclass,
            'racedistance': racedistance,
            'racegoing': racegoing,
            'racetrack': racetrack,
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

        try:
            winodds_float = float(winodds)
        except ValueError:
            winoddsrank = None
        else:
            winoddss = response.xpath('//table[@class="tableBorder trBgBlue '
                'tdAlignC number12 draggable"]//tr[@class="trBgGrey" or @class='
                '"trBgWhite"]/td[12]/text()').extract()
            winoddsranks = []
            for hc, wo in zip(response.meta['horsecodelist'], winoddss):
                try:
                    winoddsranks.append((hc, float(wo)))
                except ValueError:
                    pass
            winoddsranks.sort(key=lambda x: x[1])
            winoddsrank = winoddsranks.index((response.meta['horsecode'],
                winodds_float)) + 1

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
            winoddsrank=winoddsrank,
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
            'tr[@bgcolor][position()<6]')
        racedate = []
        place = []
        for race_raw_sel in race_rows_selector:
            racedate.append(race_raw_sel.xpath('td[3]/text()').extract()[0])
            place.append(race_raw_sel.xpath('td[2]//font/text()').extract()[0])

        ownername = response.xpath('//td[font[text()="Owner"]]/'
            'following-sibling::td/font/a/text()').extract()[0].strip()

        dam = response.xpath('//td[font[text()="Dam"]]/'
            'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

        damsire = response.xpath('//td[font[text()="Dam\'s Sire"]]/'
            'following-sibling::td/font/text()').extract()[0][1:].strip('\r\n ')

        yield items.HkjcHorseItem(
            racenumber=response.meta['racenumber'],
            raceindex=response.meta['raceindex'],
            racename=response.meta['racename'],
            raceclass=response.meta['raceclass'],
            racedistance=response.meta['racedistance'],
            racegoing=response.meta['racegoing'],
            racetrack=response.meta['racetrack'],
            horsecodelist=response.meta['horsecodelist'],
            racingincidentreport=response.meta['racingincidentreport'],
            horsenumber=response.meta['horsenumber'],
            horsename=response.meta['horsename'],
            horsecode=response.meta['horsecode'],
            timelist=response.meta['timelist'],
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
            winoddsrank=response.meta['winoddsrank'],
            marginsbehindleader=response.meta['marginsbehindleader'],
            sirename=sirename,
            racedate=racedate,
            place=place,
            ownername=ownername,
            dam=dam,
            damsire=damsire,
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
            racenumber=response.meta['racenumber'],
            raceindex=response.meta['raceindex'],
            racename=response.meta['racename'],
            raceclass=response.meta['raceclass'],
            racedistance=response.meta['racedistance'],
            racegoing=response.meta['racegoing'],
            racetrack=response.meta['racetrack'],
            horsecodelist=response.meta['horsecodelist'],
            racingincidentreport=response.meta['racingincidentreport'],
            horsenumber=response.meta['horsenumber'],
            horsename=response.meta['horsename'],
            horsecode=response.meta['horsecode'],
            timelist=response.meta['timelist'],
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
            winoddsrank=response.meta['winoddsrank'],
            marginsbehindleader=response.meta['marginsbehindleader'],
            sirename=sirename,
            racedate=racedate,
            place=place,
            final_sec_time=final_sec_time,
            ownername=ownername,
            dam=dam,
            damsire=damsire,
        )
