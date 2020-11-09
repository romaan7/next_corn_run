#!/bin/bash
[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"

timeformat='^([0-1][0-9]|[2][0-3]):([0-5][0-9])$'
if ! [[ $1 =~ $timeformat ]] ; then
	echo "error: Not a valid time" >&2; exit 1
else
	awk -v A="$1"  '$1 ~ /^([0-5][0-9]|*)+$/ && $2 ~ /^([0-1][0-9]|[2][0-3]|*|[0-9])$/ 
	function find_next_exec_time(hr,mn, a, b){
	begin_time = mktime(strftime("%Y %m %d " a" "b " " 00 , systime()))
	hr = 23
	mn =59
	hour = a
	minute = b
	
	if (hr != "*"){
		hour = hr
	if (hour != a)
		minute = 0 
		}
	
	if (mn != "*"){
		minute = mn
	if (hr == "*" && minute < b) 
		hour = (hr+1)%24
		}
	
   next_exec_time = mktime(strftime("%Y %m %d " hour" "minute" " 00 , systime()))
   if (next_exec_time > begin_time)
   return -1
   else if (next_exec_time = begin_time)
   return 0
   else if (next_exec_time < begin_time)
   return 1
}BEGIN{print $1 - "today" $3}' $input
fi