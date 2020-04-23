from TwitterAPI import TwitterAPI
import csv

#--------------------------------------------------------------------------
# for fetching tweets from tiwtter api and saving them in a csv file
#--------------------------------------------------------------------------
def save_tweets():
        print "save tweets "
        csvfile = open("tweets6.csv", "a")
        csvwriter = csv.writer(csvfile)
        row = [ "user", "text","place","created_at"]
        i = 0
        csvwriter.writerow(row)
        try:
                api = TwitterAPI('XXXXXXXXXXXXXXXXXX',
                                 'XXXXXXXXXXXXXXXXXXXXX',
                                 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                                 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
                r = api.request('statuses/filter', {'locations':'-76,45,-75,46'}) #ottawa geolocation
                for item in r:
                        print(i)
                        i = i+1
                        #print item
                        text = item['text'].encode('ascii', 'replace')
                        user = item['user']['name'].encode('ascii', 'replace') if item['user'] != None else ''
                        place = item['place']['full_name'].encode('ascii', 'replace') if item['place'] != None else ''
                        created_at = item['created_at'].encode('ascii', 'replace')
                        row = [ user, text, place, created_at ]
                        csvwriter.writerow(row)
        except Exception as ex:
                print "error while saving tweets"
                print ex



def main():
        save_tweets()

if __name__== "__main__":
  main()





