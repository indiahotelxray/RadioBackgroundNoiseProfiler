require(ggplot2)
require(reshape2)
require(plyr)
require(readr)

noise <- read_csv("./out/noise_profile.csv")
colnames(noise) <- c("set", "timestamp", "band", "freq", "signal")
# stored in order to make plots work
bandLabels = c("70cm", "1.25m", "2m", "4m", "6m", "10m", "12m", "15m", "17m", "20m", "30m", "40m", "60m", "75m", "80m", "160m") 
noise$band = as.factor(noise$band, value=bandLabels)

# example summary table
ddply(noise, .(band), summarize, min.sig = min(signal), med.min.sig = median(signal))

# example plot
ggplot(noise) + geom_boxplot(aes(x=as.factor(freq), y=signal)) + facet_wrap(~band, ncol=1, scale="free_x")



