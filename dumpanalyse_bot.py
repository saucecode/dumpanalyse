from dumpanalyse import *
import praw, json, getpass

def generateComment(grades, ratios, count):
	percentages = {
		'2160p': 100.0*grades['2160p']/count,
		'1440p': 100.0*grades['1440p']/count,
		'1080p': 100.0*grades['1080p']/count,
		'720p': 100.0*grades['720p']/count,
		'small': 100.0*grades['small']/count
	}
	
	running_percentage = 0.0
	inputs = []
	
	inputs.append(count)
	
	# first table
	for i in percentages:
		inputs.append(percentages[i])
		running_percentage += percentages[i]
		inputs.append(running_percentage)
		inputs.append(grades[i])
	
	# second table
	inputs.append(ratios['desktop'])
	inputs.append(ratios['square'])
	inputs.append(ratios['phone'])
	
	output = '''An image album analysis of %i images.

Quality | Percentage | Running Percentage | Count
---- | ---- | ---- | ----
2160p | %.1f%% | %.1f%% | %i
1440p | %.1f%% | %.1f%% | %i
1080p | %.1f%% | %.1f%% | %i
720p | %.1f%% | %.1f%% | %i
<720p | %.1f%% | %.1f%% | %i

Ratio | Percentage
---- | ----
Desktop | %.1f
Square | %.1f
Phone | %.1f

[^(I am a bot)](https://github.com/saucecode/dumpanalyse)^(, and this dump analysis was automatically generated.) [^(Bleep bloop)](https://www.reddit.com/message/compose/?to=wallpaper-cruncher)^.
''' % tuple(inputs)
	return output
	

if __name__ == '__main__':
	with open('configuration.json', 'rb') as f:
		data = json.load(f)
		reddit = praw.Reddit(
			user_agent='dumpanalyse by /u/saucecode',
		
			client_id=data['client_id'],
			client_secret=data['client_secret'],
		
			username=data['username'],
			password=getpass.getpass('enter password for %s: ' % data['username'])
		)
	
	print(generateComments(stringifyAlbumData(grabImgurAlbumData('http://imgur.com/gallery/QKa32'))))
