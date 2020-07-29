#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd

DEFICIT_RENAME = {
    'Fiscal Year': 'fiscal_year',
    'Deficit (in billions)': 'deficit', 
    'Debt Increase': 'debt_increase',
    'Deficit/GDP': 'deficit_to_gdp',
    'Events': 'events',
}

FILENAME = 'deficit.csv'

def load_data(filename):
    df = pd.read_csv(filename)
    return df

def process_financial_numbers(df, columns):
    for col in columns:
        temp_col_name = 'tmp_' + col
        df[temp_col_name] = (df[col]
            .str.replace("\(|\)|\$|,", "")
            .astype(float))
        df.loc[df[col].str.contains('(', regex=False), temp_col_name] = df[temp_col_name] * -1

        df[col] = df[temp_col_name]
        df = df.drop(temp_col_name, axis=1)
    return df


def get_deficit_data():
    df = load_data(FILENAME)
    df = df.rename(columns=DEFICIT_RENAME)
    df = process_financial_numbers(df, ['deficit'])
    df = df[~df['fiscal_year'].str.contains('C')]
    df['fiscal_year'] = df['fiscal_year'].astype(int)
    return df


def plot_deficit_data(df):
    fig, ax = plt.subplots()
    ax_font_dict = {
        'fontsize': 8
    }
    presidential_color_mappings = (
        ('1961', '1963', 'blue', 'John F. Kennedy'),
        ('1963', '1969', 'blue', 'Lyndon B. Johnson'),
        ('1969', '1974', 'red', 'Richard Nixon'),
        ('1974', '1977', 'red', 'Gerald Ford'),
        ('1977', '1981', 'blue', 'Jimmy Carter'),
        ('1981', '1989', 'red', 'Ronald Reagan'),
        ('1989', '1993', 'red', 'George H. W. Bush'),
        ('1993', '2001', 'blue', 'Bill Clinton'),
        ('2001', '2009', 'red', 'George W. Bush'),
        ('2009', '2017', 'blue', 'Barack Obama'),
        ('2017', '2021', 'red', 'Donald Trump'),
    )



    ax.plot(df['fiscal_year'].astype(str), df['deficit'])
    ax.set_xticklabels(df['fiscal_year'], fontdict=ax_font_dict, rotation=30)
    [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % 5 != 0]
    ax.set_title('U.S. Deficit by Year')
    ax.set_ylabel("USD in Billions")


    middle_y = ((max(df['deficit']) - min(df['deficit']))/2
                 - (0 - min(df['deficit'])))

    # set colors for presidential terms
    for mapping in presidential_color_mappings:
        ax.axvspan(mapping[0], mapping[1], color=mapping[2], alpha=0.5)
        ax.text(mapping[0], middle_y, "{} ({})".format(mapping[3], mapping[0]), rotation=90)

    plt.subplots_adjust(left=.05, bottom=.05, right=.95, top=.95)
    plt.show()

def main():
    df = get_deficit_data()
    plot_deficit_data(df)


if __name__ == '__main__':
    main()
