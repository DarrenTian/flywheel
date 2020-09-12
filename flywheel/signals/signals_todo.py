#price related signals for momentum trading
#all below are closing only

#1. price position(range) ceiling(resistance) and flooring
#e.g. 5,8,10,7,6,9,10,5 -> (5, 10) this should be approximately like ((4-6), (9-11))
#We could also have multiple this so we could have a wilder range of confidence, should be pair with time range
#e.g. ((4-6), (9-11), 8days, 2times reach floor, 2time reach ceil)

#2. ema, this already in the general signals, unit test needed

#3. macd, similar to #2

#4. basic statistals like max/min in a continules trend
#e.g. 5,8,10,7,9,11,8 -> 5, 10, 7, 11, 8

#5. RSI






#volumn related 
#1. total volumn of the trading day, should return list per day

#2. macd of volumn, could reuse the func in signals