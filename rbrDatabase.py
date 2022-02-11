# rbr_database.py
# Chris Shepherd, Codethink Ltd
# 21-01-14

import os
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

import track

# ------------------------------------------------------------------------------

# Store a collection of tracks and playlists


class rbrDatabase:
    def __init__(self):

        self.root = Element("DJ_PLAYLISTS")
        self.root.set("Version", "1.0.0")
        self.product_info = SubElement(self.root, "PRODUCT")
        self.product_info.set("Name", "rekordbox")
        self.product_info.set("Version", "5.8.6")
        self.product_info.set("Company", "Pioneer DJ")

        self.collection = SubElement(self.root, "COLLECTION")
        self.collection.set("Entries", "0")  # will need to change as finding new tracks

        self.playlists = SubElement(self.root, "PLAYLISTS")

        self.number_tracks = 0

        # Access nodes via their path: can access any parent nodes
        # if you know the child's path
        self.dict_paths_nodes = {}

    # ------------------------------------------------------------------------------

    def added_folder(self, parent, name, count):
        current_node = SubElement(parent, "NODE")
        current_node.set("Name", name)
        current_node.set("Type", "0")
        current_node.set("Count", count)
        current_node.set("KeyType", "0")
        return current_node

    # ------------------------------------------------------------------------------

    def added_playlist(self, parent, name, entries):
        current_node = SubElement(parent, "NODE")
        current_node.set("Name", name)
        current_node.set("Type", "1")
        current_node.set("Entries", entries)
        current_node.set("KeyType", "0")
        return current_node

    # ------------------------------------------------------------------------------

    def files_surviving(self, files):
        # TODO inefficient? duplicating list rather than removing a few elements.
        files_surviving = []
        for file in files:
            split_file = file.split(".")
            if len(split_file) > 1:
                extension = file.split(".")[len(split_file) - 1]
                allowed_extensions = ["mp3", "flac", "wav", "aac", "aiff"]
                if extension in allowed_extensions:
                    files_surviving.append(file)
        return files_surviving

    # ------------------------------------------------------------------------------

    def print_warning_message(self, specific_submessage, file_name):
        print(
            "WARNING: ",
            specific_submessage,
            " ",
            file_name,
            ", not supported by pre-2000 model CDJs",
        )

    # ------------------------------------------------------------------------------

    def added_track_id(
        self, abs_track_path, file_name, file_extension, show_warning_flags
    ):
        # Metadata is read in track class
        current_node = SubElement(self.collection, "TRACK")
        # .mp3, .flac, .wav have different metadata formats
        if file_extension == "flac":
            track_temp = track.trackFlac(abs_track_path, file_name)
            if show_warning_flags:
                # Old CDJs (e.g. 850, 900) can't play .flac files
                self.print_warning_message(".flac file", file_name)
        elif file_extension == "mp3":
            track_temp = track.trackMp3(abs_track_path, file_name)
        else:
            track_temp = track.track(abs_track_path, file_name)
            if file_extension == "wav":
                track_temp.metadata["Kind"] = "WAV File"
            elif file_extension == "aiff":
                track_temp.metadata["Kind"] = "AIFF File"
            elif file_extension == "aac":
                track_temp.metadata["Kind"] = "AAC File"
            else:
                print("found a non-track file (e.g. image): ", file_name)
        # Add the metadata
        current_node.set("TrackID", str(track_temp.track_ID))
        for metadata_item in track_temp.metadata:
            current_node.set(metadata_item, track_temp.metadata[metadata_item])
        # Old CDJs can't play high-bitrate .wav files
        try:
            if (int(track_temp.metadata["SampleRate"]) > 48000) and show_warning_flags:
                self.print_warning_message("sample rate exceeding 48 kHz", file_name)
        except Exception:
            print("ERROR: no sample rate found for file ", file_name)
        self.collection.set(
            "Entries", track_temp.metadata["TrackID"]
        )  # TODO inefficient to do every time
        # TODO inefficient to do every time
        return track_temp.track_ID

    # ------------------------------------------------------------------------------

    def add_recursively(self, root_dir, show_warning_flags):
        if not os.path.isdir(root_dir):
            print("ERROR: root doesn't exist. Try again.")
        else:
            root_dir = os.path.abspath(root_dir)
            for root, dirs, files in os.walk(root_dir):
                split_name = os.path.split(root)
                dict_key = split_name[0]
                node_name = split_name[1]
                if self.dict_paths_nodes == {}:
                    current_element = self.added_folder(
                        self.playlists, "ROOT", str(len(dirs))
                    )
                    self.dict_paths_nodes[root] = current_element
                elif dirs:
                    # Folder of playlists/folders
                    parent_element = self.dict_paths_nodes[dict_key]
                    current_element = self.added_folder(
                        parent_element, node_name, str(len(dirs))
                    )
                    self.dict_paths_nodes[root] = current_element
                elif not dirs:
                    # Playlist: add all tracks to collection and
                    # add their keys to the playlist node
                    parent_element = self.dict_paths_nodes[dict_key]
                    files = self.files_surviving(files)
                    current_element = self.added_playlist(
                        parent_element, node_name, str(len(files))
                    )
                    self.dict_paths_nodes[root] = current_element
                    # Add all audio files to collections
                    for file in files:
                        file_path = os.path.join(root, file)
                        split_file = file.split(".")
                        current_id = self.added_track_id(
                            file_path,
                            split_file[len(split_file) - 2],
                            split_file[len(split_file) - 1],
                            show_warning_flags,
                        )
                        current_track = SubElement(current_element, "TRACK")
                        current_track.set("Key", str(current_id))

    # ------------------------------------------------------------------------------

    # Return a pretty-printed XML string for the element
    def prettify(self, elem):
        rough_string = tostring(elem, "utf-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml()

    # ------------------------------------------------------------------------------

    # For debugging use
    def print_pretty(self):
        print(self.prettify(self.root))

    # ------------------------------------------------------------------------------

    def write_pretty(self, out_file_name):
        with open(out_file_name, "w", encoding="utf-8") as out_file:
            out_file.write(self.prettify(self.root))
