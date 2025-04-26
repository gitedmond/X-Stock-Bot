import schedule
import time
from datetime import datetime, time as dt_time

class StockBot:
    """Bot that monitors stock data and posts tweets about significant events"""
    
    def __init__(self, stock_client, twitter_client, symbol, data_file, market_hours=None):
        """Initialize with necessary clients and configuration"""
        self.stock_client = stock_client
        self.twitter_client = twitter_client
        self.symbol = symbol
        self.sma_differences = []
        self.data_file = data_file
        
        # Default market hours if none provided
        if market_hours is None:
            self.market_hours = {
                'start': dt_time(8, 30),
                'end': dt_time(15, 0)
            }
        else:
            self.market_hours = market_hours
    
    def is_market_hours(self):
        """Check if current time is during market hours and it's a weekday"""
        current_time = datetime.now().time()
        current_day = datetime.now().weekday()
        return (self.market_hours['start'] <= current_time <= self.market_hours['end'] 
                and current_day < 5)  # 0-4 is Monday-Friday
    
    def is_weekday(self):
        """Check if current day is a weekday"""
        return datetime.now().weekday() < 5
    
    # def fetch_and_save_quote(self):
    #     """Fetch and save quote data to a file"""
    #     if not self.is_weekday():
    #         print("It's a weekend. Skipping quote data fetch.")
    #         return
        
    #     try:
    #         quote_data = self.stock_client.get_quote(self.symbol)
            
    #         if 'open' in quote_data:
    #             datetime_value = quote_data.get('datetime', datetime.now().strftime("%Y-%m-%d"))
                
    #             # Format quote data
    #             content = (
    #                 f"${self.symbol} Quote for {datetime_value}: \n"
    #                 f"Open: {quote_data['open']}\n"
    #                 f"High: {quote_data['high']}\n"
    #                 f"Low: {quote_data['low']}\n"
    #                 f"Close: {quote_data['close']}\n"
    #                 f"#spy, #stocks, #technicalindicator, #gcgdwatcher\n"
    #             )
                
    #             # Write quote data to file
    #             with open(self.data_file, 'w') as txt_file:
    #                 txt_file.write(content)
                    
    #             print(f"Quote data saved to '{self.data_file}'.")
    #             return content
    #         else:
    #             print("No valid quote data found in the response.")
    #             return None
                
    #     except Exception as e:
    #         print(f"An error occurred while fetching quote data: {str(e)}")
    #         return None
    
    # def tweet_open_price(self):
    #     """Tweet the opening price of the stock"""
    #     if not self.is_weekday():
    #         print("It's a weekend. Skipping open price tweet.")
    #         return
        
    #     try:
    #         with open(self.data_file, 'r') as txt_file:
    #             lines = txt_file.readlines()
    #             if len(lines) > 1:
    #                 open_line = lines[1]  # Assuming 'Open' is the second line
    #                 # Extract the number from the 'open' line
    #                 open_number = open_line.split(":")[1].strip()
    #                 tweet_content = f"${self.symbol} has opened at {open_number} today."
    #                 self.twitter_client.post_tweet(tweet_content)
    #             else:
    #                 print("No 'Open' data found in the file.")
    #     except Exception as e:
    #         print(f"An error occurred while tweeting the opening price: {str(e)}")
    
    # def tweet_daily_quote(self):
    #     """Tweet the full quote data at market close"""
    #     if not self.is_weekday():
    #         print("It's a weekend. Skipping daily quote tweet.")
    #         return
        
    #     try:
    #         with open(self.data_file, 'r') as txt_file:
    #             tweet_content = txt_file.read()
            
    #         self.twitter_client.post_tweet(tweet_content)
    #     except Exception as e:
    #         print(f"An error occurred while tweeting quote data: {str(e)}")
    
    def check_sma_crossover(self):
        """Check for SMA crossover events (Golden Cross/Death Cross)"""
        if not self.is_market_hours():
            return
        
        try:
            # Get SMA-50 data
            sma50_data = self.stock_client.get_sma(self.symbol, "50")
            sma50 = float(sma50_data["values"][0]["sma"])
            
            # Get SMA-200 data
            sma200_data = self.stock_client.get_sma(self.symbol, "200")
            sma200 = float(sma200_data["values"][0]["sma"])
            
            # Calculate difference between SMA-50 and SMA-200
            difference = round(sma50 - sma200, 5)
            self.sma_differences.append(difference)
            
            print(f"SMA50: {sma50} | SMA200: {sma200} | Difference: {difference}")
            
            # Check for crossover if we have at least 2 data points
            if len(self.sma_differences) >= 2:
                prev_diff = self.sma_differences[-2]
                current_diff = self.sma_differences[-1]
                
                # Golden Cross: SMA50 crosses above SMA200
                if prev_diff < 0 and current_diff >= 0:
                    message = (f"${self.symbol} has experienced a Golden Cross! "
                              f"The 50-day SMA has crossed above the 200-day SMA, "
                              f"potentially indicating a bullish trend.")
                    self.twitter_client.post_tweet(message)
                    print("Golden Cross detected!")
                
                # Death Cross: SMA50 crosses below SMA200
                elif prev_diff > 0 and current_diff <= 0:
                    message = (f"${self.symbol} has experienced a Golden Death! "
                              f"The 50-day SMA has crossed below the 200-day SMA, "
                              f"potentially indicating a bearish trend.")
                    self.twitter_client.post_tweet(message)
                    print("Golden Death detected!")
                    
            # Keep list size manageable
            if len(self.sma_differences) > 100:
                self.sma_differences = self.sma_differences[-50:]
                
        except Exception as e:
            print(f"Error checking SMA crossover: {e}")
    
    def schedule_tasks(self, morning_fetch_time, morning_tweet_time, evening_fetch_time, evening_tweet_time, sma_check_interval):
        """Schedule all routine tasks"""
        # # Daily market open tasks
        # schedule.every().day.at(morning_fetch_time).do(self.fetch_and_save_quote)
        # schedule.every().day.at(morning_tweet_time).do(self.tweet_open_price)
        
        # # Daily market close tasks
        # schedule.every().day.at(evening_fetch_time).do(self.fetch_and_save_quote)
        # schedule.every().day.at(evening_tweet_time).do(self.tweet_daily_quote)
        
        # SMA crossover check every X minutes during market hours
        schedule.every(sma_check_interval).minutes.do(self.check_sma_crossover)
    
    def run(self, sma_check_interval):
        """Run the bot"""
        self.schedule_tasks(
            sma_check_interval
        )
        
        print(f"Stock Bot started for {self.symbol}. Monitoring for events...")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Bot stopped manually.")