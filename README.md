# dump analyse

Album analyser bot for [/r/wallpaperdump](https://reddit.com/r/wallpaperdump) posts. This is a WIP very light on features, and will run on both python 2 and 3.

----

`dumpanalyse.py` contains the library code for looking into image albums hosted on various sites, and producing intelligible data.

`dumpanalyse_bot.py` contains the bot, which crawls /r/wallpaperdump for posts to critisize.

### Image Sizes

Images are graded with the following sizes, minus 100px off the shortest edge:

2160p (3840x2160)  
1440p (2560x1440)  
1080p (1920x1080)  
720p (1280x720)

Ratio is not considered when determining image grade - a phone wallpaper that is 1080x1920 will be graded as 1080p.

### Image Ratios

An image is considered a **Desktop** image if `width/height` is greater than 1.45.  
It is considered a **Phone** image if `height/width` is greater than 1.45.  
All other images are considered square.

4:3 and 5:4 images both qualify as square images.
