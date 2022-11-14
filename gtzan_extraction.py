##LIBRARIES
# import operating system libraries
import os
import sys

#import config file libraries
import configparser

#import audio libraries
import librosa as lr 
import resampy as rs

#import file directory management
import glob

#convert ndarray output from librosa to list format parsable by json
import numpy as np

#import JSON export
import json

#import audio playback
import simpleaudio as sa

#import realtime counter
import time

#import machine learning libraries (TO DO)

#import GUI libraries (TO DO)

#print successful startup
print('The program has started successfully.')

##CONFIG FILE
#config file location
config = configparser.ConfigParser()

#function to write config file
def write_config():
    config.write(open('config.ini', 'w'))

#create config if not present
if not os.path.exists('config.ini'):
    config["Sample Settings"] = {
        "Audio File Path" : "D:\Downloads",
        "Target Sample Rate" : "44100",
        "Stereo" : "False",
        "Audio Playback Length (seconds)" : "5"}
    #placeholder config["Feature Extraction Settings"] = {}
    config["Spectral Features"] = {
        "MFCCs" : "True",
        "Root-Mean-Square (RMS)" : "True",
        "Spectral Centroid" : "True",
        "Spectral Bandwidth" : "True",
        "Spectral Contrast" : "True",
        "Spectral Flatness" : "True",
        "Spectral Rolloff" : "True",
        "Poly Features" : "True",
        "Tonal Centroid Features" : "True",
        "Zero-Crossing Rate" : "True"}
    config["Beat Features"] = {
        "Beat Track" : "True",
        "Local Pulse Estimate" : "True",
        "Tempo Estimate" : "True"}
    #placeholder config["Percussive/Harmonic Split Settings"] = {}
    write_config()
    print('\nNo config file found; a default one has been created.')

#read config if present
else:
    config.read('config.ini')
    read_file = open("config.ini","r")
    content = read_file.read()
    print('\nConfiguration file found and its settings applied.')

##STATUS DISPLAYS
#fetch song file location
audio_file_path = config.get('Sample Settings', 'Audio File Path')
print('\nTarget Audio Path:\n    - %s' %audio_file_path)

#check if .wav convert to if not (TO DO)

#get list of all .wav files in list
song_input_list = glob.glob(pathname = ('%s/*.wav' %(audio_file_path)))

#get value for audio playback length
playback_length = config.getint('Sample Settings', 'Audio Playback Length (seconds)')

#determine length of song list
song_list_length = len(song_input_list)
print('        -', song_list_length, 'song(s) found to be loaded and analysed.')
print("            -", "\n            - ".join(song_input_list))

#define and display target data output location, set directory to match config, if this fails, default it to current working directory
if not os.path.exists('Exports'):
    os.makedirs('Exports')
export_file_path = 'Exports'

#sample rate target
sr_target = config.getint('Sample Settings', 'Target Sample Rate')
print('\nTarget Sample Rate set to: %i.' %sr_target)

#mono/stereo target
stereo_status = config.getboolean('Sample Settings', 'Stereo')
mono_status = not(stereo_status)

#display mono/stereo status
if(stereo_status > mono_status):
    print('Samples will be processed as: Stereo.')
else:
    print('Samples will be processed as: Mono.')

#display characteristics active for analysis
print('\nCharacteristics Active for Analysis:')

#create class for characteristics
class Characteristic:
    def __init__(self, status, configName):
        self.status = status
        self.configName = configName
        #print status of characteristic
        print('    -', self.configName, 'active: %s.' %self.status)

#create objects for each characteristic
mfcc = Characteristic(config.getboolean('Spectral Features', 'MFCCs'), 'Spectral Features')
rms = Characteristic(config.getboolean('Spectral Features', 'Root-Mean-Square (RMS)'), 'Root-Mean-Square (RMS)')
spectralCentroid = Characteristic(config.getboolean('Spectral Features', 'Spectral Centroid'), 'Spectral Centroid')
spectralBandwidth = Characteristic(config.getboolean('Spectral Features', 'Spectral Bandwidth'), 'Spectral Bandwidth')
spectralContrast = Characteristic(config.getboolean('Spectral Features', 'Spectral Contrast'), 'Spectral Contrast')
spectralFlatness = Characteristic(config.getboolean('Spectral Features', 'Spectral Flatness'), 'Spectral Flatness')
spectralRolloff = Characteristic(config.getboolean('Spectral Features', 'Spectral Rolloff'), 'Spectral Rolloff')
polyFeatures = Characteristic(config.getboolean('Spectral Features', 'Poly Features'), 'Poly Features')
tonalCentroid = Characteristic(config.getboolean('Spectral Features', 'Tonal Centroid Features'), 'Tonal Centroid Features')
zeroXingRate = Characteristic(config.getboolean('Spectral Features', 'Zero-Crossing Rate'), 'Zero-Crossing Rate')
beatTrack = Characteristic(config.getboolean('Beat Features', 'Beat Track'), 'Beat Track')
localPulse = Characteristic(config.getboolean('Beat Features', 'Local Pulse Estimate'), 'Local Pulse Estimate')
tempoEstimate = Characteristic(config.getboolean('Beat Features', 'Tempo Estimate'), 'Tempo Estimate')

#boolean variables to carry statuses (look for better way...)
mfcc_status_var = mfcc.status
rms_status_var = rms.status
spectralCentroid_status_var = spectralCentroid.status
spectralBandwidth_status_var = spectralBandwidth.status
spectralContrast_status_var = spectralContrast.status
spectralFlatness_status_var = spectralFlatness.status
spectralRolloff_status_var = spectralRolloff.status
polyFeatures_status_var = polyFeatures.status
tonalCentroid_status_var = tonalCentroid.status
zeroXingRate_status_var = zeroXingRate.status
beatTrack_status_var = beatTrack.status
localPulse_status_var = localPulse.status
tempoEstimate_status_var = tempoEstimate.status

beat_characteristics_active = True
if (not beatTrack_status_var) and (not localPulse_status_var) and (not tempoEstimate_status_var):
    beat_characteristics_active = False

#check parameters with user before running
print('\nCheck all settings seem correct before continuing.')
start_running_check = True
while start_running_check:
    while start_running_check:
        start_running = str(input('\nContinue (y/n)?: '))
        if start_running in ('y', 'n'):
            break
        print('Invalid input...')
    if start_running == 'y':
        start_running_check = False
    else:
        print('\nEnding program...\n')
        sys.exit()

#prettier console formatting
print('')

#create functions for extracting each characteristic (UNUSED)
def extract_mfcc():
    return lr.feature.mfcc(y = y, sr = sr)

def extract_rms():
    return lr.feature.rms(y = y)

def extract_spectralCentroid():
    return lr.feature.spectral_centroid(y = y, sr = sr)

def extract_spectralBandwidth():
    return lr.feature.spectral_bandwidth(y = y, sr = sr)

def extract_spectralContrast():
    return lr.feature.spectral_contrast(y = y, sr = sr)

def extract_spectralFlatness():
    return lr.feature.spectral_flatness(y = y)

def extract_spectralRolloff():
    return lr.feature.spectral_rolloff(y = y, sr = sr)

def extract_polyFeatures():
    return lr.feature.poly_features(y = y, sr = sr)

def extract_tonalCentroid():
    return lr.feature.tonnetz(y = y, sr = sr)

def extract_zeroXingRate():
    return lr.feature.zero_crossing_rate(y = y)

def extract_beatTrack():
    return lr.beat.beat_track(y = y, sr = sr, onset_envelope = onset_env)

def extract_localPulse():
    return lr.beat.plp(y = y, sr = sr, onset_envelope = onset_env)

def extract_tempoEstimate():
    return lr.beat.tempo(y = y, sr = sr, onset_envelope = onset_env)

#create song class
class Song:

#define class properties
    def __init__(
#basic properties
                self, 
                genre,
                fileName,
                audioLength,
                fileLocation,
#status of toggleable characteristics
                mfcc_status,
                rms_status,
                spectralCentroid_status,
                spectralBandwidth_status, 
                spectralContrast_status,
                spectralFlatness_status,
                spectralRolloff_status,
                polyFeatures_status,
                tonalCentroid_status,
                zeroXingRate_status,
#
                beatTrack_status,
                localPulse_status,
                tempoEstimate_status,
#toggleable characteristic properties which trigger based on config status
                mfcc,
                rms,
                spectralCentroid,
                spectralBandwidth,
                spectralContrast,
                spectralFlatness,
                spectralRolloff,
                polyFeatures,
                tonalCentroid,
                zeroXingRate,
#
                beatTrack,
                localPulse,
                tempoEstimate
                ):
#basic properties
        self.genre = genre
        self.fileName = fileName
        self.audioLength = audioLength
        self.fileLocation = fileLocation
#toggleable characteristic properties which trigger based on config status
        self.mfcc_status = mfcc_status_var
        self.rms_status = rms_status_var
        self.spectralCentroid_status = spectralCentroid_status_var
        self.spectralBandwidth_status = spectralBandwidth_status_var
        self.spectralContrast_status = spectralContrast_status_var
        self.spectralFlatness_status = spectralFlatness_status_var
        self.spectralRolloff_status = spectralRolloff_status_var
        self.polyFeatures_status= polyFeatures_status_var
        self.tonalCentroid_status = tonalCentroid_status_var
        self.zeroXingRate_status = zeroXingRate_status_var
#
        self.beatTrack_status = beatTrack_status_var
        self.localPulse_status = localPulse_status_var
        self.tempoEstimate_status = tempoEstimate_status_var
#toggleable characteristic properties which trigger based on config status
        self.mfcc = mfcc if mfcc_status_var else None
        self.rms = rms if rms_status_var else None
        self.spectralCentroid = spectralCentroid if spectralCentroid_status_var else None
        self.spectralBandwidth = spectralBandwidth if spectralBandwidth_status_var else None
        self.spectralContrast = spectralContrast if spectralContrast_status_var else None 
        self.spectralFlatness = spectralFlatness if spectralFlatness_status_var else None
        self.spectralRolloff = spectralRolloff if spectralRolloff_status_var else None
        self.polyFeatures = polyFeatures if polyFeatures_status_var else None
        self.tonalCentroid = tonalCentroid if tonalCentroid_status_var else None
        self.zeroXingRate = zeroXingRate if zeroXingRate_status_var else None
#
        self.beatTrack = beatTrack if beatTrack_status_var else None
        self.localPulse = localPulse if localPulse_status_var else None
        self.tempoEstimate = tempoEstimate if tempoEstimate_status_var else None

#counter for management of while loop 
song_list_length_counter = song_list_length
counter_secondary = 1

#get file directory location of song to be analysed
current_song_location = song_input_list[(song_list_length - counter_secondary)]

#create song analysis function
def song_analysis():
#remove most of directory and file type to simplify name of song
        current_song_filename_with_wav = current_song_location.removeprefix('%s\\' %audio_file_path)
        current_song_filename = current_song_filename_with_wav.removesuffix('.wav')

#load audio time series and sample rate from clip, converting to mono as defined in config
        if stereo_status:
            y, sr = lr.load(path = current_song_location, mono = False, duration = 30)
        else:
            y, sr = lr.load(path = current_song_location, mono = True, duration = 30)

#get song duration for display and set to 2 decimal places
        song_duration = lr.get_duration(y = y, sr = sr)
        song_duration_2dp = format(song_duration, ".2f")

#load status including duration
        if stereo_status:
            print('\nSong \'%s\' of (approximate) duration' %current_song_filename, song_duration_2dp, 'seconds has been loaded in stereo.')
        else:
            print('\nSong \'%s\' of (approximate) duration' %current_song_filename, song_duration_2dp, 'seconds has been loaded in mono.')

#process song to intended sample rate if required
        sample_rate_found = lr.get_samplerate(path = current_song_location)
        if sample_rate_found != sr_target:
            lr.resample(y, orig_sr = sr, target_sr = sr_target)
            print('\nAudio resampled from original', sample_rate_found, 'to match preferences in config (%d).' %sr_target)
        else:
            print('\nAudio sample rate already matches preferences in config (%d).' %sr_target)

#get onset strength for beat feature extraction
        if beat_characteristics_active:
            onset_env = lr.onset.onset_strength(y = y, sr = sr)
            print('\nAs one or more beat and rhythm type characteristic is being analysed, Beat Onset Strength Envelope has been determined.')

#placeholder for automatic genre checking, referral to manual input if none present
        current_song_genre = None
        genre_check = False
        if not(current_song_genre):
            genre_check = True
#genre check and playback of song to assist if requested by input prompt
        if genre_check:
            print('\nNo genre data was found for song \'%s\', so manual entry of genre will be required.' %current_song_filename)
            playback_check = True
            playback_status = str(input('\nPlay a %i second audio clip of song prior to this input (y/n)?: ' %playback_length))
            while playback_check:
                while playback_check:
                    if playback_status in ('y', 'n'):
                        break
                    print('Invalid input...')
                    playback_status = str(input('\nPlay a %i second audio clip of song prior to this input (y/n)?: ' %playback_length))
                if playback_status == 'y':
                    replay_check = True
                    wav_sample = sa.WaveObject.from_wave_file(current_song_location)
                    play_sample = wav_sample.play()
                    time.sleep(playback_length)
                    play_sample.stop()
                    while replay_check:
                        while replay_check:
                            replay_status = str(input('\nReplay song (y/n)?: '))
                            if replay_status in ('y', 'n'):
                                break
                            print('Invalid input...')
                        if replay_status == 'y':
                            print('\nReplaying song.')
                            replay_check = False
                            playback_status == 'y'
                            playback_check - False
                        else:
                            replay_check = False
                            playback_status == 'n'
                            playback_check = False
                else:
                    playback_check = False
#genre input
        current_song_genre = str(input('\nInput genre for song \'%s\' (in all lowercase): ' %current_song_filename))
         
#AUTO GENRE GET FOR GTZAN        
        before, sep, after = current_song_filename.partition('.')
        current_song_genre = before

#get tempo and beat tracking characterisitcs
        if beat_characteristics_active:
            if beatTrack_status_var:
                extracted_tempoEstimate, extracted_beatTrack = lr.beat.beat_track(onset_envelope = onset_env, y = y, sr = sr)
            elif tempoEstimate_status_var:
                extracted_tempoEstimate = lr.beat.tempo(onset_envelope = onset_env, y = y, sr = sr)

#create song object             
        song_object = Song(
                          current_song_genre, 
                          current_song_filename, 
                          ((lr.get_duration(y = y, sr = sr)) * sr_target),
                          current_song_location, 
                          mfcc_status_var, 
                          rms_status_var,
                          spectralCentroid_status_var,
                          spectralBandwidth_status_var,
                          spectralContrast_status_var,
                          spectralFlatness_status_var,
                          spectralRolloff_status_var,
                          polyFeatures_status_var,
                          tonalCentroid_status_var,
                          zeroXingRate_status_var,
                          #
                          beatTrack_status_var,
                          localPulse_status_var,
                          tempoEstimate_status_var,
                          #
                          #extract_mfcc(),
                          #extract_rms(),
                          #extract_spectralCentroid(),
                          #extract_spectralBandwidth(),
                          #extract_spectralContrast(),
                          #extract_spectralFlatness(),
                          #extract_spectralRolloff(),
                          #extract_polyFeatures(),
                          #extract_tonalCentroid(),
                          #extract_zeroXingRate(),
                          #extract_beatTrack(),
                          #extract_localPulse(),
                          #extract_tempoEstimate(),
                          ((lr.feature.mfcc(y = y, sr = sr)).tolist()) if mfcc_status_var else None,              
                          ((lr.feature.rms(y = y)).tolist()) if rms_status_var else None,                       
                          ((lr.feature.spectral_centroid(y = y, sr = sr)).tolist()) if spectralCentroid_status_var else None,                        
                          ((lr.feature.spectral_bandwidth(y = y, sr = sr)).tolist()) if spectralBandwidth_status_var else None,                       
                          ((lr.feature.spectral_contrast(y = y, sr = sr)).tolist()) if spectralContrast_status_var else None,                       
                          ((lr.feature.spectral_flatness(y = y)).tolist()) if spectralFlatness_status_var else None,                    
                          ((lr.feature.spectral_rolloff(y = y, sr = sr)).tolist()) if spectralRolloff_status_var else None,                   
                          ((lr.feature.poly_features(y = y, sr = sr, order = 0)).tolist()) if polyFeatures_status_var else None,                
                          ((lr.feature.tonnetz(y = y, sr = sr)).tolist()) if tonalCentroid_status_var else None,                       
                          ((lr.feature.zero_crossing_rate(y = y)).tolist()) if tempoEstimate_status_var else None,      
                          #     
                          (extracted_beatTrack.tolist()) if beatTrack_status_var else None,                       
                          ((lr.beat.plp(y = y, sr = sr, onset_envelope = onset_env)).tolist()) if localPulse_status_var else None,                      
                          extracted_tempoEstimate if tempoEstimate_status_var else None              
                          )

#make sure files are not overwritten if same name by giving them a new name        
        export_name_counter = 1
        staticish_song_filename = current_song_filename
        while os.path.exists(os.path.join(export_file_path, ('%s.json' %current_song_filename))):
            current_song_filename = ('%s_%i' %(staticish_song_filename, export_name_counter))
            export_name_counter += 1    
        with open(os.path.join(export_file_path, ('%s.json' %current_song_filename)), 'w') as f:
        #json.dump(data, f)
        #with open('%s.json' %current_song_filename, 'w') as f:
            json.dump(song_object.__dict__, f, ensure_ascii=False)
        print('\nSong \'%s\' has successfully finished characteristics extraction and been saved as \'%s.json\'.\n' %(staticish_song_filename, current_song_filename))

#determine how long to run loop, target song, etc. (including actually running analysis function)
while song_list_length_counter > 0:
    print('Now analysing song', (counter_secondary), 'of', song_list_length)
    song_analysis()
    song_list_length_counter -= 1
    counter_secondary += 1
    current_song_location = song_input_list[(song_list_length - counter_secondary)]

#print final status update
print('ALL SONGS HAVE SUCCESSFULLY COMPLETED CHARACTERISTIC EXTRACT.\nTHE DATA HAS BEEN EXPORTED TO THE \'Exports\' FOLDER.\n')



#remove non consistent parts (voting buckets)
#split harmonic and percussive sources
#add more controls for librosa parameters





