# Rekordbox Recovery Tool

Chris Shepherd, January 2022

## Introduction

This code can convert a tree-like structure of nested subfolders into a Rekordbox-readable .xml database, in a manner that preserves the subfolder structure.
This functionality isn't available in Rekordbox itself, where dragging and dropping causes the tree to become flattened into a single playlist.
With the RBR tool, organised DJs can avoid repeating the effort of organising their music folders inside Rekordbox.

## Running RBR tool

* Download the correct pre-build executable from the folder of this name
(NOTE: currently only compiled for Windows. The mac version is coming, please be patient)
* Run the executable and follow the instructions
* Open Rekordbox and select "preferences", "advanced settings".
* For the option "xml location", select the .xml file produced by RBR tool.
* Open the "view" option in the sidebar and enable the "xml database" option.
* Your RBR database will now be avaiable as a structure of playlists inside the appropriate folders.
Drag and drop into your collection for BPM analysis, exporting etc.

## Hacking on RBR tool

* Download this git project
* Create a virtual environment: `python3 -m venv .venv`
* Activate the virtual environment: `source .venv/bin/activate`
* Install the contents of `requirements.txt` (currently just the mutagen package) using pip.
* Create a new git branch.
* Make your changes and push to this repo, if you think your changes would be useful to others.
* Executables for *your* OS can be built using pyinstaller.
* Deactivate the virtual environment with the `deactivate` command.

## Logging isssues

Please log any issues in the boards of this project.