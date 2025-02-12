# Setup

First of all, install Python. If you're on Windows, you can grab it [here](https://python.org/downloads). Make sure to check the little thing that says "Add to PATH" or something like that.

If you're on MacOS or Linux, you should install Python through your package manager (do NOT use the system Python!). For example, if you're on Debian/Ubuntu (or any other debian-based distro), you can just `sudo apt install python3.11` (or any other version that's available)

Then you need to install FFMpeg. If you're on Linux you should be able to just install it through your package manager. For Windows or MacOS, go [here](https://ffmpeg.org/download.html) and ignore the huge green button at the top. Go down to "More downloading options" and pick your OS from the giant colored icons. Pick the top link that shows up below them and download it. Then, extract the archive you got, and the files inside somewhere in your PATH (like `C:\Windows` if you're on Windows).

Now, you can either just download this repo as a zip, or git clone it. Whichever one you like. To download the repo as a zip, just click on the green button that says "Code", and click "Download ZIP". If you don't see it, make sure you're in "Local" and not "Codespaces" at the top.

Then, after that, open a shell (Command prompt or Terminal on Windows), navigate to the folder you put this repo in, and:

Windows: Run `pip install -r requirements.txt`

MacOS/Linux: Run `python3.11 -m pip install -r requirements.txt` (change `python3.11` to whatever version you installed, and once again, do NOT use the system Python)

# Run

If you're on Windows, you can just drag and drop your video file onto main.py!

If you don't wanna drag and drop, or you're on MacOS or Linux, then:

Windows: Run `py main.py video.mp4` (change `video.mp4` to the name of your video file)

MacOS/Linux: Run `python3.11 main.py video.mp4` (change `python3.11` to whatever version you installed and change `video.mp4` to the name of your video file)

When you run it, you should see a progress bar appear. Wait.

After the progress bar finishes, you should see a bunch of funky text in your terminal. Wait more.

After it all finishes, you should see some text saying "Press enter to exit.". This means it finished successfully, just press enter and it should close. Look for a file called `output.mp4`. That's your video. You're done.
