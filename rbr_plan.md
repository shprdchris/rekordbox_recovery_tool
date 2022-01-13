# RBR plan, new version

Chris Shepherd, Codethink ltd, 21-01-13

Useful python libraries:

* `os`: process file paths in whatever way is correct for the user's OS
* `ElementTree`: create and modify xml documents
* `wavinfo`: read .wav metadata (todo: likewise for mp3)

## Objective

* Recursively read a folder structure
* Replicate folder structure in xml
* For each leaf, add (track) files to xml with correct metadata
* Write the xml out in a manner that makes rekordbox happy

## Warmups

Recursively reading:

* ~~use `os` to read and repeat a subfolder structure (just folders)~~
* ~~check special characters are supported~~
* ~~also include all (for now) `.wav` files~~
* handle case of ~~empty root~~, nonexistent root
* test (inc. special cases)

Create an xml:

* create an empty rekordbox-friendly tree
* write the tree to xml
* manually create a folder, subfolder, playlist
* add tracks with names inc. special characters to playlist
* write to xml
* test

Combine previous:

* recursive function to:
  * read first entry of relative path
  * if relative path not in tree, add relative path to current node (root or otherwise)
  * if path contains no subfolders, add all (for now) .wav folders to tree, just store names for now
* test

Read audio metadata:

* open a .wav file
* use `wavinfo` to print metadata
* repeat for .mp3, .flac, (.aac) files
* test

Combine all above:

* where previously just adding names of .wav files, include in tree all relevant metadata
* test