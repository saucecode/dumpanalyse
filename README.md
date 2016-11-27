# dump analyse

Album analyser bot for [/r/wallpaperdump](https://reddit.com/r/wallpaperdump) posts. This is a WIP very light on features, and will run on both python 2 and 3.

### What Works

Here are some sample outputs so far.

`$ python dumpanalyse_bot.py https://imgur.com/gallery/dtjI3?lr=0`  
`521 Images / 7.87% 2160p, 33.78% 1440p, 54.32% 1080p, 4.03% 720p, 0.00% <720p / 85.80% Desktop, 1.54% Phone, 12.67% Square-ish`

`$ python dumpanalyse_bot.py https://imgur.com/gallery/EKecE`  
`20 Images / 0.00% 2160p, 0.00% 1440p, 20.00% 1080p, 20.00% 720p, 60.00% <720p / 90.00% Desktop, 5.00% Phone, 5.00% Square-ish`

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
