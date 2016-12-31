import hashlib
import os

output = ''

output += """insert into User values('sportslover', 'Paul', 'Walker', 'paulpass93', 'sportslover@hotmail.com');\n"""
output += """insert into User values('traveler', 'Rebecca', 'Travolta', 'rebeccapass15', 'rebt@explore.org');\n"""
output += """insert into User values('spacejunkie', 'Bob', 'Spacey', 'bob1pass', 'bspace@spacejunkies.net');\n"""

# insert albums
albumDict = {}
albumId = 1
albumDict['I love sports'] = albumId
output+= ('insert into Album values(' + 'DEFAULT' + """, 'I love sports', DEFAULT, DEFAULT, 'sportslover');\n""")
albumId += 1
albumDict['I love football'] = albumId
output+= ('insert into Album values(' + 'DEFAULT' + """, 'I love football', DEFAULT, DEFAULT, 'sportslover');\n""")
albumId += 1
albumDict['Around The World'] = albumId
output+= ('insert into Album values(' + 'DEFAULT' + """, 'Around The World', DEFAULT, DEFAULT, 'traveler');\n""")
albumId += 1
albumDict['Cool Space Shots'] = albumId
output+= ('insert into Album values(' + 'DEFAULT' + """, 'Cool Space Shots', DEFAULT, DEFAULT, 'spacejunkie');\n""")


# check files
seqNum = 0
m = hashlib.md5()
directory = "./../static/images"
for file in os.listdir(directory):
    if file.startswith('.'):
        continue
        
    dotNum = file.find('.')
    fname = file[0:dotNum]
    fformat = file[dotNum+1:len(file)]
    if fname.startswith('sports'):
        album = 'I love sports'
    elif fname.startswith('football'):
        album = 'I love football'
    elif fname.startswith('world'):
        album = 'Around The World'
    elif fname.startswith('space'):
        album = 'Cool Space Shots'

    albumId = albumDict[album]
    m.update(str(albumId))
    m.update(fname)
    picid = m.hexdigest()
    onme = os.path.join(directory, file)
    nnme = os.path.join(directory, picid + '.' + fformat)
    os.rename(onme, nnme)
        
    output += ("""insert into Photo values('""" + str(picid) + """', '""" + fformat + """', """ + 'DEFAULT' + """);\n""")
    output += ('insert into Contain values(' + str(seqNum) + ', ' + str(albumId) + """, '""" + str(picid) + """', '');\n""")

    seqNum += 1

oFile = open("load_data.sql", "w")
oFile.write(output)
oFile.close()