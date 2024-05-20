# aaa_chat_stats

Obtains the stats from the AAA chat

## Usage

The data you need for this script is the chat data from the AAA chat. This data is stored in a .json file. You can
download this data by going to the Settings & Privacy section of your Facebook account, and then choosing "Download you information".
Choose to download data about your messages in JSON format and then select how far back in time you want to collect your data from. To get
data from the most recent semester, 6 months should be easily enough.

After you have downloaded and saved the relevant data, adjust the generate_stats.py script to point to the correct data files "message_path_1"
and "message_path_2" in the init function. Each json file holds a maximum of 10,000 messages, so you may need to concatenate multiple files and their
messages as shown in the existing code. Note that you can delete all other chat data that you do not need, as they will not be used and take up space.

Once you have the data files set up, you can run the generate_stats.py script. This will generate a stats.txt file with the stats of the chat. Feel free to look
into the code and add additional stats that might be interesting to you!
