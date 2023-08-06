import pandas as pd
import numpy as np

# 用第一种方法筛选采食数据，并记录每种错误的数量


def get_feed_data_filter_1(raw_data):
    # 将数据按照id——enter_time排序
    raw_data = raw_data.sort_values(by=['id', 'enter_time'])
    # 删除每个id的第一条和最后一条数据
    raw_data = raw_data.groupby('id').apply(
        lambda x: x.iloc[1:-1]).reset_index(drop=True)
    # 存储各种错误的数量
    error_num = {}
    error_index = []
    # FIV-low:每次采食量<-20g的数据
    error_num['FIV-low'] = len(
        raw_data[raw_data['feed_amount'] < -20])
    error_index.extend(raw_data[raw_data['feed_amount'] < -20].index)
    # FIV-high:每次采食量>2000g的数据
    error_num['FIV-high'] = len(
        raw_data[raw_data['feed_amount'] > 2000])
    error_index.extend(raw_data[raw_data['feed_amount'] > 2000].index)
    # FIV-0:每次采食量=0的数据
    error_num['FIV-0'] = len(raw_data[raw_data['feed_amount'] == 0])
    error_index.extend(raw_data[raw_data['feed_amount'] == 0].index)
    # OTV-low:每次采食时间<0的数据
    error_num['OTV-low'] = len(
        raw_data[raw_data['feed_time'] < 0])
    error_index.extend(raw_data[raw_data['feed_time'] < 0].index)
    # OTV-high:每次采食时间>3600s的数据
    error_num['OTV-high'] = len(
        raw_data[raw_data['feed_time'] > 3600])
    error_index.extend(raw_data[raw_data['feed_time'] > 3600].index)
    # FRV-High-FIV-low:每次采食率>500g/min且 0g<每次采食量<50g的数据
    error_num['FRV-High-FIV-low'] = len(raw_data[((raw_data['feed_amount'] > 0) & (
        raw_data['feed_amount'] < 50) & (raw_data['feed_time'] < 6))])
    error_index.extend(raw_data[((raw_data['feed_amount'] > 0) & (
        raw_data['feed_amount'] < 50) & (raw_data['feed_time'] < 6))].index)
    # FRV-high-strict:每次采食率>100g/min & 每次采食量≥50g或者每次采食量＜-20g
    error_num['FRV-high-strict'] = len(raw_data[((raw_data['feed_amount'] >= 50) | (
        raw_data['feed_amount'] < -20)) & (raw_data['feed_time'] < (50/(100/60)))])
    error_index.extend(raw_data[((raw_data['feed_amount'] >= 50) | (
        raw_data['feed_amount'] < -20)) & (raw_data['feed_time'] < (50/(100/60)))].index)
    # FRV-high:每次采食率>170g/min & 每次采食量≥50g或者每次采食量＜-20g的数据
    error_num['FRV-high'] = len(raw_data[((raw_data['feed_amount'] >= 50) | (
        raw_data['feed_amount'] < -20)) & (raw_data['feed_time'] < (50/(170/60)))])
    error_index.extend(raw_data[((raw_data['feed_amount'] >= 50) | (
        raw_data['feed_amount'] < -20)) & (raw_data['feed_time'] < (50/(170/60)))].index)
    # FRV-0:每次采食率=0g/min & 采食时间>500s
    error_num['FRV-0'] = len(raw_data[((raw_data['feed_amount']
                                        == 0) & (raw_data['feed_time'] > 500))])
    error_index.extend(raw_data[((raw_data['feed_amount']
                                == 0) & (raw_data['feed_time'] > 500))].index)
    # FRV-low:每次采食率!=0g/min & 采食率<2g/min
    error_num['FRV-low'] = len(raw_data[((raw_data['feed_amount'] != 0) & (
        (raw_data['feed_amount'] / raw_data['feed_time'])*60 < 2))])
    error_index.extend(raw_data[((raw_data['feed_amount'] != 0) & (
        (raw_data['feed_amount'] / raw_data['feed_time'])*60 < 2))].index)
    # all:所有错误的数据
    error_num['all'] = len(raw_data[((raw_data['feed_amount'] < -20) | (raw_data['feed_amount'] > 2000) | (raw_data['feed_amount'] == 0) | (raw_data['feed_time'] < 0) | (raw_data['feed_time'] > 3600) | ((raw_data['feed_amount'] > 0) & (raw_data['feed_amount'] < 50) & (raw_data['feed_time'] < 6))
                                    | ((raw_data['feed_amount'] >= 50) & (raw_data['feed_time'] < 6)) | ((raw_data['feed_amount'] >= 50) & (raw_data['feed_time'] < 6)) | ((raw_data['feed_amount'] == 0) & (raw_data['feed_time'] > 500)) | ((raw_data['feed_amount'] != 0) & (raw_data['feed_time'] < 2)))])
    print(error_num)
    # 返回筛选后的数据
    return raw_data.drop(error_index)

# 用第二种方法筛选采食数据，并记录每种错误的数量


def get_feed_data_filter_2(raw_data):
    # 计算FRV = feed rate value (feed amount / feed time), g/min
    raw_data['FRV'] = raw_data['feed_amount'] / raw_data['feed_time'] * 60
    # 计算FRV的上下限
    FRV_up = raw_data['FRV'].quantile(0.75) + \
        1.5*(raw_data['FRV'].quantile(0.75) -
             raw_data['FRV'].quantile(0.25))
    FRV_down = raw_data['FRV'].quantile(0.25) - \
        1.5*(raw_data['FRV'].quantile(0.75) -
             raw_data['FRV'].quantile(0.25))
    # 计算OTV的上下限
    OTV_up = raw_data['feed_time'].quantile(0.75) + \
        1.5*(raw_data['feed_time'].quantile(0.75) -
             raw_data['feed_time'].quantile(0.25))
    OTV_down = raw_data['feed_time'].quantile(0.25) - \
        1.5*(raw_data['feed_time'].quantile(0.75) -
             raw_data['feed_time'].quantile(0.25))
    # 计算前向体重差 LWD = leading weight difference (weight of following visit − weight of present visit)
    raw_data['LWD'] = raw_data.groupby(
        'id')['weight'].shift(-1) - raw_data['weight']
    # 计算LWD的上下限
    LWD_up = raw_data['LWD'].quantile(0.75) + \
        1.5*(raw_data['LWD'].quantile(0.75) -
             raw_data['LWD'].quantile(0.25))
    LWD_down = raw_data['LWD'].quantile(0.25) - \
        1.5*(raw_data['LWD'].quantile(0.75) -
             raw_data['LWD'].quantile(0.25))
    # 计算后向体重差 FWD = following weight difference (weight of present visit − weight of preceding visit)
    raw_data['FWD'] = raw_data['weight'] - \
        raw_data.groupby('id')['weight'].shift(1)
    # 计算FWD的上下限
    FWD_up = raw_data['FWD'].quantile(0.75) + \
        1.5*(raw_data['FWD'].quantile(0.75) -
             raw_data['FWD'].quantile(0.25))
    FWD_down = raw_data['FWD'].quantile(0.25) - \
        1.5*(raw_data['FWD'].quantile(0.75) -
             raw_data['FWD'].quantile(0.25))
    # 计算前向时间差 LTD = leading time difference (entrance time of following visit − exit time of present visit)
    raw_data['LTD'] = raw_data.groupby(
        'id')['enter_time'].shift(-1) - raw_data['exit_time']
    raw_data['LTD'] = raw_data['LTD'].apply(lambda x: x.total_seconds())
    # 计算LTD的上下限
    LTD_up = raw_data['LTD'].quantile(0.75) + \
        1.5*(raw_data['LTD'].quantile(0.75) -
             raw_data['LTD'].quantile(0.25))
    LTD_down = raw_data['LTD'].quantile(0.25) - \
        1.5*(raw_data['LTD'].quantile(0.75) -
             raw_data['LTD'].quantile(0.25))
    # 计算后向时间差 FTD = following time difference (entrance time of present visit − exit time of preceding visit)
    raw_data['FTD'] = raw_data['enter_time'] - \
        raw_data.groupby('id')['exit_time'].shift(1)
    raw_data['FTD'] = raw_data['FTD'].apply(lambda x: x.total_seconds())
    # 计算FTD的上下限
    FTD_up = raw_data['FTD'].quantile(0.75) + \
        1.5*(raw_data['FTD'].quantile(0.75) -
             raw_data['FTD'].quantile(0.25))
    FTD_down = raw_data['FTD'].quantile(0.25) - \
        1.5*(raw_data['FTD'].quantile(0.75) -
             raw_data['FTD'].quantile(0.25))
    error_num = {}
    error_index = []
    # error1: 所有进出站数据中，每次采食量FIV<-20g的数据
    error1 = raw_data[raw_data['feed_amount'] < -20]
    error_index.extend(error1.index)
    error_num['error1'] = len(error1)
    # error2: 所有进出站数据中，每次采食量FIV>2000g的数据
    error2 = raw_data[raw_data['feed_amount'] > 2000]
    error_index.extend(error2.index)
    error_num['error2'] = len(error2)
    # error3: 采食时间OTV=0的数据中，|FIV|>20g的数据
    error3 = raw_data[(raw_data['feed_time'] == 0) &
                      (abs(raw_data['feed_amount']) > 20)]
    error_index.extend(error3.index)
    error_num['error3'] = len(error3)
    # error4: 所有进出站数据中，采食时间OTV<0s的数据
    error4 = raw_data[raw_data['feed_time'] < 0]
    error_index.extend(error4.index)
    error_num['error4'] = len(error4)
    # error5: 所有进出站数据中，采食时间OTV>OTV_up的数据
    error5 = raw_data[raw_data['feed_time'] > OTV_up]
    error_index.extend(error5.index)
    error_num['error5'] = len(error5)
    # error6: 0g<FIV<50g的数据中，采食速率FRV>500g/min的数据
    error6 = raw_data[(raw_data['feed_amount'] > 0) & (
        raw_data['feed_amount'] < 50) & (raw_data['FRV'] > 500)]
    error_index.extend(error6.index)
    error_num['error6'] = len(error6)
    # error7: FIV>50g的数据中，采食速率FRV>110g/min的数据
    error7 = raw_data[(raw_data['feed_amount'] > 50) & (
        raw_data['FRV'] > 110)]
    error_index.extend(error7.index)
    error_num['error7'] = len(error7)
    # error8: FIV>50g的数据中，采食速率FRV>FRV_up的数据
    error8 = raw_data[(raw_data['feed_amount'] > 50) & (
        raw_data['FRV'] > FRV_up)]
    error_index.extend(error8.index)
    error_num['error8'] = len(error8)
    # error9: FRV=0g/min的数据中，OTV>OTV_up的数据
    error9 = raw_data[(raw_data['feed_amount'] == 0)
                      & (raw_data['feed_time'] > OTV_up)]
    error_index.extend(error9.index)
    error_num['error9'] = len(error9)
    # error10: FRV!=0g/min的数据中，|FRV|<2g/min的数据
    error10 = raw_data[(raw_data['feed_amount'] != 0)
                       & (abs(raw_data['FRV']) < 2)]
    error_index.extend(error10.index)
    error_num['error10'] = len(error10)
    # error11: LWD<LWD_down的数据
    error11 = raw_data[raw_data['LWD'] < LWD_down]
    error_index.extend(error11.index)
    error_num['error11'] = len(error11)
    # error12: LWD>LWD_up的数据
    error12 = raw_data[raw_data['LWD'] > LWD_up]
    error_index.extend(error12.index)
    error_num['error12'] = len(error12)
    # error13: FWD<FWD_down的数据
    error13 = raw_data[raw_data['FWD'] < FWD_down]
    error_index.extend(error13.index)
    error_num['error13'] = len(error13)
    # error14: FWD>FWD_up的数据
    error14 = raw_data[raw_data['FWD'] > FWD_up]
    error_index.extend(error14.index)
    error_num['error14'] = len(error14)
    # error15: LTD<0s的数据
    error15 = raw_data[raw_data['LTD'] < 0]
    error_index.extend(error15.index)
    error_num['error15'] = len(error15)
    # error16: FTD<0s的数据
    error16 = raw_data[raw_data['FTD'] < 0]
    error_index.extend(error16.index)
    error_num['error16'] = len(error16)
    result = raw_data.drop(error_index)
    # all:所有错误的数据
    error_num['all'] = len(raw_data) - len(result)
    return result

# 获得筛选后的体重数据


def get_id_weight(raw_data):
    data = raw_data.copy()
    # 获得每个id的初始体重和最终体重
    fix_weight = data[['id', 'start_weight',
                       'end_weight']].drop_duplicates()
    # 将每个id的初始体重和最终体重存入字典
    start_weight = dict(zip(fix_weight['id'], fix_weight['start_weight']))
    end_weight = dict(zip(fix_weight['id'], fix_weight['end_weight']))

    data['age'] = data['enter_time'] - data['birth_date']
    # 转成日龄
    data['age'] = data['age'].dt.days
    data = data.groupby(['id', 'age']).median()
    data = data.reset_index()[['id', 'age', 'weight']]
    # 按id和date排序
    data = data.sort_values(by=['id', 'age'])

    # # 将每个id的初始体重和最终体重填入
    # data = data.groupby('id').apply(lambda x: replacee(
    #     x, start_weight, end_weight, x.iloc[0]['id']))

    return data

# def replacee(x, srart_weight, end_weight, id):
#     x.iloc[0]['weight'] = srart_weight[id]*1000
#     x.iloc[-1]['weight'] = end_weight[id]*1000
#     return x


def get_id_feed(raw_data):
    data = get_feed_data_filter_2(raw_data)
    data['age'] = data['enter_time'] - data['birth_date']
    # 转成日龄
    data['age'] = data['age'].dt.days

    data = data[['id', 'age', 'feed_amount']]
    data = data.groupby(['id', 'age']).sum()
    data = data.reset_index()[['id', 'age', 'feed_amount']]
    # 按id和date排序
    data = data.sort_values(by=['id', 'age'])
    return data


def get_data(raw_data):
    data = raw_data.copy()
    columns = ['id', 'sex','father', 'mother', 'birth_date',
               'station', 'breed', 'enter_time', 'start_weight', 'end_weight', 'birth_weight', 'birth_litter',
               'litter_size']

    data = data[columns].groupby('id').first().reset_index(drop=False)

    id_weight = get_id_weight(raw_data)

    id_feed = get_id_feed(raw_data)

    final_data = id_feed.merge(id_weight, on=['id', 'age'], how='left')

    final_data = final_data.merge(data, on=['id'], how='left')

    final_data = final_data[columns +
                            ['age', 'feed_amount', 'weight',
                             ]]

    # 按id和date排序
    final_data = final_data.sort_values(by=['id', 'age'])
    # # 删除每个id的第一条和最后一条数据
    # data = data.groupby('id').apply(
    #     lambda x: x.iloc[1:-1]).reset_index(drop=True)

    # 将体重的零值填充为前后5次体重的平均值
    final_data['weight'] = final_data.groupby('id')['weight'].apply(
        lambda x: x.replace(0, np.nan).fillna(method='ffill').fillna(method='bfill'))
    

    # 如果数据所有体重均值 > 1000g，那么将体重单位转换为kg
    if final_data['weight'].mean() > 1000:
        final_data['weight'] = final_data['weight'] / 1000

    # 如果数据所有采食均值 > 150g，那么将采食单位转换为kg
    if final_data['feed_amount'].mean() > 150:
        final_data['feed_amount'] = final_data['feed_amount'] / 1000

    return final_data
