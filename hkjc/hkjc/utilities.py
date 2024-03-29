#utiltiies
from fractions import Fraction
from datetime import date, time, datetime, timedelta
# from dateutil.relativedelta import relativedelta
import re
import operator
import math
import pprint
##SCMP

# def get_scmp_lbw(lbw):
#     '''

#     '''
#     if lbw is None or lbw == u'-':
#         return None




# def parse_mixed_fraction(s):
#     if s.isdigit():
#         return float(s)
#     elif len(s) == 1:
#         return unicodedata.numeric(s[-1])
#     else:
#         return float(s[:-1]) + unicodedata.numeric(s[-1])

# def sanitizelbw(lbw):
#     if "L" not in lbw:
#         '''suspect lbw'''
#         return None
#     lbw = lbw.replace("L", "")
#     return parse_mixed_fraction(lbw)

### RAILTYPE INFO


### DIFF DATE FORMATS HK
def getdateobject(date_str):
    #two variants on retired its %Y, on old its %y which is '15, on newform its '15 too
    #what kind of format?
    if u'/' not in date_str:
        return datetime.strptime(date_str, '%Y%m%d')
    if len(date_str) ==10:
        return datetime.strptime(date_str, '%d/%m/%Y')
    elif len(date_str) == 8:
        return datetime.strptime(date_str, '%d/%m/%y')
    else:
        raise ValueError


def getseasonstart(date_obj):
    season_start = date_obj - relativedelta(years=1,month=9, day=1) 
    return season_start

# def try_dateobj(date_obj):
#     try:
#         date_obj.year
#     except TypeError:
#         return None



def cleanstring(s):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, u' ',s).sub(u'-', u'')


def getsp(sp):
    try: 
        if sp != u'---':
            return sp
    except TypeError:
        # return try_float(sp)
        return None

def getactualwt(awt):
    try: 
        if awt != u'---':
            return try_int(awt)
    except TypeError:
        # return try_float(sp)
        return None

## for comparing with historical data
## ST / "AWT" / "-"
def getrc_track_course(racecourse, surface):
    rc_code = getrc(racecourse)
    surface = unicode.strip(surface)
    surface_course_codes = {
    u'"A" Course': ("Turf", "A"),
    u'"A+3" Course': ("Turf", "A+3"),   
    u'"B" Course': ("Turf", "B"),
    u'"B+2" Course': ("Turf", "B+2"),
    u'"C" Course': ("Turf", "C"), 
    u'"C+3" Course': ("Turf", "C+3"),
    u'All Weather Track': ("AWT", "-")
    }
    spacer = u' / '
    newsurface, newcourse = surface_course_codes[surface]
    return rc_code+spacer+newsurface+spacer+newcourse
    # add u' / '

def getinternalraceindex(racedate, racecoursecode, racenumber):
    if type(racedate) != type(datetime(2015, 5, 31, 0, 0)):
        return None
    return racedate.strftime('%Y%m%d') + '_' + str(racecoursecode) + '_' + str(racenumber)


def average(s): return sum(s) * 1.0 / len(s)


def getbestfinishstats(besttimes):
    #make sure best finishes is a list
    ##init dictionary keys
    stats = {}
    stats['standard-deviation'] = None
    stats['variance'] = None
    stats['avg'] = None
    if type(besttimes) != type([]):
        return None
    if len(besttimes) == 0:
        return None
    thesum = reduce(operator.add, map(float,besttimes))
    stats['avg'] = round(thesum*1.0/len(besttimes),2)
    # stats['maxdistance'] = max(map(float, besttimes))
    stats['variance'] = map(lambda x: (float(x) - stats['avg'])**2, besttimes)
    stats['standard-deviation'] = round(math.sqrt(sum(stats['variance'])*1.0/len(stats['variance'])),2)
    return stats

def cleanpm(prizemoney):
    return int(''.join(re.findall("[-+]?\d+[\.]?\d*", prizemoney)))/1000.0


'''
expect format datetime object + time 1:45 12 hour clock
convert to UTC time object -8
need to explicity state timezone in datetime object?
'''
def local2utc(todaysdate, basictime):
    h = int(basictime.split(':')[0])
    h = h+12 if h < 12 else h
    m = int(basictime.split(':')[1])
    hk_t = time(h,m)
    hk_d = datetime.combine(todaysdate, hk_t) ##todaysdate is a date object
    return hk_d - timedelta(hours=8) 

def getrc(racecourse):
    racecourse = unicode.strip(racecourse)
    if racecourse == 'Sha Tin' or racecourse == 'ST':
        return u'ST'
    elif racecourse =='Happy Valley' or racecourse== 'HV':
        return 'HV'
    else:
        return None

DISTANCESTOTURNS_HV = {


u'1650': [310,650,1150,1280],

}


DISTANCETOSECS  = {
    
u'1650': [450,400,400],



}

def issprint(racecoursecode, distance):
    return racecoursecode== u'ST' and distance==1000

def getearlypacepoints(isstraight, mbl1, pos1):
    pts = 0
    try:
        mbl1 = horselengthprocessor(mbl1)
        pos1 = int(pos1)
        if isstraight:
            threshold = 2.75
        else:
            threshold = 3.5
        if mbl1 <= threshold:
            pts=pts+1
        if pos1 in [1,2,3]:
            pts=pts+1
    except:
        pass
    return pts


RAILTYPES = {
    
u'ST': {
    u'A': [430, 30.5],
    u'A+2': [430, 28.5],
    u'A+3': [430, 27.5],
    u'B': [430,26],
    u'B+2': [430, 24],
    u'C': [430, 21.3],
    u'C+3': [430, 18.3],
    u'AWT': [365, 22.8]
},

u'HV': {
    u'A': [312, 30.5],
    u'A+2': [310, 8.5],
    u'B': [338, 26.5],
    u'B+2': [338, 24.5],
    u'B+3': [338, 23.5],
    u'C': [334, 22.5],
    u'C+3': [335, 19.5]
}

}

def split_by(tosplit, separator):
    rtn = []
    if tosplit is not None:
        for i in tosplit:
            rtn.append(unicode.split(i, u'\xa0'))
        return rtn

def gethomestraight(racecourse, railtype):
    if racecourse == u'Sha Tin':
        racecourse = u'ST'
    if racecourse == u'Happy Valley':
        racecourse = u'HV'
    if railtype == u"All Weather Track":
        railtype = u"AWT"
    return RAILTYPES[racecourse][railtype][0]

def gettrackwidth(racecourse, railtype):
    if racecourse == u'Sha Tin':
        racecourse = u'ST'
    if racecourse == u'Happy Valley':
        racecourse = u'HV'
    if railtype == u"All Weather Track":
        railtype = u"AWT"
    return RAILTYPES[racecourse][railtype][1]



def to_eventinfo(racecourse, surface, going, railtype):
    rtn = u''
    if racecourse in [u'Sha Tin', u'ST']:
        rtn += u'ST '
        if surface == 'AWT':
            rtn += u'aw '
    else:
        rtn += u'HV tf '
    #going
    rtn += u'-' + raitype + u' '
    return rtn


def from_eventinfo(eventinfo):
    '''
    splits e.g. ST tf g/f -C 
    into list of 
    racecourse surface going railtype
    '''
    rtn = {}
    rtn['surface'] = 'Turf'
    rtn['railtype'] = None
    goings = [u'g', u'g/f', u'f', u'w/s']
    if eventinfo is None:
        return []
    rc = re.findall("^(ST|HV)\s.*", eventinfo)
    if rc:
        rtn['racecourse'] = rc[0]
    tf_aw = re.findall(".*\s(tf|aw)\s.*", eventinfo)
    if tf_aw == 'aw':
        rtn['surface']= u'AWT'
    rt = re.findall(".*-(.*)$", eventinfo)
    if rt:
        if unicode.strip(rt[0]) == u'All Weather Track':
            rtn['railtype'] = None
        else: 
            rtn['railtype'] = unicode.strip(rt[0])
    return rtn
    ##return racecourse, surface, going, railtype
    
def getsplits(distance, timelist):
    ct = [float(i) for i in timelist if i is not None]
    splits = {}
    if distance is None:
        return None 
    if int(distance) in [1200,1600,2000]:
        #1600, 1200, 2000,2400 1sec = 400
        splits['0-400m'] = round(float(400)/float(ct[0]),3)
        splits['0-800m'] = round(float(800)/float(ct[0]+ct[1]),3)
        splits['last400m'] = round(float(400)/float(ct[-1]),3)
        splits['last800m'] = round(float(400)/float(ct[-2]+ct[-1]),3)
    if int(distance) in [1000,1400,1800,2200]:
        splits['0-200m'] = round(float(200)/float(ct[0]),3)
        splits['0-600m'] = round(float(600)/float(ct[0]+ct[1]),3)
        splits['last400m'] = round(float(400)/float(ct[-1]),3)
        splits['last800m'] = round(float(400)/float(ct[-2]+ct[-1]),3)
    if int(distance) in [1100,1500,1900]:
        splits['0-300m'] = round(float(300)/float(ct[0]),3)
        splits['0-700m'] = round(float(700)/float(ct[0]+ct[1]),3)
        splits['last400m'] = round(float(400)/float(ct[-1]),3)
        splits['last800m'] = round(float(400)/float(ct[-2]+ct[-1]),3)
    if int(distance) in [1650]:
        splits['0-350m'] = round(float(350)/float(ct[0]),3)
        splits['0-750m'] = round(float(750)/float(ct[0]+ct[1]),3)
        splits['last400m'] = round(float(400)/float(ct[-1]),3)
        splits['last800m'] = round(float(400)/float(ct[-2]+ct[-1]),3)
    # splits['zero2finish'] = None
    splits['zero2finish'] = round(float(distance)/sum(map(float,ct)),3) #d/t
    # if distance == 1600:
    #     d1 = 200
    #     splits['firstsec'] = round(float(d1)/float(ct[0]),3)
    # if distance in [1000,1400,1800,2200]:
    #     d1 = 200
    # if distance ==1600:
    #     d1 = 400
    # if distance in [1100,1500,1900]:
    #     d1 = 300
    # if distance in [1650]:
    #     d1 = 350
    # if d1 is not None:
    #     splits['firstsec'] = round(float(d1)/float(ct[0]),3) 
    return splits

#ft2time(response.meta['finishtime'])
def getodds(odds):
    if odds == u'---':
        return None
    else:
        return try_float(odds)

def getlbw(lbw):
    if lbw == u'-':
        return None
    else:
        return horselengthprocessor(lbw)

def getdraw(draw):
    if draw == u'--':
        return None
    else:
        return try_int(draw)

def valueordash(value):
    if value == u'--':
        return None
    else:
        return try_int(value)

def ft2time(finishtime):
    #format u'1.40.18'
    pass

'''
expecting format ss.mm
'''
def get_sec_in_secs(s):
    if s == u'--' or s == u'' or s is None:
        return None
    l = s.split('.') #array min, secs, milli - we want seconds
    # l[0]*60 + l[1] + l[2]/60.0
    return float(l[0]) +(float(l[1])*0.01)

def get_sec(s):
    if s == u'--':
        return None
    l = s.split('.') #array min, secs, milli - we want seconds
    # l[0]*60 + l[1] + l[2]/60.0
    return float(l[0])*60 + float(l[1]) + (float(l[2])*0.01)

def removeunicode(value):
    return value.encode('ascii', 'ignore')


def get_hkjc_ftime(ftime):
    '''
    strftime('%s')
    expected format:1:40.7 m:ss.n
    '''
    if ftime is None or ftime == u'--' or ftime == u'' or ftime == u'---':
        return None
    else:    
        ftr = [60,1,0.1]
        return round(sum([a*b for a,b in zip(ftr, map(int,ftime.split('.')))]),3)
   

def get_scmp_ftime(ftime, myformat=None):
    '''
    strftime('%s')
    expected format:1:40.7 m:ss.n
    if format =='s' return no of seconds else datetiem obj
    '''
    if ftime is None:
        return None
    dt1_obj = datetime.strptime(ftime, "%M:%S.%f")
    if dt1_obj is not None:
        totalsecs = (dt1_obj.minute*60.0) + dt1_obj.second + (dt1_obj.microsecond/1000.0)
    if myformat == u's':
        return totalsecs
    else:
        return dt1_obj

def processscmpodds(odds):
    if odds is None:
        return None
    else:
        return try_float(odds)

def isFavorite(oddscolor):
    if oddscolor is None:
        return 0
    elif oddscolor == '#FF0000':
        return bool(1)
    else:
        return bool(0)




##########
def get_rp_array(rpstr):
    # \xa0
    rpstr = unicode.strip(rpstr)
    rpstr= rpstr.replace(u'\xa0\xa0', u'-')
    return [try_int(i) for i in rpstr]
def get_rp(rpstr):
    # \xa0
    rpstr = unicode.strip(rpstr)
    return rpstr.replace(u'\xa0\xa0', u'-')

def processscmpplace(place):
    place99 = ['DISQ', 'DNF', 'FE', 'PU', 'TNP', 'UR', 'VOID', 'WD', 'WR', 'WV', 'WV-A', 'WX', 'WX-A']
    if place is None:
        return None
    elif place in place99:
        return 99
# r_dh = r'.*[0-9].*DH$'
    else:
        return try_int(place)



def timeprocessor(value):
    #tries for each possible format
    for format in ("%S.%f", "%M.%S.%f", "%S"):
        try:
            return datetime.strptime(value, format).time()
        except:
            pass
    return None

#dead heats FIX!
def processplace(place):
    # r_dh = r'.*[0-9].*DH$'
    if isinstance(place, int):
        return place
    else:
        place = unicode.strip(place)
        if place is None:
            return None
        if place == 'Pla.':
            return None
        if "DH" in place:
            return int(place.replace("DH", ''))
        else:
            if place in [u'WV', u'WV-A', u'WX-A', u'UV', u'DISQ', u'FE', u'DNF', u'PU', u'TNP', u'UR', u'WX']:
                return 99
            else:
                return int(place)


def didnotrun(value):
    if "---" in value:
        return None


# def processmargins(margin):
#     if margin is None:
#         return None
#     if u'-' in margin:
#         #mixed fraction
#         a = float(margin.split('-')[0])
#         f = float(Fraction(margin.split('-')[1]))
#     return a+f

# 'marginsbehindleader': [u'3/4', u'1-3/4', u'1-1/4', u'1', None, None]



def horselengthprocessor(value):
    from fractions import Fraction
    #covers '' and '-'
    if value is None:
        return None
    if type(value) == type([]):
            value = u''.join(value)
    value = unicode.strip(value)
    if '---' in value or '--' in value or value == u'':
        return None
    if value == '-':
        #winner
        return 0.0
    if "-" in value and len(value) > 1:
        return float(Fraction(value.split('-')[0]) + Fraction(value.split('-')[1]))
    if value == u'N':
        return 0.3
    if value == u'SH':
        return 0.1
    if value == u'HD':
        return 0.2
    if value == u'SN':
        return 0.25
    ## tailed off
    if value == u'TO':
        return 10.0 
    #nose?           
    if value == 'NOSE':
        return 0.05
    if "/" in value and "-" not in value:
         return float(Fraction(value))
    return float(Fraction(value))

def try_float(value):
    try:
        return float(value)
    except:
        return 0.0

def try_int(value):
    try:
        return int(value)
    except:
        return 0

def getHorseReport(ir, h):
    lir = ir.split('.')
    # HELEN\u2019S CHOICE
    if "'" in h:
        _h = h.split("'")
        newh = _h[0]+u"\u2019"+_h[1]
        rtn = [e.replace(".\\n", "...") for e in lir if h in e or newh in e]
    else:
        rtn = [e.replace(".\\n", "...") for e in lir if h in e]
    return u''.join([i.replace('\r', '').replace('\n', '-').replace(u'  ', ' ').replace(u'-',u'').replace(u'\u2019', u'`') for i in rtn])

#done in default output processor?
def noentryprocessor(value):
    return None if value == '' else value


'''
renvove u'\r\n\t4      \r\n\t
remove \r\n\t\t\t\t\t
what about \u2019S ? '
'''
def cleanstring(value):
    return unicode.strip(value)
