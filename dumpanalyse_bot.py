from __future__ import print_function
import requests, os, time, json

'''
Image Grading
2160p (3840x2160)
1440p (2560x1440)
1080p (1920x1080)
720p (1280x720)

'''

# downloads data about an imgur album
def grabImgurAlbumData(url):
	if not ('://imgur.com/a/' in url or '://imgur.com/gallery/' in url):
		return False
	
	album_id = ''
	
	if '://imgur.com/gallery/' in url or '://imgur.com/a/' in url:
		album_id = url.split('/')[4].split('#')[0].split('?')[0]
	r = requests.get('http://imgur.com/a/%s/layout/blog' % (album_id,))
	
	if not r.status_code == 200: return False
	if not 'album_images":{"count":' in r.text: return False
	
	json_data = json.loads(r.text.split('album_images":')[1].split(',"place":')[0])

	return json_data

def stringifyAlbumData(data):
	grades = {'2160p':0.0, '1440p':0.0, '1080p':0.0, '720p':0.0, 'small':0.0}
	ratios = {'desktop':0.0, 'phone':0.0, 'square':0.0}
	count = data['count']
	for i in data['images']:
		if i['height'] >= 2160 - 100: grades['2160p'] += 1
		elif i['height'] >= 1440 - 100: grades['1440p'] += 1
		elif i['height'] >= 1080 - 100: grades['1080p'] += 1
		elif i['height'] >= 720: grades['720p'] += 1
		else: grades['small'] += 1
		
		ratio = i['width']/1.0/i['height']
		if ratio > 1.45: ratios['desktop'] += 1
		elif 1.0/ratio > 1.45: ratios['phone'] += 1
		else: ratios['square'] += 1
		
	return '%i Images / %.2f%% 2160p, %.2f%% 1440p, %.2f%% 1080p, %.2f%% 720p, %.2f%% <720p / %.2f%% Desktop, %.2f%% Phone, %.2f%% Square-ish' % (
		data['count'],
		100*grades['2160p']/count,
		100*grades['1440p']/count,
		100*grades['1080p']/count,
		100*grades['720p']/count,
		100*grades['small']/count,
		100*ratios['desktop']/count,
		100*ratios['phone']/count,
		100*ratios['square']/count,
		)

if __name__ == '__main__':
	data = grabImgurAlbumData('https://imgur.com/gallery/WqDEO')
	print(stringifyAlbumData(data))
	print('\n')
	data = grabImgurAlbumData('https://imgur.com/a/qqi1l')
	print(stringifyAlbumData(data))
	
	print('\n')
	data = grabImgurAlbumData('https://imgur.com/gallery/dtjI3?lr=0')
	print(stringifyAlbumData(data))
