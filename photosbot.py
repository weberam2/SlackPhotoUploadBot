import os
import slack
from slack.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('/home/weberam2/Pictures/_MikeTimGooglePhotos/') / '.env'
load_dotenv(dotenv_path=env_path)

# init slack client with access token
#slack_token = os.environ['SLACK_TOKEN']
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

#dirName = './BarnesLeonard-001'

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

filelist = getListOfFiles('/home/weberam2/Pictures/_MikeTimGooglePhotos/BarnesLeonard-001/')

fileslen = len(filelist)

with open('/home/weberam2/Pictures/_MikeTimGooglePhotos/num.txt') as f:
    lines = f.readlines()
    num = (lines[0])

num = int(num)

if num == fileslen:
    num = 0

choosefile = filelist[num]

try:
    client.files_upload(file=choosefile,
        initial_comment='Here is your pic of the day:',
        channels='#general'
    )

except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")

with open('/home/weberam2/Pictures/_MikeTimGooglePhotos/num.txt','r+') as myfile:
    data = myfile.read()
    myfile.seek(0)
    myfile.write(str(num+1))
    myfile.truncate()
