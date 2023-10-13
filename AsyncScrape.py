import asyncio
import json
from tiktokapipy.async_api import AsyncTikTokAPI
from datetime import datetime, timezone
from tiktokapipy.api import TikTokAPIError



async def FetchVideos(hashtag, output):
    """
    param:
        hashtags: requested hashtags to fetch
    return:
        dict {video_id: [url, creation_date, description=""]}
    """
    async with AsyncTikTokAPI() as api:
        threshold_datetime = datetime(2023, 10, 7, tzinfo=timezone.utc)
        print(f"hashtag: {hashtag}")
        try:
            tag = await api.challenge(hashtag, video_limit=10)
        except TikTokAPIError as err:
            print("================WARNING================\n" +
            f"hashtag - {hashtag} - FAILED TO FIND HASHTAG\n" +
            "================WARNING================")
        videos = tag.videos
        try:
            async for video in videos:
                # video_comments = DeferredCommentIterator(api, video.id)   # TODO: classify by comments (optional)
                print(f"{video.create_time}  :  {threshold_datetime}")
                if video.create_time > threshold_datetime:
                    output[video.id] = [video.url, video.create_time, video.desc]
                else:
                    print("  -not relevant")
        except Exception as err:  # 
                print(f"hashtag - {hashtag} - FAILED TO GET VIDEOS. Error: {err}")
                return
    

async def FetchHashtags(hashtags):
    output = {}
    tasks = []
    for hashtag in hashtags:
        t = asyncio.create_task(FetchVideos(hashtag, output))
        tasks.append(t)
    for t in tasks:
        await asyncio.wait_for(t, timeout=15)
    return output


def LoadHashtagFromFile(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File {file_path} not found. Please check the file path.")
        return []



def SaveDataToFile(video_data, filename="support.json"):
    """
    Saves the video data to a specified file in JSON format.
    
    Parameters:
        video_data (dict): Dictionary containing video data.
        filename (str, optional): Name of the file to save data to. Defaults to "output.json".
    """
    CleanDataVideo(video_data)
    try:
        with open(filename, 'w') as f:
            json.dump(video_data, f, indent=4)
        print(f"Data saved successfully to {filename}")
    except Exception as e:
        print(f"Failed to save data to {filename}. Error: {e}")
    






def CleanDataVideo(video_data):
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
    
    support_hashtags = LoadHashtagFromFile('try.txt')
    print(support_hashtags)
    print(asyncio.run(FetchHashtags(support_hashtags)))
    #print(video_data)
    
    #SaveDataToFile(video_data)


if __name__ == "__main__":
    main()