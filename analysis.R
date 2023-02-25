require(ggplot2)
require(reshape2)
require(plyr)
require(readr)

noise <- read_csv("./out/noise_profile.csv")
colnames(noise) <- c("sweep", "timestamp", "band_name", "frequency", "signal_level")
# stored in order to make plots work
bandLabels = c("70cm", "1.25m", "2m", "4m", "6m", "10m", "12m", "15m", "17m", "20m", "30m", "40m", "60m", "75m", "80m", "160m") 
noise$band_name = factor(noise$band_name, levels=bandLabels)

# example summary table
#ddply(noise, .(band_name), summarize, min.sig = min(signal_level), med.min.sig = median(signal_level))

# example plot
ggplot(noise) + geom_boxplot(aes(x=as.factor(frequency), y=signal_level)) + facet_wrap(~band_name, ncol=1, scale="free_x") + theme_bw()



