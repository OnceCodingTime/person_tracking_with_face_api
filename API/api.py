import iapp_ai
import vlc
import threading

api_key = 'api key from https://ai.iapp.co.th/'
api = iapp_ai.api(apikey=api_key)
company = "super_ai_ss3"

path = "API/mp3"

mp3_filenames = {}

id_spoke = []
id_speaking = []

def thread_face_reg_and_tts(file_path, id):
    t = threading.Thread(target=face_recognition, args=(file_path,id,))
    t.start()

def get_text2mp3(text,filename):
    with open(filename, "wb") as f:
        f.write(api.thai_thaitts_kaitom(text).content)

def play_mp3(filename):
    p = vlc.MediaPlayer(filename)
    p.play()

def face_recognition(file_path, id):
    global id_speaking, id_spoke
    # print(file_path)
    # print(all_id)
    if id not in id_spoke and id not in id_speaking:
        id_speaking.append(id)
        result = api.face_recog_single(file_path=file_path, company_name=company)

        if result.status_code == 200:
            res_json = result.json()
            person_name = res_json['name']

            if person_name != 'unknown':
                if person_name not in mp3_filenames:
                    filename = f"{path}/name-{len(mp3_filenames):03}.mp3"
                    text = 'สวัสดีครับ คุณ'+person_name
                    get_text2mp3(text=text,filename=filename)
                    mp3_filenames.update({person_name:filename})
                else:
                    filename = mp3_filenames[person_name]
                
                play_mp3(filename)
                id_spoke.append(id)
        id_speaking.append(id)

