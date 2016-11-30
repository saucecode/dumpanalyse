from dumpanalyse import *
import praw, json, getpass

def generateComment(grades, ratios, count):
	percentages = {
		'2160p': grades['2160p']/count,
		'1440p': grades['1440p']/count,
		'1080p': grades['1080p']/count,
		'720p': grades['720p']/count,
		'small': grades['small']/count
	}
	
	running_percentage = 0.0
	inputs = []
	
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
	
	output = '''Quality | Percentage | Running Percentage | Count
---- | ---- | ---- | ----
2160p | %.2f%% | %.2f%% | %i
1440p | %.2f%% | %.2f%% | %i
1080p | %.2f%% | %.2f%% | %i
720p | %.2f%% | %.2f%% | %i
<720p | %.2f%% | %.2f%% | %i

Ratio | Percentage
---- | ----
Desktop | %.2f
Square | %.2f
Phone | %.2f

^(This is a test post for a future bot. Please ignore.)
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
	
	print(generateComment(*stringifyAlbumData(grabImgurAlbumData('http://imgur.com/gallery/QKa32'))))
