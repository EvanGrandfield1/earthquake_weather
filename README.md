Run with the following example command. 
The integer following the "n" argument can be between 2 and 50 officially, 
but any positive integer should likely work. Determines window for the 
sliding average of temperatures.

python main.py -n 2. 


Next steps:
Obviously, there were significant time constraints in my ability to do this exercise
compared to what I would have been able to do if this were something I was working
on full-time without a time constraint. Here are the things I would continue working 
on, listed from easiest to hardest, if I had more time. 

1. Only processing the most recent n events in the while loop. The current implementation
of the while loop reconstructs the entire pandas dataframe from scratch each time, versus 
just needing to process the last n events in order to print the most recent event and the 
n-window average. If n were arbitrarily large and the data were higher velocity, this 
would be a must. 

2. Creating a fake dataset in order to test better the contents of the while loop. I 
tested the while loop by making sure the code within it was used in the first step 
(getting all data from an hour ago til now) so that I wouldn't have to rely on 
different code that is hard to test. Because I don't have a fake dataset, I need 
to wait for a new earthquake to happen in order for the while loop to append
a new dictionary to the list of dicts that generates the pandas dataframe. If 
I had a test/fake dataset for this while loop, I would not have to worry about this
and could run tests more easily while not having to wait for realtime data. 

3. Code optimization. My current implementation needs to take a python list of 
dictionaries and generate a pandas dataframe every time the while loop finds a 
new earthquake. This takes a decent amount of time. It would make more sense 
to append the new row directly to the dataframe so we didn't have to do this generation
time and time again. 
