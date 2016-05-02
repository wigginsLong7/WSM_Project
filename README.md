# WSM_Project
idiot Search Engine for DPLB DataBase


## Application method 

##### Inner Kerneal Part has two seperate parts, which are Crawler and InvertTableMaker.

1.Use the Crawler to catch the realted link url and xml file in two different txt files

2.Use the InvertTableMaker to read these two txt files and build an invert-index-posting-list and store it in redis DB
 
##### Outer Interface provide some functions to fetch  data from redis DB

1.Use the RedisHandler Class to deal with the searching job




