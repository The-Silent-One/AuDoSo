# AuDoSo: Convert Process & Play
Audiveris + Docker + Sonic-pi

AuDoSo is a self contained sheet music player. It takes a pdf file as input, converts it to musicxml file using Audiveris, process the file to simplify it then sends that data to Sonic-pi to play it.
The project uses a modified version of [weidi/audiveris-docker](https://github.com/weidi/audiveris-docker). It's a docker container for Audiveris

## Usage
-put music sheet files in pdf format in the ./input directory
-run the shell script

## Future Development
-feed data to Sonic-pi either in live mode or write a .rb file (or both)
-extend readme
