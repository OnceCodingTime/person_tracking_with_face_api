import iapp_ai
import vlc
import threading
import sys, os

path = "../API"
if not os.path.isdir(path):
    path = "./API"

sys.path.append(path)

def read_txt(path):
    with open(path, mode="r") as f:
        data = f.readline()
    return data.strip(" \n")
#'api key from https://ai.iapp.co.th/'

api_key = read_txt('apikey.txt')
api = iapp_ai.api(apikey=api_key)
company = "super_ai_ss3"

mp3_dir = "mp3"

mp3_filenames = {}

id_spoke = []
id_speaking = []

def thread_face_reg_and_tts(file_path, id=""):
    t = threading.Thread(target=face_recognition_and_tts, args=(file_path,id,))
    t.start()

def get_text2mp3(text,filename):
    tts_response = api.thai_thaitts_kaitom(text)
    if tts_response.status_code == 200:
        tts_content = tts_response.content
        with open(filename, "wb") as f:
            f.write(tts_content)

def play_mp3(filename):
    p = vlc.MediaPlayer(filename)
    p.play()

def face_recognition_and_tts(file_path):
    filename = f"{mp3_dir}/unknown.mp3"
    result = api.face_recog_single(file_path=file_path, company_name=company)
    if result.status_code == 200:
        res_json = result.json()
        person_name = res_json['name']

        if person_name != 'unknown':
            if person_name not in mp3_filenames:
                filename = f"{mp3_dir}/name-{len(mp3_filenames):03}.mp3"
                text = 'สวัสดีครับ คุณ'+person_name
                get_text2mp3(text=text,filename=filename)
                mp3_filenames.update({person_name:filename})
            else:
                filename = mp3_filenames[person_name]
        play_mp3(filename)
    else:
        play_mp3(filename)
        print(result.text)

def get_tts(file_path, id=""):
    global id_speaking, id_spoke

    if not id:
        face_recognition_and_tts(file_path)

    elif id not in id_spoke and id not in id_speaking:
        id_speaking.append(id)
        face_recognition_and_tts(file_path)

        id_spoke.append(id)
        id_speaking.append(id)

