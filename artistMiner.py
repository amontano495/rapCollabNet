import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import pprint
import string
import smtplib
from email.parser import Parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


def sendMail(body):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Ding!'
    msg['From'] = 'adamsocialnetworkproject@gmail.com'
    msg['To'] = 'amontano495@gmail.com'
    msg.attach(MIMEText(body,'plain'))

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.login('adamsocialnetworkproject@gmail.com','goRY72QcsDZE')
    s.sendmail('adamsocialnetworkproject@gmail.com', ['amontano495@gmail.com'], msg.as_string())
    s.quit()


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
        fullTrack = spotipyInstance.track(track['id'])
        trackList.append(fullTrack)

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
            artists = list()
            trackPop = track['popularity']

            if len(track['artists']) < 2:
                continue

            else:
                for i in range(len(track['artists'])):
                    artists.append(track['artists'][i]['name'])

                if artistName in artists or artistName in track['name']:
                    artists[:] = [x for x in artists if x != artistName]

                    for artist in artists:
                            if artist in allRappers:
                                collaborators.append(
                                        str(artist.encode('utf-8') + 
                                            ',' + 
                                            str(trackPop)))

    return collaborators

def getPop(artistName,spotipyInstance):
    results = sp.search(q=artistName,type='artist')
    artistID = results['artists']['items'][0]['uri'].split(':')[2]
    artistObj = spotipyInstance.artist(artistID)
    return artistObj['followers']['total']



client_credentials_manager = SpotifyClientCredentials(client_id='b522ba0a33df4fe5b09357c42a7edda9', client_secret='cf073ed6ddb043dda91c74e5773a3c3d')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


allRappers = list()
rapperListFile = open('rapperList','r')
for rapper in rapperListFile:
    allRappers.append(rapper[:-1])
rapperListFile.close()


#print collabFinder('Higher Brothers',sp,allRappers)
#print getPop('Higher Brothers',sp)

edgeList = list()
nodeList = list()
errorList= list()

nodeFile = open('node_list', 'w')
collabFile = open('edge_list','w')
errorFile = open('error_list','w')

counter = 0
for rapper in allRappers:
    if counter == 288:
        sendMail('25 percent finished!')
    elif counter == 577:
        sendMail('50 percent finished!')
    elif counter == 866:
        sendMail('75 percent finished!')

    try:
        collabs = collabFinder(rapper,sp,allRappers)
        for entry in collabs:
            edgeList.append(str(rapper + ',' + entry + '\n'))

        rapperPopularity = getPop(rapper,sp)
        nodeList.append(str(rapper + ',' + str(rapperPopularity) + str(len(collabs)) + '\n'))

    except Exception, e:
        errorList.append(str(rapper+'\n'))
        continue
    counter += 1


collabFile.writelines(edgeList)
collabFile.close()

errorFile.writelines(errorList)
errorFile.close()

nodeFile.writelines(nodeList)
nodeFile.close()

sendMail('DING we are done!')
