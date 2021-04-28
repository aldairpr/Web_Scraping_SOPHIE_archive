import argparse
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(filename):
    logger.info('Starting cleaning process')

    df = _read_data(filename)
    df = _change_data_type(df)
    df = _order_days(df)
    RV, err_RV = _get_RV__err_RV(df)
    df = _create_columns(df, RV, err_RV)
    df = _change_data_type_RV_err_RV(df)
    df = _filter_data(df)
    _save_data(df, filename)

    return df


def _read_data(filename):
    logger.info('Reading file {}'.format(filename))

    return pd.read_csv(filename, sep=';')


def _change_data_type(df):
    logger.info('Change data type')

    df['dates'] = df['dates'].astype('datetime64')
    df['fibers'] = df['fibers'].astype('str')
    df['radial_velocity'] = df['radial_velocity'].astype('str')
    df['JD'] = df['julian_day'].astype('float64')
    return df


def _order_days(df):
    logger.info('Order by dates')
    
    df = df.sort_values(by='dates', ascending=True)
    df = df.reset_index(drop=True)
    return df


def _get_RV__err_RV(df):
    logger.info('Get RV and err_RV from column radial_velocity')
    
    separate_data = (df.apply(lambda row: row['radial_velocity'] + '±', axis=1)
                        .apply(lambda separate: separate.split('±'))
                        .apply(lambda numbers: list(map(lambda number: number.replace(' ', ''), numbers)))
                    )

    RV = []
    for i in range(0,len(df)):
        if len(separate_data[i][0]) != 0:
            RV.append(separate_data[i][0])
        elif len(separate_data[i][0]) == 0:
            RV.append(None)

    err_RV = []
    for i in range(0,len(df)):
        if len(separate_data[i][1]) != 0:
            err_RV.append(separate_data[i][1])
        elif len(separate_data[i][1]) == 0:
            err_RV.append(None)
    
    return RV, err_RV


def _create_columns(df, RV, err_RV):
    logger.info('Create the columns RV and err_RV in the DataFrame')

    df = df.drop('radial_velocity', axis=1)
    df['RV'] = RV
    df['err_RV'] = err_RV

    return df


def _change_data_type_RV_err_RV(df):
    logger.info('Change data type of RV and err_RV')
    
    df['RV'] = df['RV'].astype('float64')
    df['err_RV'] = df['err_RV'].astype('float64')
    df = df.dropna().reset_index(drop=True)
    
    return df


def _filter_data(df):
    logger.info('Data required for the final dataframe')

    # fibers = WAVE
    df = df[df['fibers'] =='WAVE']
    # sns > 70
    df = df[df['signal_to_noise'] > 70]
    # err_RV < 0.0009
    df = df[df['err_RV'] < 0.0009]

    return df


def _save_data(df, filename):
    clean_filename = 'clean_{}'.format(filename)
    logger.info('Saving data: {}'.format(clean_filename))
    df.to_csv(clean_filename, encoding = 'utf-8-sig', sep=';', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='The path to the dirty data',
                        type=str)

    args = parser.parse_args()

    df = main(args.filename)