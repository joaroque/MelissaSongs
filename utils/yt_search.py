from youtubesearchpython import VideosSearch

def search(title):
	result = VideosSearch(title).result()
	if not result['result']:
		return (False, "not_found")

	link = result['result'][0]['link']
	title = result['result'][0]['title']
	result = result['result'][0]['duration'].split(':')
	
	min_duration = int(result[0])
	split_count = len(result)

	if not (min_duration) < 30 and split_count < 3:
		return (False, "too_long")

	else:
		return (True, link, title)

