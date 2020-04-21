library("implied")
library("dplyr")
library("readr")

df = read_csv("C:\\Users\\Ian Kotliar\\Documents\\repos\\UFC_Project\\datasets\\straightbetwoutcomeslast7.csv")
columns =  c('5Dimes',
             'BetDSI',
             'BookMaker',
             'SportBet',
             'Bet365',
             'Bovada',
             'Sportsbook',
             'William_H',
             'Pinnacle',
             'SportsInt',
             'BetOnline',
             'Intertops')
columns_f1 = paste(columns, "_f1", sep = "")
columns_f2 = paste(columns, "_f2", sep = "")
methods = c( 'basic', 'bb', 'wpo','or', 'power')
imply <- function (x, method, i) {
    return(tryCatch(implied_probabilities(x, method = method)$probabilities[i], error=function(e) NA))
  }
for (i in seq(1,length(columns_f1))){
  for(j in methods){
    f1 = unlist(apply(df[,c(columns_f1[i], columns_f2[i])], 1,
                      function(x) imply(unname(unlist(x[1:2])), method = j, 1)))
    f2 = unlist(apply(df[,c(columns_f1[i], columns_f2[i])], 1,
                      function(x) imply(unname(unlist(x[1:2])), method = j, 2)))
    df[paste(columns_f1[i],"_prob","_",j, sep ="")] = f1
    df[paste(columns_f2[i],"_prob","_",j, sep ="")] = f2
  }
}

write_csv(df,
          "C:\\Users\\Ian Kotliar\\Documents\\repos\\UFC_Project\\datasets\\straightbetwoutcomeslast7_allprobmethods.csv" )
