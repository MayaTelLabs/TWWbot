# THE WEST WING - EVERY FRAME IN ORDER BOT
# or, TWWBOT
# Maya Ventura - August 1st, 2024
# Based the now very decrepit MonogatariBot, from Spacebruce

# licensed under the MayaTel Labs Standard License. https://github.com/MayaTelLabs/MSL

# hi Liz. I know you'll be snooping around here. I love you a lot

import tweepy
import os
import time
import datetime

# Episode Config (this is manual, I'm real fuckin lazy)
season_num = 1
episode_num = 1
tweet_text = f"The West Wing - Season {season_num} Episode {episode_num}"

# Timing Config
wait_time = 1800 # Seconds after a Tweet, 30 minutes by default

# Directories
frame_dir = f"/Users/Maya/Documents/TWWBot-main/S{season_num}/"
current_episode_folder = f"E{episode_num}/"
image_folder = os.path.join(frame_dir,current_episode_folder)

# Frame Tweet Counter
counter = 0
Now = datetime.datetime.now()

# Launch Confirmation
connect_to_twitter = input('Connect to Twitter and start the script?')

# TOP SECRET DO NOT STEAL...
consumer_key = 'insert_key_here'
consumer_secret = 'insert_key_here'
access_token = 'insert_key_here'
access_token_secret = 'insert_key_here'

if connect_to_twitter.lower() == 'y':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Connected to Twitter!")
    except:
        print("Not connected to Twitter! Retrying...")
        time.sleep(10)
# specific 2.0 auth bullshit
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret)

# image_folder = f"{frame_dir}testSingle"
image_folder = f"{frame_dir}E{episode_num}"
print(f"Image folder: {image_folder} loaded")

# Load the index from a file (or initialize it to 0 if the file doesn't exist)
index_file = "progress.txt"
if os.path.exists(index_file):
    with open(index_file) as f:
        index = float(f.read())
    print("Progress.txt found. Resuming...")
else:
    index = 0
    print("No progress.txt found. From the top...")

# Determine number of frames
ListLength = len(os.listdir(image_folder))
print(ListLength, "files found")

# List images in folder
images = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpeg')]
images.sort()
for i in range(0, len(images)):
    images_to_tweet = images[i:1]
    # Skip files before the saved index
    if i < index:
        continue
    print(index)
    for j, image in enumerate(images_to_tweet):
        # Get the base name of the file
        base_name = os.path.basename(image)

       
    Status = f"{tweet_text}\nFrame {index+1} of {ListLength}"
    print(Status)
    
    retries = 0
    success = False
    while not success and retries < 5:
        if len(images_to_tweet) > 0:
            try:
                # Upload the images and get IDs
                media_ids = []
                media_metadata_list = []
                # Upload images
                response = api.media_upload(filename=image)
                print(f"Uploaded {image}")
                # Append media ID to list
                media_ids.append(response.media_id)
                # Tweet the images
                if connect_to_twitter.lower() == 'y':
                    # Post the FUCKIGN tweet
                    tweet = client.create_tweet(text=Status, media_ids=media_ids)
                else:
                    print(f"Processing files {images_to_tweet}")
                    time.sleep(3)
                success = True
            except tweepy.errors.TweepyException as error:
                print(f'Error while tweeting images {images_to_tweet}: {error}')
                retries += 1
                print('Trying again in 60.')
                time.sleep(60)
    if not success:
        print(f'Failed to tweet image {file} after {retries} attempts')
        # Wait for user input before exiting
        input("Too many errors. Press Enter to restart...")
    
    # Increment the index
    index += 1
    
    # Save progress to text file
    with open("progress.txt", "w") as f:
        f.write(str(index))
    
    # Increment the counter
    counter += 1

    # Sleep for the specified wait time.
    if counter == 1:
        print(f"Image posted. Waiting for {wait_time} seconds.\n")
        time.sleep(wait_time)
        counter = 0
        
# Wait for user input before exiting
input("Script's done. Press Enter to restart...")
