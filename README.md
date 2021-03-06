# Storytelling_Data_Visualization_on_Exchange_Rates

authors:
[Júlia Guardiani](https://www.linkedin.com/in/juliaguardiani/) e
[Víctor Kaillo](https://www.linkedin.com/in/victorkaillo/)


date:
Nov. 2021

course: [Machine Learning Based Systems Design](https://github.com/ivanovitchm/mlops)

master: [Ivanovitch Medeiros Dantas da Silva](https://github.com/ivanovitchm)

## Our project is an extension of the guided project [Guided Project: Storytelling Data Visualization on Exchange Rates](https://app.dataquest.io/c/96/m/529/guided-project%3A-storytelling-data-visualization-on-exchange-rates/1/introducing-the-dataset) provided by [Dataquest](dataquest.io).
#### Throughout this project we seek to explore and explain the dataset: [Daily Exchange Rates per Euro 1999-2021](https://www.kaggle.com/lsind18/euro-exchange-daily-rates-19992020) through data visualization
###### The data source is the European Central Bank. Dataset contains date and Euro rate corresponding to Argentine peso, Australian dollar, Bulgarian lev, Brazilian real, Canadian dollar, Swiss franc, Chinese yuan renminbi, Cypriot pound, Czech koruna, Danish krone, Algerian dinar, Estonian kroon, UK pound sterling, Greek drachma, Hong Kong dollar, Croatian kuna, Hungarian forint, Indonesian rupiah, Israeli shekel, Indian rupee, Iceland krona, Japanese yen, Korean won, Lithuanian litas, Latvian lats, Moroccan dirham, Maltese lira, Mexican peso, Malaysian ringgit, Norwegian krone, New Zealand dollar, Philippine peso, Polish zloty, Romanian leu, Russian rouble, Swedish krona, Singapore dollar, Slovenian tolar, Slovak koruna, Thai baht, Turkish lira, New Taiwan dollar, US dollar, South African rand.

### First step: clean the code

- We changed the names of the columns of interest to something easier to type. For example, we rename the [US dollar ] and Period\Unit: columns to something easier to type — US_dollar and Time.
- We discarded the columns that were not interesting. Only Euro, Brazilian real and US dollar were used by us.
- We change the Time column to a datetime data type. 
- We sort the values by Time in ascending order
~~~ python
exchange_rates.rename(columns={'[US dollar ]': 'US_dollar',
                               'Period\\Unit:': 'Time'},
                      inplace=True)
exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)
exchange_rates.reset_index(drop=True, inplace=True)
euro_to_dollar = exchange_rates[['Time', 'US_dollar']].copy()
euro_to_dollar['US_dollar'].value_counts() 
euro_to_dollar = euro_to_dollar[euro_to_dollar['US_dollar'] != '-']
euro_to_dollar['US_dollar'] = euro_to_dollar['US_dollar'].astype(float)
~~~

### Second step: data visualization

- We generated a line plot to visualize the evolution of the euro-dollar exchange rate and of the euro-real-dollar exchange rate.
- We used the rolling mean technique to smooth the graph curve  
<img width="431" alt="Captura de Tela 2021-11-28 às 19 30 00" src="https://user-images.githubusercontent.com/27768375/143788718-9e85a6a6-0b78-43e8-80cd-96d9fc81a4db.png">

- We show how the euro-dollar rate changed during the 2007-2008's financial crisis.

<img width="541" alt="Captura de Tela 2021-11-28 às 19 39 14" src="https://user-images.githubusercontent.com/27768375/143789096-393a91ee-248f-4185-ae68-42129224a8d1.png">

- Note: At this point our extension begins. In the original guided project there is no analysis for the period of President Biden's government
- We show comparatively how the euro-dollar rate changed under the last four US presidents (George W. Bush (2001-2009), Barack Obama (2009-2017), Donald Trump (2017-2020) and Joe Biden(2021)). We can use a line plot. See the code we use to prepare the dataset for this use:
~~~ python
bush_obama_trump_biden = euro_to_dollar.copy(
                   )[(euro_to_dollar['Time'].dt.year >= 2001) & (euro_to_dollar['Time'].dt.year <= 2021)]
bush = bush_obama_trump_biden.copy(
       )[bush_obama_trump_biden['Time'].dt.year < 2009]
obama = bush_obama_trump_biden.copy(
       )[(bush_obama_trump_biden['Time'].dt.year >= 2009) & (bush_obama_trump_biden['Time'].dt.year < 2017)]
trump = bush_obama_trump_biden.copy(
       )[(bush_obama_trump_biden['Time'].dt.year >= 2017) & (bush_obama_trump_biden['Time'].dt.year < 2021)]
biden = bush_obama_trump_biden.copy(
       )[(bush_obama_trump_biden['Time'].dt.year == 2021)]
~~~

<img width="792" alt="Captura de Tela 2021-11-28 às 19 49 43" src="https://user-images.githubusercontent.com/27768375/143789461-d73e5147-73af-472a-83f9-f3603e77e786.png">

- Note: more extensions, in the original guided project there is no Brazilian real case study.
- We show how the euro-dollar rate has changed over the last 20 years. See the code we use to prepare the dataset for this use:

~~~ python
exchange_rates.rename(columns={'[Brazilian real ]': 'BRL_real'}, inplace=True) # padronizando para trabalhar com os dados
euro_to_dollar_to_real = euro_to_dollar.copy()
euro_to_dollar_to_real['BRL_real'] = exchange_rates['BRL_real']
euro_to_dollar_to_real['BRL_real'] = exchange_rates['BRL_real']
euro_to_dollar_to_real = euro_to_dollar_to_real[euro_to_dollar_to_real['BRL_real'] != '-']
euro_to_dollar_to_real['BRL_real'] = euro_to_dollar_to_real['BRL_real'].astype(float)
#Taxa de cambio do Euro e do dólar, agora em relação ao Real brasileiro
brl_to_euro_to_dollar = euro_to_dollar_to_real[['Time', 'BRL_real']].copy()
brl_to_euro_to_dollar.rename(columns={'BRL_real': 'euro_rate'}, inplace=True)
brl_to_euro_to_dollar['dollar_rate'] = euro_to_dollar_to_real['BRL_real']/euro_to_dollar_to_real['US_dollar']

~~~

<center>
  
  ![BRL-USD rate](https://user-images.githubusercontent.com/27768375/143790094-884e48b5-4741-40cd-8b87-3f80579524cc.jpeg)

</center>

- We show comparatively how the euro-real-dollar rate changed under the last five Brazil presidents (FHC (2000-2002), Lula (2003-2010), Dilma Rousseff (2011-2016), Michel Temer (2016-2018) and Jair M. Bosonaro(2019-2021)). We can use a line plot. See the code we use to prepare the dataset for this use:
 
~~~ python
brl_to_euro_to_dollar['dollar_rolling_mean'] = brl_to_euro_to_dollar['dollar_rate'].rolling(50).mean()
brl_to_euro_to_dollar['euro_rolling_mean'] = brl_to_euro_to_dollar['euro_rate'].rolling(50).mean()
todos_presidentes = brl_to_euro_to_dollar.copy(
                   )[(brl_to_euro_to_dollar['Time'].dt.year >= 2000) & (brl_to_euro_to_dollar['Time'].dt.year < 2021)]
fhc = todos_presidentes.copy(
       )[todos_presidentes['Time'].dt.year < 2002]
lula = todos_presidentes.copy(
       )[(todos_presidentes['Time'].dt.year >= 2002) & (todos_presidentes['Time'].dt.year < 2010)]
dilma = todos_presidentes.copy(
       )[(todos_presidentes['Time'].dt.year >= 2010) & ((todos_presidentes['Time'].dt.year < 2017) & (todos_presidentes['Time'].dt.month < 9))]
temer = todos_presidentes.copy(
       )[((todos_presidentes['Time'].dt.year >= 2016) & (todos_presidentes['Time'].dt.month >= 9))  & (todos_presidentes['Time'].dt.year < 2019)]
jair = todos_presidentes.copy(
       )[(todos_presidentes['Time'].dt.year >= 2019)  & (todos_presidentes['Time'].dt.year < 2022)]
# presidentes = [fhc, lula, dilma, temer, bozo]
# anos = [2000,2001,2002.2003,2004,2005,2006,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
~~~
 
<center>

  ![BRL-USD rate under the last 5 Brazilian presidents](https://user-images.githubusercontent.com/27768375/143790044-d367f635-8921-4e40-b634-a3d14d6d9a0d.jpeg)

</center>

### Based on the production ready code methods provided in [Production_Ready_Code.ipynb](https://github.com/ivanovitchm/mlops/blob/main/week_04/Production_Ready_Code.ipynb), we made use of try and except to avoid breaks in code execution due to misuse in data manipulation.
