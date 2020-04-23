import sys
import csv
import classifier

def main():
    print "------------------"
    print 'processing the tweets from different cities and analysing the depression of the people'
    print 'writing output to output.csv'
    csvfile = open("output.csv", "a")
    csvwriter = csv.writer(csvfile)
    row = [ "city", "text","sentiment","created_at"]
    csvwriter.writerow(row)
    count = 0
    city_tweets = csv.reader(open('tweets.csv', 'rb'), delimiter=',')
    next(city_tweets, None)  # skip the headers
    for row in city_tweets:
        count = count + 1
        print count
        user_tweet = row[1]
        place = row[2]
        time = row[3]
        sentiment = classifier.classify(user_tweet)
        out_row = [ place, user_tweet, sentiment, time ]
        if(len(out_row) > 0):
            csvwriter.writerow(out_row)
    print "auto classified "+str(count)+" tweets"
if __name__ == "__main__":
    main()
