from tiktokapipy.api import TikTokAPI, TikTokAPIError
from tiktokapipy.util.deferred_collectors import DeferredCommentIterator
import translators
import json
from datetime import datetime, timezone

support_hashtags = [
    "standwithisrael", "jews", "peace", "idf", "supportisrael", 
    "istandwithisrael", "warzone", "warinisrael", "israelunderattack", 
    "freeisrael", "standwithus", "bringthemback", "spreadthetruth", "israel", 
    "Swords_of_Iron", "hostages", "israelgazaconflict", "help", "novafestival", 
    "יהודי", "מדינתישראל", "מלחמה", "חטופים", "שבויים", 
    "ישראל", "מילואים", "צהל", "תנולצהללנצח", "עםישראלחי", "עםישראלחייי🇮🇱", 
    "🇮🇱🇮🇱🇮🇱", "מחאה", "מלחמהבישראל", "אזעקות", "עוטףעזה", "פחד", 
    "טילים", "חרבותברזל", "צבאהגנהלישראל", "אמונה", "ניצולים", "חיילים", 
    "צה״ל", "משטרתישראל", "חמל", "מילואימניקים", "פוריומלחמה", "מבצעחרבותברזל", 
    "חללימערכותישראל", "המצבבמדינה", "תודהלבוראעולם", "למחוקאתעזה", "מחדל", 
    "נחטפו", "תעזרולי", "מבצעצבאי", "לזכרםשלכלנפגעיהטרור", "הינקוםדמם", 
    "יהיה_טוב", "גולני", "ניצוליהמסיבה"
]


against_hashtags = [
    "جنين_نابلس_طولكرم_رام_الله_فلسطين", "freepalestine🇵🇸", "tiktokdz", "algeria🇵🇸🇩🇿", 
    "palestine🇵🇸❤️", "palestinelivesmatter", "falestine", "palestine", "palestinetiktok", "dzpower", 
    "algerienne", "ArabTikTok", "Palestina", "israel", "Telaviv", "Kudüs", "Quds", "masjidalaqsa", 
    "Aksa", "Islam", "FREEPALESTINE", "🇵🇸", "Celtic", "Palesadelinderfba&", "Freepalestin", "Hamas", 
    "foryoupage", "freepalestine", "bellahadid", "gigihadid", "celebrities", "viral", "blowthisup", 
    "hadidsisters", "fvp>viral", "fyp", "fyppppppppppppppppppppp", "news", "foryou", "standwithpalestine", 
    "pubg", "trending", "viralvideo", "Unfreezemyaccoun", "gaza", "muslimfyp", "muslim", "war", "alaqsa", 
    "فلسطين_حرة🇵🇸", "الجزائر🇵🇸🇩🇿", "حياة_فلسطين_مهمة", "فلسطين", "تيكتوك_فلسطين", "جزائرية", 
    "تيكتوك_عربي", "إسرائيل", "تل_أبيب", "القدس", "المسجد_الأقصى", "الأقصى", "الإسلام", "حماس", 
    "لك_الصفحة", "بيلا_حديد", "جيجي_حديد", "مشاهير", "فيروسي", "أخوات_حديد", "أخبار", "لك", 
    "أنا_مع_فلسطين", "بوبجي", "تتجه", "فيديو_فيروسي", "غزة", "مسلم_لك", "مسلم", "حرب"
]



hashtags = ["طوفان_القدس"]


def FetchVideos(hashtags):
    """
    param:
        hashtags: requested hashtags to fetch
    return:
        dict {video_id: [url, creation_date, description=""]}
    """
    with TikTokAPI() as api:
        output = {}
        threshold_datetime = datetime(2023, 10, 7, tzinfo=timezone.utc)

        for hashtag in hashtags:
            print(f"hashtag: {hashtag}")
            try:
                tag = api.challenge(hashtag, video_limit=10)
            except TikTokAPIError as err:
                print("================WARNING================\n" +
                f"hashtag - {hashtag} - FAILED TO FIND HASHTAG\n" +
                "================WARNING================")

            try:
                for video in tag.videos:
                    # video_comments = DeferredCommentIterator(api, video.id)   # TODO: classify by comments (optional)
                    if video.create_time > threshold_datetime:
                        output[video.id] = [video.url, video.create_time, video.desc]
                    else:
                        print("  -not relevant")
            except Exception as err:  # 
                 print(f"hashtag - {hashtag} - FAILED TO GET VIDEOS")
                 continue
        return output
            


def SaveDataToFile(video_data, filename="output.json"):
    """
    Saves the video data to a specified file in JSON format.
    
    Parameters:
        video_data (dict): Dictionary containing video data.
        filename (str, optional): Name of the file to save data to. Defaults to "output.json".
    """
    clean_video_data(video_data)
    with open(filename, 'w') as f:
        json.dump(video_data, f, indent=4)
    


def clean_video_data(video_data):
    """
    Cleans and translates video description data.
    
    Parameters:
        video_data (dict): Dictionary containing video data.
    """
    for key in video_data.keys():
        desc = video_data[key][2]
        desc = desc.replace("#", "# ")
        # desc = translators.translate_text(desc)
        video_data[key] = (video_data[key][0], str(video_data[key][1]), desc)

                

def main():
    """
    Main function to execute the fetching and saving operations.
    """
    video_data = FetchVideos(support_hashtags)

    SaveDataToFile(video_data)


if __name__ == "__main__":
    main()