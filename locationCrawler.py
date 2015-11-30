import urllib2
import urllib
import json

# https://maps.googleapis.com/maps/api/geocode/json?address=04TH%20ST%20and%20PERRY%20ST%20in%20san%20francisco
apiKey = 'AIzaSyCO7AAKGTSz9p-ZfIvPeqyPDtMAQA27jZ0'
baseUrl = 'https://maps.googleapis.com/maps/api/geocode/json'

# inputFile = open('List_of_Intersections_only.csv', 'r')
inputFile = open('sample_data.csv', 'r')
outputFile = open('sample_output.csv', 'w')

# key: set([street1, street2]), value: {lat, lng, name}
cache = {}

def generateCacheKey(street1, street2):
	keyList = [street1, street2]
	keyList.sort()
	return ' '.join(keyList)

succCount, cacheCount, failedCount = 0,0,0

for line in inputFile.readlines():
	streets = line.split(',')
	lat, lng, name = 0, 0, ''

	cKey = generateCacheKey(streets[1], streets[2])
	if cKey in cache:
		result = cache[cKey]
		lat, lng, name = result['lat'], result['lng'], result['name']
		cacheCount += 1
		print 'cache'
	else:
		query = {'address': '%s and %s in San Francisco' %(streets[1], streets[2]), \
						 'key': apiKey }
		url = baseUrl + '?' + urllib.urlencode(query)

		try:
			response = urllib2.urlopen(url)
		except urllib2.HTTPError, err:
			print 'Http error %s: %s' %(err.code, err.read())
		except urllib2.URLError, err:
			print 'Url error %s: %s' %(err.code, err.read())
		else:
			results = json.load(response)['results'][0]
			if results['types'][0]=='intersection':
				loc = results['geometry']['location']
				lat, lng, name = loc['lat'], loc['lng'], results['formatted_address']
				cache[cKey] = {'lat': lat, 'lng': lng, 'name': name}
				 
				succCount += 1
				print 'success'
	
	# For each line in output file, 
	# search success -> '* lat, long | formatted_address | original input'
	# failure -> 'original input'
	if lat > 0:
		line = '* %f, %f | %s | ' %(loc['lat'], loc['lng'], results['formatted_address']) + line
	else:
		failedCount += 1
		print 'failure'

	outputFile.write(line)

print 'Complete with result: succ - %d, cache - %d, failure - %d, total - %d' \
			%(succCount, cacheCount, failedCount, succCount+cacheCount+failedCount)
outputFile.close()



	






