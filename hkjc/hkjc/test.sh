#!/bin/bash
VENV=/Users/vmac/Documents/PROGRAMMING/PY/scrapy/Chabrov/hkjcresults/hkjc/newscrapy1/bin
source ${VENV}/activate
cd "/Users/vmac/Documents/PROGRAMMING/PY/scrapy/Chabrov/hkjcresults/hkjc/hkjc"
printf '%s\n' "${PWD##*/}"
# A pretend Python dictionary with bash 3
# cd "/Users/vmac/Documents/PROGRAMMING/PY/scrapy/Chabrov/hkjcresults/hkjc"
# source newscrapy1/bin/activate

NOW=$(date +"%Y%m%d")

echo $NOW

old_IFS=$IFS      # save the field separator           
IFS=$'\n'     # new field separator, the end of line           
for line in $(cat meets.txt)
do
   echo "....FROM FILE"
   FILEDATE=${line%%:*}
   FILECODE=${line#*:}
   echo $FILECODE
   echo $FILEDATE
   ##run spider 
   # 20150909:HV has 9+11+9+12+11+12+11+12=87
   # scratched 1 
done          
IFS=$old_IFS     # restore default field separator 


# #2 days 
# nowplus2=$(date -v +2d +%d%m%Y)

# # unix_now=$(date -d "${NOW}" +"%s")

ARRAYNEW1516=(
	"20150906:ST"
	"20150909:HV"
	) 

SORTED=($(printf '%s\n' "${ARRAYNEW1516[@]}"|sort))
# #get todays meet code
for m in "${SORTED[@]}" ; do
	THEDATE=${m%%:*}
# 	# THEDIFF= "${NOW}"-"${THEDATE}"
	# echo $THEDATE
# 	# unix_todate=$(date -d "${THEDATE}" +"%s")
	##  historical results
	if [ "${THEDATE}" -le "${NOW}" ]; then
    	echo $THEDATE
		CODE=${m#*:}
		echo $CODE
		scrapy crawl hkjcsep2 -a date=$THEDATE -a racecoursecode=$CODE > batchimport.log
		sleep 5m
    fi
 	if [ "${THEDATE}" -eq "${NOW}" ]; then
    	echo $THEDATE
# 		CODE=${m#*:}
# 		echo $CODE
# 		scrapy crawl hkjcsep2 -a date=$THEDATE -a racecoursecode=$CODE > batchimport.log
    fi
#     # printf "%s likes to %s.\n" "$DATE" "$CODE"
done


# while read rdate code
# do
# # csv_array[$col2]=$col1
# aa[$rdate]=$code

# done < $INPUT_FILE

# echo "${!aa[*]}" 

# m[0]='test' || (echo 'Failure: arrays not supported in this version of bash.' && exit 2)

# m=(
# 	'15-03-2015 ST'
# 	'18-03-2015 HV'
#    )
# count=0
# while [ "x${m[count]}" != "x" ]
# do
#    count=$(( $count + 1 ))
# done

# today=$(date +"%d-%m-%Y")    	# The week of the year (0..53).
# today=${today#0}       	# Remove possible leading zero.
                                                                                
# let "index = $today"   # week modulo count = the lucky person

# email=${m[index]}     # Get the lucky person's e-mail address.
                                                                                
# echo $email     	# Output the person's e-mail address.



# homedir[ormaaj]=/home/ormaaj # Ordinary assignment adds another single element

# for user in "${!homedir[@]}"; do   # Enumerate all indices (user names)
#     printf 'Home directory of user %s is: %s\n' "$user" "${homedir[$user]}"
# done


# csv=( $(cat "$infile"))
# declare -A m
# m=( ["15-03-2015"]="ST" ["18-03-2015"]="HV")
# NOW=$(date +"%d-%m-%Y")

# echo "Current user is: $USER.  Full name: ${m[$USER]}."

# echo "${m["$NOW"]}"
# m=( $(cat "$infile"))
# l=("0")
# for element in $(seq $l $((  ${#m[@]} - 1)) )
# do
# 	echo "${m[$element]}"
# done
# $l = $l+1
# while IFS=, read -ra arr; do
#     ## Do something with $a, $b and $c
#     echo "${arr[0]:0}" #dates
# done < $infile

# OLDIFS="$IFS"

# # Create the CSV Array Hash keyed by Col #2
# while IFS="," read -r col1 col2
# do
#     csv_array[$col2]=$col1
# done <<EOD
# $csv
# EOD

# #For each key in Data Hash, print out corresponding keyed value in CSV Hash
# for key in "${!csv_array[@]}"
# do
#     echo "$key ${csv_array[$key]}"
# done
# IFS="$OLDIFS"
# eCollection=( $(cut -d ',' -f2 futuremeetings.csv ) )
# printf '%s\t%s' "${eCollection[0]}, ${eCollection[1]}"

# printf "http://bet.hkjc.com/racing/getXML.aspx?type=jcbwracing_winplaodds&date="+ ${eCollection[0]}+ "&venue=" + ${eCollection[1]} 

# VENUE = $("HV")
# cd "/Users/vmac/Documents/PROGRAMMING/PY/scrapy/NEWHKODDS/v3/HKOdds" && python ./HKOddsCollector.py -U "http://bet.hkjc.com/racing/getXML.aspx?type=jcbwracing_winplaodds&date=$NOW&venue=HV" > 2.log
# python ./HKOddsCollector.py -U "http://bet.hkjc.com/racing/getXML.aspx?type=jcbwracing_winplaodds&date=08-03-2015&venue=ST" > live.log
# python /Users/vmac/Documents/PROGRAMMING/PY/scrapy/NEWHKODDS/v3/HKOdds/HKOddsCollector.py -U "http://bet.hkjc.com/racing/getXML.aspx?type=jcbwracing_winplaodds&date=08-03-2015&venue=ST" > live.log
# python ./HKOddsCollector.py -U "http://bet.hkjc.com/racing/getXML.aspx?type=jcbwracing_winplaodds&date=04-03-2015&venue=HV" > 1.log

