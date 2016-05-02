# WSM_Project
idiot Search Engine for DPLB DataBase


## Application method 

##### Inner Kerneal Part has two seperate parts, which are Crawler and InvertTableMaker.

1.Use the Crawler to catch the realted link url and xml file in two different txt file

2.Use the InvertTableMaker to read these two txt file and build invert index posting list and store it in redis DB
 
##### Outer Interface provide some function to fetch the data from redis DB

1.Use the RedisHandler Class to deal with the searching job




