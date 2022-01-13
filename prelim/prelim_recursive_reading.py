# recursive_reading.py
# chris shepherd, codethink ltd
# use os module to recursively read/print a subfolder structure
# must take a route through subfolders that makes sense for creating new nodes of a tree

import os

root_dir = 'root_test'

# use os.walk, with topdown = true
# for each new node, for now just print a message
for root, dirs, files in os.walk(root_dir):
    print("currently at: ", root)
    if dirs:
        print("contains subfolders -> folder node. found subfolders: ",dirs)
    elif not dirs: # good place to creat playlist node
        print("no subfolders -> plalist node. found files: ", files)

print("done")