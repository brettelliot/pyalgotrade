from pyalgotrade import eventstudy
from pyalgotrade.barfeed import alphavantagefeed
import datetime
from pyalgotrade.barfeed import csvfeed
import pandas as pd

# Event inspired on an example from Ernie Chan's book:
# 'Algorithmic Trading: Winning Strategies and Their Rationale'


class EventList:
    def __init__(self):
        csv_file_name = './data/eventstudyAVdates.csv'

        df = pd.read_csv(csv_file_name,
                         encoding="ISO-8859-1",
                         usecols=["Date", "Value"],
                         parse_dates=['Date'],
                         index_col='Date')

        # Sort by date
        df = df.sort_index()

        # Select rows after a certain date.
        df = df.loc['2012-01-01':'2015-12-31']
        df = df[df['Value'] >= 7]
        df = df.drop(['Value'], axis=1)

        self.__datetimes = df.index.tolist()

    def get_datetime_list(self):
        return self.__datetimes

class BuyOnEvent(eventstudy.Predicate):
    def __init__(self, feed):
        super(BuyOnEvent, self).__init__()
        event_ist = EventList()
        self.__dates = event_ist.get_datetime_list()

    def eventOccurred(self, instrument, bards):
        ret = False

        if bards[-1].getDateTime() in self.__dates:
            #print("Got one: {0}".format(bards[-1].getDateTime()))
            ret = True
        return ret


def main(plot):

    feed = alphavantagefeed.Feed()

    start_date = datetime.datetime(2012, 1, 1)
    end_date = datetime.datetime(2015, 12, 31)

    data_filter = csvfeed.DateRangeFilter(fromDate=start_date, toDate=end_date)
    feed.setBarFilter(data_filter)
    feed.addBarsFromCSV("AAPL", "./data/daily_adjusted_AAPL.csv")
    feed.addBarsFromCSV("MSFT", "./data/daily_adjusted_MSFT.csv")
    feed.addBarsFromCSV("SPY", "./data/daily_adjusted_SPY.csv")

    predicate = BuyOnEvent(feed)
    event_study = eventstudy.EventStudy(predicate, 5, 5)
    event_study.run(feed, True)

    results = event_study.getResults()
    print("%d events found" % (results.getEventCount()))
    if plot:
        eventstudy.plot(results)

if __name__ == "__main__":
    main(True)
