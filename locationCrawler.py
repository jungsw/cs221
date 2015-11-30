import urllib2
import urllib
import json

# https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDX1GshmuCV3qfFCfoBqHTtVw4SFbLWT8w&address=04TH%20ST%20and%20PERRY%20ST%20in%20san%20francisco

# versiempre@gmail.com, hanklee514@gmail.com, jake, sw
apiKeyList = ['AIzaSyCO7AAKGTSz9p-ZfIvPeqyPDtMAQA27jZ0', 'AIzaSyDqDhnuWqA6KWy8-VM_tTByD4mgFWIP0pM', \
							'AIzaSyDX1GshmuCV3qfFCfoBqHTtVw4SFbLWT8w', 'AIzaSyCufQQEadq3JZOx5sXfwpfy4AUcR1AIXMM']
apiKey = apiKeyList[3]
baseUrl = 'https://maps.googleapis.com/maps/api/geocode/json'

inputFile = open('IntersectionsWithLatLng.csv', 'r')
startIndex = 7391


def crawl():
	outputFile = open('IntersectionsWithLatLng_v2.csv', 'w')
	# Prevent querying duplicate
	cache = {}
	def generateCacheKey(street1, street2):
		keyList = [street1, street2]
		keyList.sort()
		return ' '.join(keyList)


	for index, line in enumerate(inputFile.readlines()):
		if index >= startIndex and line[0]!='*' \
			and 'END,,,,END' not in line:

			streets = line.split(',')
			st1 = streets[1]
			st2 = streets[2].split('\\')[0]
			lat, lng, name = 0, 0, ''

			cKey = generateCacheKey(st1, st2)
			if cKey in cache:
				result = cache[cKey]
				lat, lng, name = result['lat'], result['lng'], result['name']
				print 'cache'
			else:
				query = {'address': '%s and %s in San Francisco' %(st1, st2), \
								 'key': apiKey }
				url = baseUrl + '?' + urllib.urlencode(query)
				print url

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

						print 'success'
		
			# For each line in output file, 
			# search success -> '* lat, long | formatted_address | original input'
			# failure -> 'original input'
			if lat > 0:
				line = '* %f, %f | %s | ' %(loc['lat'], loc['lng'], results['formatted_address']) + line
			else:
				print 'failure'

		outputFile.write(line)
	outputFile.close()


def getStat():
	succCount, failedCount = 0, 0
	for index, line in enumerate(inputFile.readlines()):
		if index > startIndex: break

		if line[0]=='*': succCount += 1
		else: failedCount += 1
	succRate = float(succCount) / float(succCount+failedCount)
	print 'Success - %d, Failed - %d, Rate - %f' %(succCount, failedCount, succRate)


# def validate():
	# check lat, lng range

###### Main ######
# crawl()
getStat()
	






