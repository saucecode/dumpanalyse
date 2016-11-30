from dumpanalyse import *
import praw, json, getpass, time

SUPPORTED_DOMAINS = {
	'imgur.com': grabImgurAlbumData
}

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
	inputs.append(100.0*ratios['desktop']/count)
	inputs.append(100.0*ratios['square']/count)
	inputs.append(100.0*ratios['phone']/count)
	
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
Desktop | %.1f%%
Square | %.1f%%
Phone | %.1f%%

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
	
	print 'starting bot...'
	wallpaperdump = reddit.subreddit('wallpaperdump')
	POSTS_I_COMMENTED_ON = []
	while 1:
		print 'loading new posts'
		new_submissions = wallpaperdump.new(limit=5)
		
		for submission in new_submissions:
			print '\n'
			print 'Looking at submission:',submission.id, submission.title
			print 'URL: ', submission.url
			
			if not submission.domain in SUPPORTED_DOMAINS:
				print 'Domain',submission.domain,'is not supported. Skipping...'
				continue
			
			if submission.id in POSTS_I_COMMENTED_ON:
				print 'I have already commented on this post.'
				continue
			
			if reddit.user.me().name in [i.author.name for i in submission.comments.list()]:
				POSTS_I_COMMENTED_ON.append(submission.id)
				print 'I have already commented on this post.'
				continue
			
			print 'generating comment for post', submission.id, submission.title
			
			# all checks passed - generate comment
			start = time.time()
			comment = generateComment( *stringifyAlbumData( SUPPORTED_DOMAINS[submission.domain](submission.url) ) )
			time_elapsed = time.time() - start
			print 'generated a comment - took',int(time_elapsed),'seconds - replying now...'
			submission.reply(comment)
			print 'comment submitted. sleeping 10 minutes'
			time.sleep(10*60 + 10)
			
		print 'sleeping for 10 minutes before refreshing'
		time.sleep(10)

