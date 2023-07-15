# Dynamic Constant Product Market Maker Using Cryptocurrency Price Prediction Based on Deep Learning 

This project is about Dynamic Constant Product Market Maker that control the price curve following predicted cryptocurrency price based on deep learning.  
<br/>

## :clipboard: Contents
1. [About DCPMM](#🔎-about-project)
2. [Background](#🌱-background)
3. [Tech Stack](#📚-tech-stack)
4. [My Roles](#📝-my-roles)
5. [System Structure](#🏭-system-structure)
6. [Shortcomings](#⭐-shortcomings)
<br/>

## :mag_right: About Project
This project is about Dynamic Constant Product Market Maker that control the price curve following predicted cryptocurrency price based on deep learning. 

This system aims to
* give lower latency and
higher accurate price than using decentralized oracle data feed  
* mitigate impermanent loss and give more profit to liquidity providers  
<br/>

## :seedling: Background  
When I was in graduate school, I participated in developing Delio’s decentralized exchange service. During the project, I studied Decentralized Exchange(DEX) and Constant Product Market Maker(CPMM) algorithm. 

I also enjoyed solving the challenges in the constant product market maker algorithm on impermanent loss and slippage. For my thesis, I studied a novel solution that mitigates the slippage and impermanent loss of the CPMM.

I got an idea from Bhaskar’s paper, 
Dynamic Curves for Decentralized Autonomous Cryptocurrency Exchanges.  
:link: https://arxiv.org/abs/2101.02778  

Bhaskar et all. proposed the concept of dynamic curve-based AMM decentralized exchanges.
The curve is continuously and automatically adjusted to a current pool price equal to a market price. This mechanism requires external market price information with low-latency and accuracy. 

I proposed a dynamic constant product AMM using cryptocurrency price prediction based on deep learning. This system uses deep learning to forecast cryptocurrency prices and adjusts the curve based on the predicted result.

This idea got fund approximately $ 56,000 from AI product/service prduction support
project in Gwangju city.  

While on this project, I studied Atomic Swap and wrote a survey paper. The paper has published to The Institute of Electronics and Information Engineers Conference, on November, 2021.  
:link: https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11027676   

Thesis  
:link: https://heungno.net/wp-content/uploads/2022/08/20201123_Ha-youngPark.pdf 
<br/>

## :books: Tech Stack
<br/>
<p align = "center">
<img src="https://img.shields.io/badge/DeFi-FF8000?style=for-the-badge&logo=&logoColor=white">
<img src="https://img.shields.io/badge/Decentralized Exchange-3C3C3D?style=for-the-badge&logo=&logoColor=white">
<img src="https://img.shields.io/badge/Automated Market Maker-55C500?style=for-the-badge&logo=&logoColor=white"> <br/>  
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Price Prediction-5A0FC8?style=for-the-badge&logo=&logoColor=white">
<img src="https://img.shields.io/badge/LSTM-40B5A4?style=for-the-badge&logo=&logoColor=white"> <br/>    
<img src="https://img.shields.io/badge/Chainlink-375BD2?style=for-the-badge&logo=Chainlink&logoColor=white">  
</p>
<br/>

## :memo: My roles  
* Research
    - Studying Decentralized Exchange, Automated Market Maker(AMM) algorithms, and Atomic Swaps
    - Studying previous literature on solving issues of the CPMM
    - Investigating and analyzing the dynamic curve-based AMM decentralized exchanges
    - Proposing a research idea 
* Cryptocurrency Price Prediction
    - Collecting and optimizing historical cryptocurrency price data  
    - Studying time series data prediction models
    - Making a cryptocurrency price prediction model
* Simulation
    - Conducting simulations experiments on three scenarios
    - Evaluating the performance of the system  
* Etc
    - Writing paper and thesis  
<br/>

## :factory: System Structure
The system consists of Cryptocurrency price prediction, Decentralized oracle, and Dynamic constant product market maker DEX.  

The cryptocurrency price prediction model can be made into an API.  
Decentralized oracle requests the price prediction results to price prediction model API. Then the API responses to the oracle.   
DCPMM DEX deployed on the Ethereum network requests external information to the oracle. Oracle responses to the DEX's request. The DCPMM DEX adjusts the curve refers to predicted price results.  

<p align = "center">
<img src = "images\system-structure.png" width = "600" height = "250">
</p>
<br/>

### Cryptocurrency Price Prediction   
#### Dataset
The cryptocurrency price prediction part makes use of historical cryptocurrency price data. I got BTC/ETH historical price data from Yahoo Finance. Data was collected from the 1st, of January 2020 to the 31st, of December 2021. Total data size is 691 rows. Close price data is used for predicting cryptocurrency prices. The data is split into 491 training sets and 200 test sets. Min-max normalization is used to scale the data in the range [0,1].   

#### Deep learning model
I used Long Short-Term Memory (LSTM) to predict cryptocurrency price. Long Short-Term Memory (LSTM) is a deep learning model with cycle structure makes previous event affect the future event. The model can handle long-term dependencies as well as short-term memory. It is frequently used for time series data such as price and natural language.  

Price prediction model has 2 LSTM layers and 1 Dense layer. I set the window size as 40 which means the model predicts one day using 40 days of previous data. I set batch size as 10, and epochs as 20. Adam
optimizer is used. Mean squared error is used for loss function. In order to assessthe model's performance, we measured the mean squared error, which is 0.0002054, and the mean absolute error, which is 0.0108949. I used Keras deep learning framework to implement price prediction model.

```python
...
model = Sequential()
model.add(LSTM(40, return_sequences = True, input_shape = (40,1)))
model.add(LSTM(64, return_sequences = False))
model.add(Dense(1, activation = 'linear'))
model.compile(loss = 'mse', optimizer = 'adam', metrics = ['mae'])
...
```
<br/>


### Decentralized oracle   
Oracle is system that allows real-world off-chain data to be imported into the blockchain. There are decentralized oracle services such as Chainlink, Band protocol and Witnet. Chainlink decentralized oracle is used to directly transfer predicted price data.  


### Dynamic constant product market maker DEX  
DEX uses smart contracts and Automated Market Maker(AMM). AMM is an algorithm that calculates the cryptocurrency price according to a mathematical formula. It was introduced to a prediction market at first. There were several algorithms including Logarithmic Market Scoring Rule (LMSR) and Liquidity Sensitive LMSR (LS-LMSR). However, these algorithms are not a good model for DEX. Meanwhile Vitalik buterin suggested Constant Product Market Maker (CPMM) for decentralized exchange. 

#### CPMM
CPMM is as follows 
$$𝑥 ∙ 𝑦 = 𝑘$$   
𝑥 and 𝑦 are reserves of each asset. 𝑘 is constant that made by product of x and y. The price of assets is automatically determined according to a ratio of assets balance while maintaining the 𝑘 value. At the beginning of supplying liquidity, pool smart contract is created and assets are stored to the contract. Using this pool, user exchanges their assets.


<p align = "center">
    <img src = "images\cpmm.png" width = "200" height = "200">
<p/> 
<br/>

CPMM has drawbacks called slippage and impermanent loss.  
Slippage occurs when the expected price of assets differs from the actual price of assets. 
Slippage is caused by a change in state as a result of latency between transaction execution and
completion, as well as a lack of liquidity. Slippage results in loss of profit for the trader and front-runner
attack.  
Impermanent loss, also known as divergence loss occurs when a liquidity provider withdraws their assets due to difference in value between when liquidity was provided to the pool and when the assets are simply held. External change in the market value of
assets and the change of pool price cause the difference.   
Trader and liquidity provider may lose their assets because of impermanent loss and slippage. It disturbs users’ participation and activation of the DEX.

#### Dynamic curve based automated market maker

Bhaskar et all. proposed the concept of dynamic curve-based AMM decentralized exchanges.
The price curve is continuously and automatically adjusted to a current pool price equal to a market price.
It utilizes market price input to modify the mathematical relationship between the assets. The pool price does not change if the market price does not change. Thus there are no arbitrage opportunities and impermanent loss. This mechanism requires
an external oracle that provides low-latency and accurate market prices.  

Dynamic constant product curve is as follows
$$𝑤(𝑡) ∙(𝑥(𝑡) − 𝑎(𝑡𝑡)) ∙ 𝑦(𝑡) = 𝑘$$
𝑥(𝑡) and 𝑦(𝑡) are reserves of each token at 𝑡 time. 𝑥(𝑡) and 𝑦(𝑡) is positive. 𝑎(𝑡) is less than 𝑥(𝑡).
𝑤(𝑡) is positive.  
When the market price changes, w(t) and a(t) change in order to ensure that the new market price and the new curve intersects the current liquidity pair.  
<br/>


## :star: Shortcomings
I conducted simulations on three scenarios: when the curve is fixed, when the curve changed according to the actual market price, and when the curve changed according to the predicted price.  

The simulation results show that the changing curve following the market price is better than the fixed price curve but changing curve following the predicted price is worse.  

There are limitations that will be addressed in future works.  
* Our cryptocurrency price prediction model provides daily price prediction data. Additional data should be collected using a web scraper to provide a more sophisticated time unit dataset. 
* I used LSTM which is commonly used for price prediction but has limitations. We can make use of recent findings on processing time series data, such as ARIMA, GRU, and Transformer.  
* Sentimental analysis can be used with historical price data analysis. Social media(Twitter and Reddit) have a significant impact on changes in cryptocurrency prices.  
* Our price prediction model is centralized. It’s not line with the blockchain's decentralization character. In the future, we might make our model decentralized using InterPlanetary FileSystem (IPFS) and computational oracle.


Considering the results of a simulation that used actual market price, if the latest research methods are applied and design of the research is refined, it is certain that our system would be improved.





