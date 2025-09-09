# Download Videos from Graphy or Spayee
Requirements:
* ffmpeg
* openssl
* wget

## Step 1: Getting the video data

* Play the video you want to download
* Open Developer Tools (Ctrl+Shift+I in Chrome)
* Go to Network tab
* Now reload the browser
* Search for ".m3u8" : 

![image](https://user-images.githubusercontent.com/43024008/202852640-4b243437-bd41-4067-ab5c-7a709638a50e.png)
* Look for index.m3u8 or master.m3u8. Here I found index.m3u8, click on that: 

![image](https://user-images.githubusercontent.com/43024008/202852694-96ebcb15-22e9-44e5-9c5f-071197ce0a61.png)

* Go to Preview tab
* Copy the file name of resolution you want to download:

![image](https://user-images.githubusercontent.com/43024008/202852941-246a3870-87c0-4d0c-9263-b22804c87dd0.png)

* Search again by that file name:

![image](https://user-images.githubusercontent.com/43024008/202853018-6b11c536-6f59-4663-bb7e-b755c36e5dcc.png)

* Open that and go to headers tab then copy the request url:

![image](https://user-images.githubusercontent.com/43024008/202853060-50054d40-dba1-4ca1-88df-54f963c82127.png)

* Open it in a new tab and download the file.

_The file you have just downloaded, it has all of the .ts files. (Don't need to know what is .ts :^)_

_Those ts are encrypted. So you have to decrypt that. You need a key to decrypt that. You will get the key in the source code. Let's see.._

## Step 2: Getting the decryption key

* Go to the sources tab in the Developer Tools
* Look for 'cdn.jsdelivr.net' or '*.cloudfron.net/static/files': 

![image](https://user-images.githubusercontent.com/43024008/202853269-d51dbf4c-e73b-4b68-99d5-f558f92930a8.png)

* Expand that, expand npm, open the hls.js file
* Pretty print the file: 

![image](https://user-images.githubusercontent.com/43024008/202853323-de89fc83-ccf0-4e6a-a812-c14cad7fe141.png)

* Now search for 'this.decryptkey', and find the code like this then put a breakpoint at that line, after that pause the script:

![image](https://user-images.githubusercontent.com/43024008/202853438-407eba94-c24e-47c0-9fb9-444de04d752a.png)

* Reload the browser, now the browser might not finish the loading. Don't worry
* Go to console tab of the Developer tools, clear the console: 

![image](https://user-images.githubusercontent.com/43024008/202853559-52087dda-a96c-442e-b4e6-f13a6f49c41d.png)

* Paste this code and hit enter:

```js
Array.prototype.map.call(this.decryptkey, x => ('00' +
x.toString(16)).slice(-2)).join('')
```
_The output you will get is the key you need in order to decrypt the video files_

## Step 3: Downloading all of the .ts files

### Now you have to download all of the .ts files

* Open terminal (cmd for windows)
* Open the m3u8 file you downloaded
* Check the .ts files:

![image](https://user-images.githubusercontent.com/43024008/202854385-7ff441d2-b0c3-491a-a709-9a747a9f5fc6.png)

For me the m3u8 file link is - ```https://d2qny97nu4rj64.cloudfront.net/spees/w/o/62849985/v/6339af82c819310/u/636fd9da2ec532/t/99cc6d32e738/p/assets/videos/628222f8bf2b49985/2022/10/02/6339a819310/hls_500k_.m3u8```
Note: _Values have been changed for privacy_

* Remove the last parameter of the URL:
```https://d2qny97nu4rj64.cloudfront.net/spees/w/o/62849985/v/6339af82c819310/u/636fd9da2ec532/t/99cc6d32e738/p/assets/videos/628222f8bf2b49985/2022/10/02/6339a819310/```

* Add the first ts filename you found from m3u8 file and replace the text which changes at every ts with $i:
```https://d2qny97nu4rj64.cloudfront.net/spees/w/o/62849985/v/6339af82c819310/u/636fd9da2ec532/t/99cc6d32e738/p/assets/videos/628222f8bf2b49985/2022/10/02/6339a819310/hls_500k_$i.ts```

* Paste this to the terminal/cmd, replace <link> with the link you just made by adding .ts:
See how many ts do you have and replace the ```<limit_of_the_ts>``` with that value
```
for i in {1..<limit_of_the_ts>}; do wget "<link>" -O ->> "encrypted.ts"; done;
```
After editing hit enter. All of the ts will be downloaded now.

* Decrypt that ts to mp4 now:
```
sh
openssl enc -aes-128-cbc -nosalt -d -in encrypted.ts -K '<the_key_you_got_in_console>' -iv '<iv_in_m3u8_file_without_0x>' > decrypted.mp4
```
### Boom! You got the video but without audio. :)

* To get the audio do the same thing - 

First find the audio by searching

```https://d2qny97nu4rj64.cloudfront.net/spees/w/o/62849985/v/6339af82c819310/u/636fd9da2ec532/t/99cc6d32e738/p/assets/videos/628222f8bf2b49985/2022/10/02/6339a819310/hls_audio_0_$i.ts```

```
for i in {1..<limit_of_the_ts>}; do wget "<link>" -O ->> "encrypted.ts"; done;
```

```
sh
openssl enc -aes-128-cbc -nosalt -d -in encrypted.ts -K '<the_key_you_got_in_console>' -iv '<iv_in_m3u8_file_without_0x>' > audio.aac
```

# Step 4 : Finish the process

Combine the audio and the video

```
sh
ffmpeg -i video.mp4 -i audio.aac -c copy output.mp4
```


