Program - 5
-------------


Consists Part 1 and 2.

Part1
-----

• A file named query_ideas.md of all the ideas possible

• A file named mongotest.py, sample pymongo program from class lectures.

• A file named pymongo_proof.png to prove mongo is working properly on my system.


Part 2
------
	Query 1: Find Interesting Features along some path:
	---------------------------------------------------
		•Select a starting point: X and a destination point Y. This can be done by mouse click, or by entering airport codes via sys.argv
		•sample query running format
			python query1.py DFW DOH 500
		•We can try all the possible combinatins of airports, whenever there is no possible airport within specified radius, the radius is changed to radius+100 for that point and then reverted back to radius specified while executing
		•All the airports are displayed as pins and the volcanos as red dots, earthquakes as blue dots and meteor as green dots.
		•The larger the radius the clearer is the ouput.
		
	
	Query 2: Nearest Neighbor:
	--------------------------
	•Click on the world map and get the nearest feature within XXX miles, possibly with specific feature values, further filtering the query (magnitude of earthquake, etc.) where features are listed below:
		Volcanos
		Earthquakes
		Meteors
	•sample query running format
		python query2.py [feature] [field] [field value] [min/max] [max results] [radius] [lon,lat]
			feature = volcano, earthquake, meteor
			field = some field in the 'properties' to compare against
			field_value = the value in wich to compare with
			min/max = whether we want all results greater than or less than the field_value.
			radius (in miles) = radius to apply our query with.
			lon,lat (optional) = Some point coords to act as a mouse click instead of actually clicking the screen.
			
		python query2.py r
			r=radius

	•Some examples
		python query2.py volcanos altitude 3000 min 3 1000
		python query2.py earthquakes magnitude 5 min 0 2000, 0 means all
		python query2.py 1000
	
	• If on a mosue click, if there are no volcanos or earthquakes or meteorites, it means on our filter cinditions there is nothing to display so please try at another point or chnage the filters in the command line
	
	Query 3: Clustering:
	--------------------
	• Use dbscan to find the top 3-5 clusters of volcanoes, earthquakes, and meteors.
	• sample query running format
		python query3.py [feature] [min_pts] [eps]
		Feature = (volcano, earthquake, meteor) and
		min_pts = minimum points to make a cluster, and
		eps is the distance parameter for dbscanpython 
	
		query3.py volcanos 5 3
		query3.py eartquakes 5 3
		query3.py meteorites 5 3
	• Volcanos as a feature run quickly as data is less, rest two take time.
	
	

