import requests
import common.common as common
import datetime
import csv

# 定数を定義
APP_ID = "1039864632497298124"
API_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'
P_API_URL = "https://app.rakuten.co.jp/services/api/Product/Search/20170426"
R_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"
MASTER_FILE_PATH = './master.csv'
OUT_FILE_PATH = './out_data/{export_at}_ranking.txt'

### 商品クラス
class Item_list:
    def __init__(self):
        self.keyword = None
        self.item_lists=[]
        self.product_lists=[]
        self.rank_lists=[]

    def input_word(self):
        self.keyword = input("キーワード入力：")

    def get_data(self,keyword):
        url = API_URL
        payload = {
            'applicationId': APP_ID,
            'keyword': keyword,
        }
        r = requests.get(url, params=payload)
        resp = r.json()
        # print(resp)
        for item in resp["Items"]:
            self.item_lists.append(item["Item"])

    def get_product(self,keyword):
        url = P_API_URL
        payload = {
            'applicationId': APP_ID,
            'keyword': keyword,
        }
        r = requests.get(url, params=payload)
        resp = r.json()
        # print(len(resp["Items"]))
        for product in resp["Products"]:
            self.product_lists.append(product["Product"])

    def get_rank(self):
        url = R_API_URL
        payload = {
            'applicationId': APP_ID,
        }
        r = requests.get(url, params=payload)
        resp = r.json()
        # print(len(resp["Items"]))
        for rank in resp["Items"]:
            self.rank_lists.append(rank["Item"])

    def show_data(self):
        for item in self.item_lists:
            print(f"品名：{item['itemName']}")
            print(f"金額：{item['itemPrice']}円")

    def show_Max_Min(self):
        for item in self.product_lists:
            print(f"商品：{item['productName']}")
            print(f"最大額：{item['maxPrice']}円")
            print(f"最低額：{item['minPrice']}円")

    def show_rank(self):
        for item in self.rank_lists:
            print(f"{item['rank']}位：{item['itemName']}")
            print(f"金額：{item['itemPrice']}円")
    
    def Out_csv_rank(self):
        now = datetime.datetime.now()
        out_file_path = OUT_FILE_PATH.format(export_at=now.strftime('%Y%m%d_%H%M%S'))
        with open(out_file_path, mode='w') as out_file:
            out_data = []
            out_data.append("rank")
            out_data.append("name")
            out_data.append("price")
            out_data.append("URL")
            writer = csv.writer(out_file)
            writer.writerow(out_data)
        for item in self.rank_lists:
            out_data = []
            out_data.append(item['rank'])
            out_data.append(item['itemName'])
            out_data.append(item['itemPrice'])
            out_data.append(item['itemUrl'])
            with open(out_file_path, mode='a') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(out_data)

### メイン処理
def main():
    item_master = Item_list()
    
    # キーワード入力
    item_master.input_word()

    # データ取得
    item_master.get_data(item_master.keyword)
    item_master.get_product(item_master.keyword)
    item_master.get_rank()
    # データ表示
    item_master.show_data()
    item_master.show_Max_Min()
    item_master.Out_csv_rank()

if __name__ == "__main__":
    common.write_log("start")
    main()