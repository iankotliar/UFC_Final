# Project Background & Description:
The sport of Mixed Martial Arts or MMA has grown exponentially in popularity over the past decade, as has the volume of betting on MMA fights. As a result, many people are interested in predicting MMA fight outcomes.

Predicting sports results is both an art and science, as the most accurate predictions tend to combine subjective expert analysis with hard statistics. The relative importance of expert analysis and statistics varies from sport to sport. In baseball, for example, many of the most succesful forecasters have relied heavily on statistical models. The best MMA forecasters, by contrast, have not been known to rely heavily on data. There are two mainy reasons for this. First, most MMA fighters only fight 2 to 4 times a year, which limits the amount of data available. Second, how a fight plays out depends heavily on the particular styles and skillsets of each fighter. MMA fighters employ a diverse range of techniques from striking, wrestling, grappling, and Brazilian Jiu Jitusu to defeat their opponents. This makes it difficult to use a fighter's past performance, often against fighters with different styles and skillsets than their current opponent, to estimate their current chance of victory.  

Given the limited use of data in MMA predictions, I wondered if I could nevertheless find a way to use data science techniques to accurately predict fight outcomes. It occured to me that instead of using information about the fighters as inputs to a prediction model, I could instead use the betting odds offered by sports betting sites, since betting odds have been shown to be excellent predictors of sports results accross a wide variety of sports. This idea led to the data science project stored in this respositoy.

This project consists of several steps:

1. **Web Scraping & Data Munging**
    * I scraped data on betting odds from www.bestfightodds.com, which lists the odds offered by 12 popular betting sites for every UFC fight from 2008 to the present. I also scraped data from wikipedia on the outcomes of all UFC fights in this period. I focused on the UFC because to date it has always been the the most popular MMA promotion. 
    * I then merged the betting odds and fight outcomes data to determine whether each bet was succesful or not. 
2. **Exploratory Data Analysis & Model Selection**
    * I first created some summary statistics and visualizations to better understand the data.
    * I then experimented with several different models which took the betting odds as inputs and returned the probability of a fighter winning as the output. To evalaute model performance, I divided the data into several test-training groups based on time period. Importantly, the time period of the test data was always subsequent to that of the training data. I then selected the best performing model.
3. **Historical Profitability Analysis**
    * Armed with a model for estimating each fighter's chance of winning, I investigated whether I would have been able to make a profit if I only placed bets at the highest odds offered and which I predicted had an expected value above a certain threshold. Because my probability of winning is derived from the betting odds of several sites, this essentially amounts to finding instances where a particular betting site is offering significantly higher odds than the others.
4. **Model Deployment**
    * I wrote code to scrape live betting odds data for upcoming UFC cards on www.bestfightodds.com, estimate and apply the model to predict each fighter's chance of winning, and return the predictions for each fighter's probability of winning and the expected value of each bet.

If you're not familliar with sports betting, you may find it helpful to read the section on bet odds formats, implied probabilities and overround.

# Table of Contents #
[Bet Odds Formats, Implied Probabilities & Overround](#bet-formats-implied-probabilities--overround)

[Historical Profitability Analysis](#historical-profitability-analysis)


## Historical Profitability Analysis

Suppose a bet is offered with decimal odds *d*, the probability of winning is *p*, and you'd like to earn an expected value of at least *r* per dollar staked. This is equivalent to the condition

<img src="https://render.githubusercontent.com/render/math?math=p \ge \frac{1 %2B r}{d}">

Using my model's estimate of *p*, I analyzed how much money I would have made if I only placed bets at the highest odds offered by each site and which met the condition above for different values of *r*, in effect looking for fights where a particular betting site was offering much higher odds relative to other sites. Although requiring a higher value of *r* should lead to a higher expected profit per bet, this also limits the number of bets one can place (since fewer fights will pass the threshold).

## Bet Formats, Implied Probabilities & Overround

### Betting 101

Even if you're unfamiliar with sports betting, chances are you made a small bet with a friend. Perhaps you made a bet where if you win your friend gives you $10 and if you lose you give your friend $10. This kind of bet is simple but is not necessarily fair. Suppose the bet was on whether it was going to rain tomorrow and there's a forecasted 80% chance of rain. Obviously, betting on rain would be the smart move and betting on no-rain would be a dumb move.

The attractiveness of a bet is generally determined by its expected value: the amount of money that would be gained or loss, on average, if the bet were repeated an infinite number of times. A bet is, therefore, considered fair when it has an expected value of 0. In the previous example, a bet on rain would have an expected value of .8($10)+.2(-$10)= $6 whereas a bet on no-rain would have an expected value of .8($-10)+.2($10)= $-6. To make the bet fair, the prospective winnings to the side predicting no-rain would have to be increased and those on the side predicting rain would have to be decreased. The practice of adjusting the payouts to make a bet fair is known as handicapping.

Handicapping is all about odds. Odds, definied mathematically, are the ratio of the probability that an outcome occurs to the probability that it doesn't occur. For example, if there's an 80% chance of rain, then the odds of rain are 80% to 20% or 4 to 1. A little math shows that a bet is fair exactly when the ratio of the prospective winnings to the amount staked equals the odds of losing. The side betting on no-rain will lose with odds of 80% to 20% or 4 to 1, so the bet will be fair if $4 is offered for every $1 staked. If more than this amount (e.g. $5 per $1 staked) is offered then a bet on no-rain would have positive expected value, whereas any amount less than this (e.g. $3 per $1 staked) would have negative expected value. 

So what have we learned? The next time your friend wants to bet you $10 that it'll rain and the forecast is 80%, tell him you'll wager $10 if he wagers at least $40.

### Bet Formats

Different bet formats express the prospective winnings relative to the amount staked in different ways. Because the ratio of the prospective winnings to the amount staked is equal to the odds of losing when a bet is fair, betting quotes are also referred to as odds.

The 3 most common bet formats are American, Decimal and Fractional odds. Below is a real bet from SportsBook on the Aldo vs McGregor fight represented in each format.


Bets          | American Odds | Decimal Odds | Fractional Odds
------------- | ------------- |------------- | -------------
McGregor Wins | +105          | 2.05         | 21/20
Aldo Wins     | -135          | 1.74         | 20/27


* **American Odds**: American odds are always expressed with either a plus or minus sign. When betting on an underdog, a plus sign is used and the number indicates the amount one would win on an $100 stake. When betting on a favorite, a minus sign is used and the number represents the amount one needs to stake to win $100.

  * Here McGregor is the underdog. +105 means that a succesful $100 bet on Mcregor would pay out $105.
  * Here Aldo is the favorite. -135 means that a succesful $135 bet on Aldo would pay out $100.

* **Decimal Odds**: Decimal odds are often preferred because unlike American Odds they are expressed the same way for both underdogs and favorites.  Decimal odds equal the total money that would be returned to you if you win (your winnings plus your original stake) per dollar staked. This definition is also useful because it be can shown that the reciprocal of the decimal odds equals the probability of winning when the bet is fair (i.e. fair-odds probability). If your actual probability of winning is above this value, you'd expect to make money on average whereas if it's below this level you'd expect to lose money. The fair-odds probability can, therefore, be looked at as a breakeven threshold.   

  *  2.05 means a succesful $1 bet on McGregor would earn you (2.05 - 1.00)= $1.05. To expect a profit from your bet, McGregor would need to have at least a 1/2.05 = 49% probability of winning. 
  *  1.74 means a succesful $1 bet on Aldo would earn you (1.74 - 1.00)= $.74. To expect a profit from your bet, Aldo would need to have at least a 1/1.74 = 57% probability of winning. 
  
* **Fractional Odds**: Fractional odds are the ratio of the amount one stands to win over the amount staked. Like decimal odds, they are helpful because they are expressed the same way for both underdogs and favorites. 

  *  A succesful $20 dollar stake on McGregor would earn $21.
  *  A succesful $27 dollar stake on Aldo would earn $20
  
### Overround
In the section on decimal odds, I discussed how the reciprocal of the decimal odds equals the fair-odds probability, the probability of winning at which a bet has 0 expected value. In the example of McGregor versus Aldo, Mcgregor had decimal odds of 2.05, implying that if the bet were fair then McGregor would have a 1/2.05 = 49% chance of victory. Conversely, Aldo's 1.74 odds implied he had a 57% chance of victory if the bet were fair. The astute reader will note if these numbers corresponded to the true probabilities of McGregor and Aldo winning then they would add up to 100%, yet 57% + 49% adds up to 106%.

Why the mismatch? The answer is that these probabilities come from assuming that each bet is fair, but bookmakers are not in the business of offering fair bets. If they did, how would they be able to make a profit? The difference between the sum of the implied probabilities and 100% is known by many different names including the overround, vig or the juice, and can be thought of as the bookmaker's margin. In general, a higher overround implies greater expected profit for the bookmaker and less expected profit for the bettors.

To understand this in greater detail, it's helpful to think about bookmakers' business model. Bookmakers provide a valuable service by connecting individuals who want to bet on opposing sides of an outcome and by guaranteeing that the winners receive their payment. In return for these services, bookmakers generally offer decimal odds lower than (i.e. less favorable than) the fair odds. This is why the fair-odds proabilities, which are the reciprocal of the decimal odds, sum up to more than 100%. This ensures that on average bettors will lose money and the bookmakers will make money. 

Depending on how much money is coming in on either side of the bet, a bookmaker will distribute the amount juice on each side differently, making the odds on each side more or less attractive until they have a sufficiently balanced amount bet on each side. This balance allows the bookmaker to make a profit (or at least avoid a large loss) irrespective of the outcome of the event being bet on. 

While the odds offered by each bookmaker will depend on their particular exposure to each side of the bet, bookmaker odds tend to accurately predict the true probabilities of each outcome. This is because of the interaction between bookmaker's efforts to maintain a balanced book and decentralized supply-and-demand forces from bettors. If a bookmaker's odds for one side of a bet are too favorable relative to its true probability, money will flow into that side of the bet, causing the bookmaker to lower the odds on that side and raise the odds on the other in an effort to re-balance their book. 

Although bookmakers' odds contain valuable information about the likelihood of a fighter winning, the overround makes it difficult to convert them into estimates of each fighter's probability of winning. While the total juice can be observed by adding up the reciprocal of the decimal odds on both sides and seeing how much it is above 100%, it's not possible to infer exactly how the juice is apportioned among each side of the bet. Using the McGregor vs Aldo of 2.05 vs 1.74 odds as an example, if one assumes that all of the juice was applied to McGregor and a bet on Aldo is fair, then McGregor's true probability of winning would be 1 - 1/1.74 = 42%. If on the other hand all the juice were applied to Aldo and a bet on McGregor is fair, then McGregor's true probability of winning is 1/2.05 = 49%. The range from 42% to 49% demonstrates the uncertainty caused by the juice.

Empirical evidence suggests that bookmakers apply overround to both sides of a bet, with a greater portion being applied to the underdog. This is why sports bets on average lose money, and bets on longshots will on average lose even more money than bets on favorites. One commonly used approach for estimating probabilities from decimal odds is to divide the fair-odds probabilities by one plus the total amount of overround. For example, this approach would conclude that McGregor and Aldo will win with probabilities of 49%/106% = 46% and 57%/106% = 54% respecitvely. While this method is simple to calculate, it tends to overestimate the underdog's chance of winning, as it does not fully account for the disproportionate juice applied to the underdog. A number of other approaches have been developed to estimate probabilities from odds that account for this phenomenon. 
