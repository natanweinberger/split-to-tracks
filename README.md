# split-to-tracks

A CLI tool to split a single MP3 track into multiple tracks, complete with title and track number metadata.

# Get started

1. Clone the repo

2. Build the Docker image

```bash
~ $ make build
```

3. Find an MP3 file that you want to split

```bash
~ $ ls -1 ~/Desktop
jungle-live-at-la-cigale.mp3
```

4. Create a text file that contains a track listing with titles and start times

```
# listings.txt
Intro 0:00
Platoon 1:35
Julia 6:46
Crumbler 11:11
The Heat 15:15
Smoking Pixels 19:45
Accelerate 22:36
Lemonade Lake 27:47
Son of a Gun 32:39
Lucky I Got What I Want 37:05
Drops 42:39
Busy Earnin 49:05
Time 56:54
```

5. Run `split_to_tracks`

```bash
~ $ ./split_to_tracks ~/Desktop/jungle-live-at-la-cigale.mp3 listings.txt
```

The output tracks will be in a directory in the same location as the MP3 file.

```bash
~ $ ls -1 ~/Desktop/jungle-live-at-la-cigale/
Accelerate.mp3
Busy Earnin.mp3
Crumbler.mp3
Drops.mp3
Intro.mp3
Julia.mp3
Lemonade Lake.mp3
Lucky I Got What I Want.mp3
Platoon.mp3
Smoking Pixels.mp3
Son of a Gun.mp3
The Heat.mp3
Time.mp3
```

(Optional) Add this repo to your `$PATH` to be ablt to run it from anywhere

```bash
PATH=$PATH:/path/to/split-to-tracks
```
