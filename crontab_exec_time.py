#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""File name : corntab_exec_time.py
   Usage : python3 corntab_exec_time.py <start_time> < config
   
   Description : For each valid job entry in corntab finds the 
                 soonest  time  at which each of the  commands 
                 will fire and whether it is today or tomorrow.
                 
   Date : 01/11/2020
   
   Author : - ( Hidden for the anonymity)
   Platform : WSL 2 Ubuntu 20.04
   Revision : v 0.1

   
   Comments: Considering the simplicity of the task it would be 
   an overkill to use oop    classes here. And it would complicate 
   the logic unnecessarily. Initially I thought    of using awk and 
   bash for performing this since it would be native to Unix/Linux 
   environment and of course faster. But found python more forgiving 
   when dealing    with time format after a partial implementation 
   (See 'next_corn_run.sh' for a    partial implantation).
   
   Given more time I would have written a standard python unit test 
   class to test each    of the test cases and edge cases. But since 
   this task was completed in time, all    the test cases were validated 
   against entries in the config file.
   
   Also if this script is being used for monitering, it would be useful 
   to implement logging to track the executions.

"""

from datetime import datetime
import sys,re

#Finds the next run time given a start time and input hours and minutes in the unix corn table format.
#returns the next_exec_time as a datetime object
def find_next_exec_time(input_hour, input_minute, start_time):
    hour = start_time.hour
    minute = start_time.minute
    
    if input_hour != '*':
        hour = int(input_hour)
        minute = 0 if hour != start_time.hour else minute
        
    if input_minute != '*':
        minute = int(input_minute)
        
        if input_hour != '*' and minute < start_time.minute:
            hour = (hour+1)%24

    next_exec_time = datetime(start_time.year, start_time.month, start_time.day, hour, minute)
    return next_exec_time

#parses corntab file line to validate the minute hour command format.
#returns output with next run time as a string object. If invalid time return None.
def parse_input(line):
    try:
        min = line.split()[0]
        hr = line.split()[1]
        command = line.split()[2]
    
        minute_format = re.compile('^([0-5][0-9]|\*)+$')
        hour_format = re.compile('^([0-1][0-9]|[2][0-3]|\*|[0-9])$')
        now = datetime.now()
    
        if minute_format.match(min) and hour_format.match(hr):
            start_time = datetime(now.year, now.month, now.day,start_time_hr ,start_time_min)
            next_exec_time = find_next_exec_time(hr, min, start_time)
                 
            if next_exec_time < start_time:
                day = 'tomorrow'
            else:
                day = 'today'
                
            stdout = '{} {} - {}'.format(next_exec_time.strftime('%H:%M'),day,command)
            
            return stdout
    except IndexError:
        pass #can exit/break here for stopping if file is not correct
        print("Error : malformed line or config file is corrput")
        
        
if __name__ == "__main__":
    #match validate start_time argument 
    time_format = re.compile('^([0-1][0-9]|[2][0-3]):([0-5][0-9])$')
    
    try:
        if time_format.match(sys.argv[1]) and not sys.stdin.isatty():
            start_time_hr = int(sys.argv[1].split(":")[0])
            start_time_min = int(sys.argv[1].split(":")[1])
            for line in sys.stdin:
                output = parse_input(line)
                if output != None: #ignore invalid lines from file. .Can be changed to throw error
                    print(output)
        else:
            print("error: Not a valid time")
            exit(1)
    except IndexError:
        print("Usage : corntab_exec_time.py <start_time> < config")
        exit(1)