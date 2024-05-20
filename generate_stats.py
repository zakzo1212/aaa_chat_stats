import json
import os

class Parser():

    def __init__(self):
        """
        Loads in and combines all the chat data from the downloaded messages files. 
        """
        # message_path = "2023_data/your_facebook_activity/messages/inbox/fall_23_freps/message_1.json"
        # message_path = "2023_data/your_facebook_activity/messages/inbox/fall_23_nofreps/message_1.json"
        message_path_1 = "data/messages/messages/inbox/chat_sp24/message_1.json"
        message_path_2 = "data/messages/messages/inbox/chat_sp24/message_2.json"

        with open(message_path_1, "r") as f1, open(message_path_2, "r") as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

        data1['messages'] += (data2['messages'])
        self.data = data1

        # with open(message_path, "r") as f:
        #     self.data = json.load(f)

        if 'stats.txt' in os.listdir():
            os.remove("stats.txt")

        with open("stats.txt", "w") as f:
            f.write("StAAAts for the Spring 2024 AAA ChAAAt \n" + "-"*50 + "\n\n")
            # f.write("StAAAts for the Fall 2023 ChAAAt w/ Freps\n" + "-"*50 + "\n\n")
            # f.write("StAAAts for the Fall 2023 ChAAAt w/out Freps\n" + "-"*50 + "\n\n")

    def _sort_dict(self, d):
        """
        Sorts the dictionary by value in descending order
        """
        return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))

    def messages_per_person(self, log=True):
        """
        returns a dictionary mapping each person to the number of messages they've sent
        """
        messages_per_person = {}

        for message in self.data['messages']:
            messages_per_person[message['sender_name']] = messages_per_person.get(message['sender_name'], 0) + 1

        messages_per_person = self._sort_dict(messages_per_person)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Messages per person: \n" + "-"*50 + "\n")
                for person, messages in messages_per_person.items():
                    f.write(f"{person:25}: {messages}\n")
                f.write("\n")

        return messages_per_person
    
    def total_messages(self, log=True):
        """
        returns the total number of messages in the chat
        """
        total = len(self.data['messages'])
        if log:
            with open("stats.txt", "a") as f:
                f.write("Total messages: \n" + "-"*50 + "\n")
                f.write(f"Total messages: {total}\n")
                f.write("\n")
        return len(self.data['messages'])
    
    def count_message_match(self, keys: list, log=True):
        """
        returns a dictionary mapping each person to the number of messages they've sent that contain any of the words in the keys list
        """
        message_matches = keys
        message_matches_per_person = {}
        for message in self.data['messages']:
            if 'content' not in message.keys():
                continue
            if any(match in message['content'].lower() for match in message_matches):
                message_matches_per_person[message['sender_name']] = message_matches_per_person.get(message['sender_name'], 0) + 1

        message_matches_per_person = self._sort_dict(message_matches_per_person)
        if log:
            with open("stats.txt", "a") as f:
                f.write(f"Messages containing {keys}: \n" + "-"*50 + "\n")
                for person, messages in message_matches_per_person.items():
                    f.write(f"{person:25}: {messages}\n")
                f.write("\n")
        return message_matches_per_person
    
    def reacts_received(self, log=True):
        """
        returns a dictionary mapping each person to the number of reactions they've received on their messages
        """
        reacts_per_person = {}
        for message in self.data['messages']:
            if 'reactions' not in message.keys():
                continue
            for react in message['reactions']:
                reacts_per_person[message['sender_name']] = reacts_per_person.get(message['sender_name'], 0) + 1

        reacts_per_person = self._sort_dict(reacts_per_person)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Reacts Received: \n" + "-"*50 + "\n")
                for person, reacts in reacts_per_person.items():
                    f.write(f"{person:25}: {reacts}\n")
                f.write("\n")
        
        return reacts_per_person

    def reacts_given(self, log=True):
        """
        returns a dictionary mapping each person to the number of reactions they've given on other people's messages
        """
        reacts_per_person = {}
        for message in self.data['messages']:
            if 'reactions' not in message.keys():
                continue
            for react in message['reactions']:
                reacts_per_person[react['actor']] = reacts_per_person.get(react['actor'], 0) + 1

        reacts_per_person = self._sort_dict(reacts_per_person)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Reacts Given: \n" + "-"*50 + "\n")
                for person, reacts in reacts_per_person.items():
                    f.write(f"{person:25}: {reacts}\n")
                f.write("\n")

        return reacts_per_person
    
    def likes_to_messages_ratio(self, log=True):
        """
        returns a dictionary mapping each person to the ratio of the number of reactions they've received to the number of messages they've sent
        """
        reacts_per_person = self.reacts_received(log=False)
        messages_per_person = self.messages_per_person(log=False)

        ratio = {}
        for person in reacts_per_person.keys():
            ratio[person] = round(reacts_per_person[person] / messages_per_person[person], 6)
        
        ratio = self._sort_dict(ratio)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Likes to messages ratio: \n" + "-"*50 + "\n")
                for person, r in ratio.items():
                    f.write(f"{person:25}: {r}\n")
                f.write("\n")
        return ratio
    
    def self_likers(self, log=True):
        """
        returns a dictionary mapping each person to the number of times they've liked their own messages
        """
        self_likes_per_person = {}
        for message in self.data['messages']:
            if 'reactions' not in message.keys():
                continue
            for react in message['reactions']:
                if react['actor'] == message['sender_name']:
                    self_likes_per_person[message['sender_name']] = self_likes_per_person.get(message['sender_name'], 0) + 1
        
        self_likes_per_person = self._sort_dict(self_likes_per_person)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Self-likers: \n" + "-"*50 + "\n")
                for person, likes in self_likes_per_person.items():
                    f.write(f"{person:25}: {likes}\n")
                f.write("\n")

        return self_likes_per_person
    
    def likes_given_per_person(self):
        """
        returns a dictionary mapping each person to another dictionary mapping the people they liked to the number of times they liked that person's messages

        ie. {
            'person1': {
                'person2': 5,
                'person3': 3
            },
            'person2': {
                'person1': 2,
                'person3': 1
            }
        }
        """
        likes_per_person = {}
        for message in self.data['messages']:
            if 'reactions' not in message.keys():
                continue
            for react in message['reactions']:
                likes_per_person[message['sender_name']] = likes_per_person.get(message['sender_name'], {})
                likes_per_person[message['sender_name']][react['actor']] = likes_per_person[message['sender_name']].get(react['actor'], 0) + 1
        
        return likes_per_person
    

    def _sort_admirers_or_haters(self, admirers_or_haters):
        """
        Sorts the output of secret_admirers or secret_haters by the percentage of messages liked
        """
        return dict(sorted(admirers_or_haters.items(), key=lambda item: item[1][0], reverse=True))

    def secret_admirers(self, log=True):
        """
        Finds all instances of people who like >= 25% of the messages of another person. 

        Algorithm first finds the total number of messages each person has sent. Then, for each person, finds how many of every other person's messages they liked.
        Then, for each pair of people, calculates the percentage of messages liked by the first person. If this percentage is >=5%, add that pair of people 
        and their ratio to the output. Specifically, the output maps admirer name --> (percentage of messages liked, person liked)
        """
        messages_per_person = self.messages_per_person(log=False)
        likes_given_per_person = self.likes_given_per_person()
        secret_admirers = {}
        for person in messages_per_person.keys():
            for liked_person in likes_given_per_person[person].keys():
                if likes_given_per_person[person][liked_person] / messages_per_person[liked_person] >= 0.1:
                    secret_admirers[person] = (round(likes_given_per_person[person][liked_person] / messages_per_person[liked_person], 4), liked_person)

        secret_admirers = self._sort_admirers_or_haters(secret_admirers)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Secret Admirers: \n" + "-"*50 + "\n")
                for admirer, (ratio, admired) in secret_admirers.items():
                    f.write(f"{admirer:25} likes {admired} {ratio*100:.4}% of the time\n")
                f.write("\n")

        return secret_admirers
    
    def secret_haters(self, log=True):
        """
        same as secret admirers, but logs people who like the least percentage of another person's messages
        """
        messages_per_person = self.messages_per_person(log=False)
        likes_given_per_person = self.likes_given_per_person()
        secret_haters = {}
        for person in messages_per_person.keys():
            for liked_person in likes_given_per_person[person].keys():
                if likes_given_per_person[person][liked_person] / messages_per_person[liked_person] <= 0.0025:
                    secret_haters[person] = (round(likes_given_per_person[person][liked_person] / messages_per_person[liked_person], 4), liked_person)
        
        secret_haters = self._sort_admirers_or_haters(secret_haters)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Secret Haters: \n" + "-"*50 + "\n")
                for hater, (ratio, hated) in secret_haters.items():
                    f.write(f"{hater:25} likes {hated} {ratio*100:.7}% of the time\n")
                f.write("\n")
                
        return secret_haters
    
    def most_reacted_messages(self, n, log=True):
        """
        finds the top n most reacted messages and records the message content, the sender, and the number of reactions
        """
        reacts_per_message = {}
        for message in self.data['messages']:
            if 'reactions' not in message.keys() or 'content' not in message.keys():
                continue
            reacts_per_message[message['content']] = len(message['reactions'])
        
        reacts_per_message = self._sort_dict(reacts_per_message)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Most reacted messages: \n" + "-"*50 + "\n")
                for message, reacts in list(reacts_per_message.items())[:n]:
                    f.write(f"{message}...: {reacts}\n")
                f.write("\n")
        
        return reacts_per_message
    
    def best_message_per_person(self, log=True):
        """
        returns a dict mapping each person to their most reacted message as well as the number of reactions it received
        """
        best_message_per_person = {}
        for message in self.data['messages']:
            if 'reactions' not in message.keys() or 'content' not in message.keys():
                continue
            if message['sender_name'] not in best_message_per_person.keys():
                best_message_per_person[message['sender_name']] = (message['content'], len(message['reactions']))
            elif len(message['reactions']) > best_message_per_person[message['sender_name']][1]:
                best_message_per_person[message['sender_name']] = (message['content'], len(message['reactions']))
        
        if log:
            with open("stats.txt", "a") as f:
                f.write("Best message per person: \n" + "-"*50 + "\n")
                for person, (message, reacts) in best_message_per_person.items():
                    f.write(f"{person:25}: {message}... ({reacts} reacts)\n")
                f.write("\n")
        
        return best_message_per_person
    
    def most_times_atted(self, log=True):
        """
        returns a dictionary mapping each person to the number of times they've been @'d
        """
        ats_per_person = {}
        for message in self.data['messages']:
            if 'content' not in message.keys():
                continue
            ats_per_person[message['sender_name']] = ats_per_person.get(message['sender_name'], 0) + message['content'].count('@')

        ats_per_person = self._sort_dict(ats_per_person)
        if log:
            with open("stats.txt", "a") as f:
                f.write("Most @'d people: \n" + "-"*50 + "\n")
                for person, ats in ats_per_person.items():
                    f.write(f"{person:25}: {ats}\n")
                f.write("\n")
        
        return ats_per_person

def main():
    parser = Parser()

    squid_keys = ['squid']
    AAA_keys = ['aaa']
    rizz_keys = ['rizz']
    rat_keys = ['rat', 'ratting', 'rats']
    snipe_keys = ['snipe', 'sniping', 'sniped', 'snipes']
    at_keys = ['@']
    furry_keys = ['furry', 'furries']
    uwu_keys = ['uwu', 'owo', 'rawr']
    drinking_keys = ['drinking', 'drinks', 'drunk', 'drank', 'drink', 'alcohol', 'beer', 'wine', 'liquor', 'vodka', 'whiskey', 'alc', 'alcoholic']

    total_messages = parser.total_messages()
    messages_per_person = parser.messages_per_person()
    squid_messages = parser.count_message_match(squid_keys)
    AAA_messages = parser.count_message_match(AAA_keys)
    rizz_messages = parser.count_message_match(rizz_keys)
    snipe_messages = parser.count_message_match(snipe_keys)
    at_messages = parser.count_message_match(at_keys)
    rat_messages = parser.count_message_match(rat_keys)
    furry_messages = parser.count_message_match(furry_keys)
    drinking_messages = parser.count_message_match(drinking_keys)
    uwu_messages = parser.count_message_match(uwu_keys)
    reacts_received = parser.reacts_received()
    reacts_given = parser.reacts_given()
    likes_to_messages_ratio = parser.likes_to_messages_ratio()
    self_likers = parser.self_likers()

    secret_admirers = parser.secret_admirers()
    secret_haters = parser.secret_haters()

    most_reacted_messages = parser.most_reacted_messages(10)
    best_message_per_person = parser.best_message_per_person()
    most_times_atted = parser.most_times_atted()

if __name__ == "__main__":
    main()