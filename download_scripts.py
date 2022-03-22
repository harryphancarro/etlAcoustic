import requests
import json
import pandas as pd

csv_name = 'listing_files_engine_audio_202202161248'

f = open(f'.\{csv_name}.json')

data = json.load(f)
df = pd.DataFrame(data['listing_files_engine_audio'])

print(df['mime_type'].value_counts())
# allow_extention = ['wav','aac','mp3','flac']
mime_types_dict = {'audio/x-m4a':'m4a','video/3gpp':'3gp','video/mp4':'mp4','image/jpeg':'jpg','application/octet-stream':'bin','application/zip':'zip'}

audio_names = []
count = 0
for i in data['listing_files_engine_audio']:
    id = i['id']
    filename = i['url'].rsplit('/', 1)[1]

    url = str(i['url']).replace("\/","/")

    if i['mime_type'] in list(mime_types_dict.keys()):
        extention = mime_types_dict[i["mime_type"]]
        filename = f'{filename}.{extention}'   
        audio_names.append(filename)
        error_dict = []
        r = requests.get(url)
        with open(f"./2022-info/{id}_{filename}",'wb') as f:
            f.write(r.content)
        count=count+1
        if count//100:
            print(count)

f.close()

df['audio_name'] = audio_names
df.to_csv(f'.\{csv_name}.csv',index=False)