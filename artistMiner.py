import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import pprint
import string
import smtplib
from email.parser import Parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




def getAlbums(artistID,spotipyInstance):
    albumTypeList = ['album','single','appears_on','compilation']
    albumList = list()

    for albumType in albumTypeList:
        results = spotipyInstance.artist_albums(artistID,album_type=albumType)
        albums = results['items']
        while results['next']:
            results = spotipyInstance.next(results)
            albums.extend(results['items'])
        for album in albums:
            albumList.append(album)

    return albumList


def getTracks(albumID,spotipyInstance):
    trackList = list()

    results = spotipyInstance.album_tracks(albumID)
    tracks = results['items']
    while results['next']:
        results = spotipyInstance.next(results)
        tracks.extend(results['items'])

    for track in tracks:
        trackList.append(track)

    return trackList

def collabFinder(artistName,spotipyInstance,allRappers):
    results = sp.search(q=artistName,type='artist')
    artistID = results['artists']['items'][0]['uri'].split(':')[2]
    collaborators = list()

    print 'Mining arist: ',artistName,'\tid:\t',artistID
    albums = getAlbums(artistID,spotipyInstance)
    for album in albums:
        tracks = getTracks(album['id'],spotipyInstance)

        for track in tracks:
            artists = track['artists']
            if artistName in artists or artistName in track['name']:
                #print 'artist is on THIS track!'
                #print 'track: ',track['name']
                #print 'artists: ',artists
                for artist in artists:
                    for rapperName in allRappers:
                        if artist['name'] in rapperName and artist['name'] != artistName:
                            collaborators.append(artist['name'].encode('utf-8'))
                            #print artist['name'].encode('utf-8')

                if 'feat' in track['name']:
                    for rapperName in allRappers:
                        if rapperName in track['name'] and rapperName != artistName:
                            #print rapperName
                            collaborators.append(rapperName)

    collaborators = list(set(collaborators))
    return collaborators




client_credentials_manager = SpotifyClientCredentials(client_id='b522ba0a33df4fe5b09357c42a7edda9', client_secret='cf073ed6ddb043dda91c74e5773a3c3d')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


allRappers = list()
rapperListFile = open('rapperList','r')
for rapper in rapperListFile:
    allRappers.append(rapper[:-1])
rapperListFile.close()


#print collabFinder('Higher Brothers',sp,allRappers)
edgeList = list()
errorList= list()

collabFile = open('edge_list','w')
errorFile = open('error_list','w')

for rapper in allRappers:
    try:
        collabs = collabFinder(rapper,sp,allRappers)
        for entry in collabs:
            edgeList.append(str(rapper + ',' + entry + '\n'))
    except Exception, e:
        errorList.append(str(rapper+'\n'))
        continue

collabFile.writelines(edgeList)
collabFile.close()

errorFile.writelines(errorList)
errorFile.close()

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Ding!'
msg['From'] = 'adamsocialnetworkproject@gmail.com'
msg['To'] = 'amontano495@gmail.com'
body = 'The mining has completed!'
msg.attach(MIMEText(body,'plain'))

s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.login('adamsocialnetworkproject@gmail.com','goRY72QcsDZE')
s.sendmail('adamsocialnetworkproject@gmail.com', ['amontano495@gmail.com'], msg.as_string())
s.quit()

'''
def collabFinder(artistName):
    allArtists = list()
    nonRappers = list()
    albumList = list()
    trackList = list()
    results = sp.search(q=artistName,type='artist')

    for albumType in albumTypeList:
        results = sp.artist_albums(artistID,album_type=albumType)
        albums = results['items']
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])

        for album in albums:
            #print 'ALBUM: ',album['name'],'-------------------'
            trackSearch = sp.album_tracks(album['id'])
            tracks = trackSearch['items']
            while trackSearch['next']:
                trackSearch = sp.next(trackSearch)
                tracks.extend(trackSearch['items'])

            for track in tracks:
                if track['name'] not in trackList:
                    trackList.append(track['name'])
                    artistSearch = track['artists']

                    artistOnTrack = False
                    for i in range(len(artistSearch)):
                        if artistName in artistSearch[i]['name']:
                            artistOnTrack = True
                            break

                    if len(artistSearch) > 1 and artistOnTrack:
                        #print 'song: ',track['name'],'----'
                        #print 'Artists: '
                        for i in range(len(artistSearch)):
                            if artistSearch[i]['name'] not in allArtists and artistSearch[i]['name'] not in nonRappers:
                                #print artistSearch[i]['name']
                                artist = sp.artist(artistSearch[i]['id'])
                                #print artist['genres']
                                    #print artist['name']
                                #if (any(genre in artist['genres'] for genre in acceptedGenres) or artist['name'] in allRappers) and artistName not in artist['name']:
                                if (any(genre in artist['genres'] for genre in acceptedGenres)) and artistName not in artist['name']:
                                    allArtists.append(artistSearch[i]['name'])
                                else:
                                    #print artist['name'],' aint a rapper'
                                    #print artist['genres']
                                    nonRappers.append(artist['name'])


    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    allArtists = list(set(allArtists))
    collabFileName = str(''.join(c for c in artistName if c in valid_chars).replace(' ','') + '_collabFile')
    collabFile = open(collabFileName,'wr')

    for i in range(len(allArtists)):
        allArtists[i] = artistName + ',' + allArtists[i].encode('utf-8')+'\n'


    collabFile.writelines(allArtists)
    collabFile.close()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = artistName + "'s " +'collaborators'
    msg['From'] = 'adamsocialnetworkproject@gmail.com'
    msg['To'] = 'amontano495@gmail.com'
    body = '\n'.join(allArtists)
    msg.attach(MIMEText(body,'plain'))

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.login('adamsocialnetworkproject@gmail.com','goRY72QcsDZE')
    s.sendmail('adamsocialnetworkproject@gmail.com', ['amontano495@gmail.com'], msg.as_string())
    s.quit()

'''


