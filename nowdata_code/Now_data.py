import pandas as pd
import glob
import json


def now_data_merge():
    path = './data/now_waiting/'
    files = glob.glob(path + "/*.json")
    li = []

    for file in files:
        with open(file, 'r', encoding='utf-8-sig') as file:
            x = json.load(file)
        df = pd.DataFrame(x)
        li.append(df)
    now_waiting = pd.concat(li, axis=0, ignore_index=True)

    target = pd.read_csv('./data/baemin/Accumulated_data.csv')

    cols = ['id', 'source_type', 'serving_type', 'amount', 'amount_to_pay', 'user_comment']
    df = now_waiting[cols]
    df = df.rename(columns={'id': '주문번호',
                            'source_type': '서비스타입',
                            'serving_type': '결제방법',
                            'amount': '주문금액',
                            'amount_to_pay': '결제금액',
                            'user_comment': '요청사항'})

    import datetime

    def get_timestamps(timestamp_list):
        if timestamp_list.get('completed') is None:
            return
        registered_ts = timestamp_list.get('registered') / 1000
        registered_dt = datetime.datetime.fromtimestamp(int(registered_ts)).strftime('%Y-%m-%d %H:%M:%S')

        return pd.Series((registered_dt))

    def get_order_details(orders):
        if orders['status'] != 'completed':
            return
        all_orders = []
        i = -1
        order_list = orders['order_items']
        for item in order_list:
            quantity = item['quantity']
            # item w/o Parent ID (main)
            if item['parent_order_item_id'] == None:
                order = {}.fromkeys(['order_id', 'main', 'method', 'dressings', 'toppings'], '')
                order['order_id'] = item['id']
                if '샐러드' in item['name']:
                    order['main'] = [item['name']] if quantity == 1 else [item['name'] for _ in range(quantity)]

                all_orders.append(order)
                i += 1
                dressings = []
                toppings = []

            # item w Parent ID
            else:
                order_i = all_orders[i]
                if item['parent_order_item_id'] == order_i['order_id']:
                    content = item['content'].lower().split(':')[0]
                    name = item['name'].replace('추가', '').replace('-', '').replace(' ', '').replace('(',
                                                                                                    '').replace(')',
                                                                                                                '')
                    if '수령방식' in content:
                        order_i['method'] = name
                    elif ('소스선택' in content) or ('드레싱' in content):
                        for _ in range(quantity):
                            dressings.append(name)
                    elif '메인' in content:
                        for _ in range(quantity):
                            toppings.append(name)
                    elif '제외' in content:
                        pass

                    else:
                        if ('고구마' in name) and ('g' in name):
                            grams = int(''.join(filter(str.isdigit, name)))
                            if grams == 100:
                                quantity *= 2
                                name = name.replace('100', '50')
                        elif '계란' in name:
                            name = '삶은달걀'
                        for _ in range(quantity):
                            toppings.append(name)
                    order_i['dressings'] = dressings
                    order_i['toppings'] = toppings

                # 다음 Parent ID 로 넘어감
                else:
                    print('순서 이상')
                    return False
        method_list = []
        items_list = []
        toppings_list = []
        sauce_list = []

        for _ in range(len(all_orders)):
            if len(all_orders[_]['main']) == 0 and len(all_orders[_]['dressings']) != 0:
                sauce_list.extend(all_orders[_]['dressings'])
            for k in range(len(all_orders[_]['main'])):
                method_list.append(all_orders[_]['method'])
                toppings_list.extend(all_orders[_]['toppings'])
                sauce_list.extend(all_orders[_]['dressings'])
            items_list.extend(all_orders[_]['main'])

        method = (', ').join(method_list)
        items = (', ').join(items_list)
        toppings = (', ').join(toppings_list)
        sauce = (', ').join(sauce_list)
        return pd.Series((method, items, toppings, sauce))


    df[['수령방법', '항목', '추가선택', '드레싱']] = now_waiting.apply(lambda row: pd.Series(get_order_details(row)),
                                                          axis=1)
    df[['주문시각']] = now_waiting.apply(lambda row: pd.Series(get_timestamps(row['timestamps'])), axis=1)
    target_cols = target.columns
    df['주소'] = 'X'
    df['배달팁'] = 0
    df.loc[df['서비스타입'] == 'from_kakao', '서비스타입'] = '챗봇'
    df.loc[df['서비스타입'] == 'from_kiosk', '서비스타입'] = '나우웨이팅 POS'
    df.loc[df['서비스타입'] == 'from_nw_pos', '서비스타입'] = '현금'
    df['접수시각'] = None
    df['배달시각'] = None
    df['배달요청사항'] = None
    df['실제배달료'] = None
    df = df[target_cols]
    df = df.dropna(subset=['주문시각'])
    with open('./data/baemin/Accumulated_data.csv', 'a') as old_file:
        df.to_csv('./data/now_waiting/Accumulated_data.csv', index=False, encoding='utf-8-sig')