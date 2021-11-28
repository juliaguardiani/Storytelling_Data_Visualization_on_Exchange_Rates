"""
ALUNA: JÚLIA NEVES GUARDIANI
PROFESSOR: IVANOVITCH MEDEIROS DANTAS DA SILVA
DATA: NOVEMBRO 2021
"""
# Importações necessárias.
import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

# Estilo para das figuras exportadas.
style.use('fivethirtyeight')

logging.basicConfig( # Arquivo de log para as operações do projeto.
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)


class DataStoryTeller:
    """
    Classe com leitura dos dados para executar o data storytelling.
    """
    file_path = 'euro-daily-hist_1999_2020.csv'
    # !!! DESCOMENTAR PARA RODAR !!!
    #file_path =
    #'https://raw.githubusercontent.com/juliaguardiani/
    # Storytelling_Data_Visualization_on_Exchange_Rates/main/euro-daily-hist_1999_2020.csv'

    def __init__(self):
        """
        Construtor da classe com os principais atributos.
        """
        self.exchange_rates = pd.DataFrame()
        self.brl_to_euro_to_dollar = pd.DataFrame()
        self.fhc = pd.DataFrame()
        self.lula = pd.DataFrame()
        self.dilma = pd.DataFrame()
        self.temer = pd.DataFrame()
        self.jair = pd.DataFrame()

    def read_data(self) -> None:
        """
         Preenche o atributo da classe exchange_rates
        """
        try:
            self.exchange_rates = pd.read_csv(self.file_path)
            logging.info(
                self.exchange_rates.shape[0]
            )
        except FileNotFoundError:
            print(f'There is no such  {self.file_path}')
            logging.error('Erro: Não foi possível encontrar este arquivo')

    def data_cleaning(self) -> None:
        """
        1)Renomeação
        2)agrupamento
        3)segregação dos dados
        """
        self.exchange_rates.rename(columns={'[US dollar ]': 'US_dollar',
                                            'Period\\Unit:': 'Time'},
                                   inplace=True)
        self.exchange_rates['Time'] = pd.to_datetime(self.exchange_rates['Time'])
        self.exchange_rates.sort_values('Time', inplace=True)
        self.exchange_rates.reset_index(drop=True, inplace=True)
        self.exchange_rates.rename(columns={'[Brazilian real ]': 'BRL_real'}, inplace=True)

        euro_to_dollar = self.exchange_rates[['Time', 'US_dollar']].copy()
        euro_to_dollar = euro_to_dollar[euro_to_dollar['US_dollar'] != '-']
        euro_to_dollar['US_dollar'] = euro_to_dollar['US_dollar'].astype(float)

        euro_to_dollar_to_real = euro_to_dollar.copy()
        euro_to_dollar_to_real['BRL_real'] = self.exchange_rates['BRL_real']
        euro_to_dollar_to_real = euro_to_dollar_to_real[euro_to_dollar_to_real['BRL_real'] != '-']
        euro_to_dollar_to_real['BRL_real'] = euro_to_dollar_to_real['BRL_real'].astype(float)

        self.brl_to_euro_to_dollar = euro_to_dollar_to_real[['Time', 'BRL_real']].copy()
        self.brl_to_euro_to_dollar.rename(columns={'BRL_real': 'euro_rate'}, inplace=True)
        self.brl_to_euro_to_dollar['dollar_rate'] = \
            euro_to_dollar_to_real['BRL_real'] / euro_to_dollar_to_real['US_dollar']
        self.brl_to_euro_to_dollar['dollar_rolling_mean'] = \
            self.brl_to_euro_to_dollar['dollar_rate'].rolling(50).mean()
        self.brl_to_euro_to_dollar['euro_rolling_mean'] = \
            self.brl_to_euro_to_dollar['euro_rate'].rolling(50).mean()

        todos_presidentes = self.brl_to_euro_to_dollar.copy()[
            (self.brl_to_euro_to_dollar['Time'].dt.year >= 2000) &
            (self.brl_to_euro_to_dollar['Time'].dt.year < 2021)
            ]
        self.fhc = todos_presidentes.copy()[todos_presidentes['Time'].dt.year < 2002]
        self.lula = todos_presidentes.copy()[
            (todos_presidentes['Time'].dt.year >= 2002) &
            (todos_presidentes['Time'].dt.year < 2010)
            ]
        self.dilma = todos_presidentes.copy()[
            (todos_presidentes['Time'].dt.year >= 2010) &
            ((todos_presidentes['Time'].dt.year < 2017) &
             (todos_presidentes['Time'].dt.month < 9))
            ]
        self.temer = todos_presidentes.copy()[
            ((todos_presidentes['Time'].dt.year >= 2016) &
             (todos_presidentes['Time'].dt.month >= 9)) &
            (todos_presidentes['Time'].dt.year < 2019)
            ]
        self.jair = todos_presidentes.copy()[
            (todos_presidentes['Time'].dt.year >= 2019) &
            (todos_presidentes['Time'].dt.year < 2022)
            ]

    def dollar_real_storytelling(self) -> None:
        """
        Real X Dólar em relação a cada presidente do Brasil.
        """
        plt.figure(figsize=(12, 8))
        plt.subplots_adjust(top=0.9)
        plt.tight_layout()

        # Adding the subplots
        ax1_fhc = plt.subplot(2, 5, 1)
        ax2_lula = plt.subplot(2, 5, 2)
        ax3_dilma = plt.subplot(2, 5, 3)
        ax4_temer = plt.subplot(2, 5, 4)
        ax5_jair = plt.subplot(2, 5, 5)

        ax6_resultado = plt.subplot(2, 1, 2)
        axes = [ax1_fhc, ax2_lula, ax3_dilma, ax4_temer, ax5_jair, ax6_resultado]

        for axis in axes:
            axis.set_ylim(0.8, 1.7)
            axis.set_yticks([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0])
            axis.set_yticklabels(
                ['1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5', '5.5', '6'],
                alpha=0.3
            )
            axis.grid(alpha=0.5)

        # Ax1
        ax1_fhc.plot(self.fhc['Time'], self.fhc['dollar_rolling_mean'],
                     color='#BF5FFF')
        ax1_fhc.set_xticklabels(['2000', '', '', '2001', '', '', '2002'],
                                alpha=0.3)
        ax1_fhc.text(11000, 7.0, 'FHC', fontsize=18, weight='bold',
                     color='#BF5FFF')
        ax1_fhc.text(11000, 6.5, '(2000-2002)', weight='bold',
                     alpha=0.3)

        # Ax2
        ax2_lula.plot(self.lula['Time'], self.lula['dollar_rolling_mean'],
                      color='#ffa500')
        ax2_lula.set_xticklabels(['', '2003', '', '', '', '2007', '', '', '', '2011'],
                                 alpha=0.3)
        ax2_lula.text(11300, 7.0, 'LULA', fontsize=18, weight='bold',
                      color='#ffa500')
        ax2_lula.text(11300, 6.5, '(2003-2010)', weight='bold',
                      alpha=0.3)

        # Ax3
        ax3_dilma.plot(self.dilma['Time'], self.dilma['dollar_rolling_mean'],
                       color='#00B2EE')
        ax3_dilma.set_xticklabels(['', '2012', '', '', '2014', '', '',
                                   '2016'],
                                  alpha=0.3)
        ax3_dilma.text(14500, 7.0, 'DILMA', fontsize=18, weight='bold',
                       color='#00B2EE')
        ax3_dilma.text(14500, 6.5, '(2011-2016)', weight='bold',
                       alpha=0.3)

        # Ax4
        ax4_temer.plot(self.temer['Time'], self.temer['dollar_rolling_mean'],
                       color='#b83333')
        ax4_temer.set_xticklabels(['', '2016', '', '', '2017', '', '', '2018'],
                                  alpha=0.3)
        ax4_temer.text(17000, 7.0, 'TEMER', fontsize=18, weight='bold',
                       color='#b83333')
        ax4_temer.text(17000, 6.5, '(2016-2018)', weight='bold',
                       alpha=0.3)

        # Ax5
        ax5_jair.plot(self.jair['Time'], self.jair['dollar_rolling_mean'],
                      color='#664710')
        ax5_jair.set_xticklabels(['', '2019', '', '', '2020', '', '', '2021'],
                                 alpha=0.3)
        ax5_jair.text(17800, 7.0, 'BOLSO', fontsize=18, weight='bold', color='#664710')
        ax5_jair.text(17800, 6.5, '(2019-2021)', weight='bold', alpha=0.3)

        # Ax4
        ax6_resultado.plot(self.fhc['Time'], self.fhc['dollar_rolling_mean'],
                       color='#BF5FFF')
        ax6_resultado.plot(self.lula['Time'], self.lula['dollar_rolling_mean'],
                       color='#ffa500')
        ax6_resultado.plot(self.dilma['Time'], self.dilma['dollar_rolling_mean'],
                       color='#00B2EE')
        ax6_resultado.plot(self.temer['Time'], self.temer['dollar_rolling_mean'],
                       color='#b83333')
        ax6_resultado.plot(self.jair['Time'], self.jair['dollar_rolling_mean'],
                       color='#664710')
        ax6_resultado.grid(alpha=0.5)
        ax6_resultado.set_xticks([])

        # Adding a title and a subtitle
        ax1_fhc.text(
            11000,
            9,
            'BRL-USD rate under the last 5 Brazilian presidents',
            fontsize=20,
            weight='bold'
        )
        ax1_fhc.text(
            11000,
            8.4,
            'Taxa de câmbio real-dolar entre os anos 2000 e 2020',
            fontsize=16
        )
        # Adding a signature
        ax6_resultado.text(
            10300,
            0.65,
            'Source: European Central Bank',
            color='#f0f0f0',
            backgroundcolor='#4d4d4d',
            size=14
        )
 
    def euro_real_storytelling(self):
        """
        Real X Euro em relação a cada presidente do Brasil.
        """
        plt.figure(figsize=(12, 8))
        plt.subplots_adjust(top=0.9)
        plt.tight_layout()
        # Adding the subplots
        ax1_fhc = plt.subplot(2, 5, 1)
        ax2_lula = plt.subplot(2, 5, 2)
        ax3_dilma = plt.subplot(2, 5, 3)
        ax4_temer = plt.subplot(2, 5, 4)
        ax5_jair = plt.subplot(2, 5, 5)

        ax6_resultado = plt.subplot(2, 1, 2)
        axes = [ax1_fhc, ax2_lula, ax3_dilma, ax4_temer, ax5_jair, ax6_resultado]

        # Changes to all the subplots
        for axis in axes:
            axis.set_ylim(0.8, 1.7)
            axis.set_yticks([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0])
            axis.set_yticklabels(
                ['1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5', '5.5', '6.0', '6.5', '7.0'],
                alpha=0.3
            )
            axis.grid(alpha=0.5)

        # Ax1
        ax1_fhc.plot(self.fhc['Time'], self.fhc['euro_rolling_mean'],
                     color='#BF5FFF')
        ax1_fhc.set_xticklabels(['2000', '', '', '2001', '', '', '2002'],
                                alpha=0.3)
        ax1_fhc.text(11000, 7.7, 'FHC', fontsize=18, weight='bold',
                     color='#BF5FFF')
        ax1_fhc.text(11000, 7.2, '(2000-2002)', weight='bold',
                     alpha=0.3)

        # Ax2
        ax2_lula.plot(self.lula['Time'], self.lula['euro_rolling_mean'],
                      color='#ffa500')
        ax2_lula.set_xticklabels(['', '2003', '', '', '', '2007', '', '', '', '2011'],
                                 alpha=0.3)
        ax2_lula.text(11300, 7.7, 'LULA', fontsize=18, weight='bold',
                      color='#ffa500')
        ax2_lula.text(11300, 7.2, '(2003-2010)', weight='bold',
                      alpha=0.3)

        # Ax3
        ax3_dilma.plot(self.dilma['Time'], self.dilma['euro_rolling_mean'],
                       color='#00B2EE')
        ax3_dilma.set_xticklabels(['', '2012', '', '', '2014', '', '',
                                   '2016'],
                                  alpha=0.3)
        ax3_dilma.text(14500, 7.7, 'DILMA', fontsize=18, weight='bold',
                       color='#00B2EE')
        ax3_dilma.text(14500, 7.2, '(2011-2016)', weight='bold',
                       alpha=0.3)

        # Ax4
        ax4_temer.plot(self.temer['Time'], self.temer['euro_rolling_mean'],
                       color='#b83333')
        ax4_temer.set_xticklabels(['', '2016', '', '', '2017', '', '', '2018'],
                                  alpha=0.3)
        ax4_temer.text(17000, 7.7, 'TEMER', fontsize=18, weight='bold',
                       color='#b83333')
        ax4_temer.text(17000, 7.2, '(2016-2018)', weight='bold',
                       alpha=0.3)

        # Ax5
        ax5_jair.plot(self.jair['Time'], self.jair['euro_rolling_mean'],
                      color='#664710')
        ax5_jair.set_xticklabels(['', '2019', '', '', '2020', '', '', '2021'],
                                 alpha=0.3)
        ax5_jair.text(17800, 7.7, 'BOLSO', fontsize=18, weight='bold', color='#664710')
        ax5_jair.text(17800, 7.2, '(2019-2021)', weight='bold', alpha=0.3)

        # Ax4
        ax6_resultado.plot(self.fhc['Time'], self.fhc['euro_rolling_mean'],
                       color='#BF5FFF')
        ax6_resultado.plot(self.lula['Time'], self.lula['euro_rolling_mean'],
                       color='#ffa500')
        ax6_resultado.plot(self.dilma['Time'], self.dilma['euro_rolling_mean'],
                       color='#00B2EE')
        ax6_resultado.plot(self.temer['Time'], self.temer['euro_rolling_mean'],
                       color='#b83333')
        ax6_resultado.plot(self.jair['Time'], self.jair['euro_rolling_mean'],
                       color='#664710')
        ax6_resultado.grid(alpha=0.5)
        ax6_resultado.set_xticks([])

        # Adding a title and a subtitle
        ax1_fhc.text(
            11000,
            9.5,
            'BRL-EUR rate under the last 5 Brazilian presidents',
            fontsize=20,
            weight='bold'
        )
        ax1_fhc.text(
            11000,
            8.8,
            'Taxa de câmbio real-euro entre os anos 2000 e 2020',
            fontsize=16
        )
        # Adding a signature
        ax6_resultado.text(
            10350,
            0.35,
            'Source: European Central Bank',
            color='#f0f0f0',
            backgroundcolor='#4d4d4d',
            size=14
        )

if __name__ == '__main__':
    data_story_teller = DataStoryTeller()
    data_story_teller.read_data()
    data_story_teller.data_cleaning()
    data_story_teller.dollar_real_storytelling()
    data_story_teller.euro_real_storytelling()
