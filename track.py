# track.py
# Chris Shepherd, Codethink Ltd, 21-01-17
import mutagen
import pdb
import os
from datetime import date
import urllib.parse

# ------------------------------------------------------------------------------

# Read metadata of one audio file with supported CDJ formats (wav, .mp3, .flac, .aac)
class track:
    track_ID = 0

    # ------------------------------------------------------------------------------

    def __init__(self, track_path, track_name): #TODO is track_name superflous?
        track.track_ID += 1
        self.name = track_name
        self.mutagen_obj = mutagen.File(track_path)
        self.location = track_path
        # Extract the metadata
        self.metadata = {
            'TrackID' : track.track_ID,
            'Name' : track_name,
            'Kind' : '',
            'Size' : '',
            'Artist' : '',
            'TrackNumber': '',
            'Album' : '',
            'Composer' : '',
            'Comments': '',
            'Year' : '',
            'BitRate': '',
            'SampleRate': '',
            'TotalTime' : '',
            'DiscNumber' : '',
            'AverageBpm' : '',
            'DateAdded' : date.today(),
            'PlayCount' : '',
            'Rating' : '',
            'Location' : ''
        }
        # Shared metadata between all file types
        self.metadata['BitRate'] = self.mutagen_obj.info.bitrate
        self.metadata['SampleRate'] = self.mutagen_obj.info.sample_rate
        self.metadata['TotalTime'] = self.mutagen_obj.info.length
        self.metadata['Size'] = self.metadata['BitRate'] * self.metadata['SampleRate']
        self.metadata['Location'] = urllib.parse.quote(track_path.encode('utf8')).replace('%3A', ':').replace('%5C', '/')
        # Prefix required by Rekordbox, for some reason
        self.metadata['Location'] = 'file://localhost/'+self.metadata['Location']
        for item in self.metadata:
            self.metadata[item] = str(self.metadata[item])

    # ------------------------------------------------------------------------------

    def print_info(self):
        print(self.mutagen_obj.pprint())

    # ------------------------------------------------------------------------------

    def print_metadata(self):
        for element in self.metadata:
            print(element,": ",self.metadata[element])

# ------------------------------------------------------------------------------

# mp3: metadata in an ID3 key
class trackMp3(track):
    ID3_dict_keys = {
        'Name': 'TIT2',
        'Artist': 'TPE1',
        'TrackNumber': 'TRCK',
        'Composer': 'TPE2',
        'Comments': 'COMM::eng'
    }
    def set_ID3_element(self, dict_key):
        try: #TODO is there a safer way to handle the exceptions?
            self.metadata[dict_key] =  self.mutagen_obj[trackMp3.ID3_dict_keys[dict_key]].text[0]
        except:
            pass

    # ------------------------------------------------------------------------------

    def set_all_ID3(self):
        for key in self.ID3_dict_keys:
            self.set_ID3_element(key)

    # ------------------------------------------------------------------------------

    def __init__(self, track_path, track_name):
        track.__init__(self, track_path, track_name)
        self.metadata['Kind'] = "MP3 File"
        self.set_all_ID3()

# ------------------------------------------------------------------------------

# flac: metadata is in "flac tag", rather than ID3. Mutagen handles identically though.
class trackFlac(track):
    flac_dict_keys = {
        'Name': 'title',
        'Artist': 'ARTIST',
        'Year' : 'DATE',
        'Comments' : 'COMMENT',
        'Album': 'ALBUM',
        'TrackNumber' : 'TRACKNUMBER',
        'Composer' : 'ALBUMARTIST'
    }

    # ------------------------------------------------------------------------------

    def set_flac_element(self, dict_key):
        try:
            self.metadata[dict_key] =  self.mutagen_obj[trackFlac.flac_dict_keys[dict_key]][0]  # TODO why no 'text'?
        except:
            pass

    # ------------------------------------------------------------------------------

    def set_all_flac(self):
        for key in self.ID3_dict_keys:
            self.set_flac_element(key)

    # ------------------------------------------------------------------------------

    def __init__(self, track_path, track_name):
        track.__init__(self, track_path, track_name)
        self.metadata['Kind'] = "FLAC File"
        self.set_all_flac()
