import os
import requests
import datetime
import csv
from common.spread_sheet_manager import SpreadsheetManager
from dotenv import load_dotenv
load_dotenv() #環境変数のロード

# 定数を定義
APP_ID = "1039864632497298124"
API_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'
P_API_URL = "https://app.rakuten.co.jp/services/api/Product/Search/20170426"
R_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"
MASTER_FILE_PATH = './master.csv'
OUT_FILE_PATH = './out_data/{export_at}_ranking.csv'
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]

### 商品クラス
class Item_list:
    def __init__(self):
        self.item_lists=[]

    def get_data(self,url,keyword,columns_name,colum_name):
        self.item_lists=[]
        payload = {
            'applicationId': APP_ID,
            'keyword': keyword,
        }
        r = requests.get(url, params=payload)
        resp = r.json()
        # print(resp)
        if columns_name in resp:
            for item in resp[columns_name]:
                self.item_lists.append(item[colum_name])

        return self.item_lists

    def set_Item(self,data,init_list,columns_list):
        item_lists = []
        tmp_list = init_list
        item_lists.append(tmp_list)
        for item in data:
            tmp_list = []
            for col in columns_list:
                tmp_list.append(item[col])
            item_lists.append(tmp_list)
        # print(item_lists)

        return item_lists

    def Out_csv_rank(self,data):
        now = datetime.datetime.now()
        out_file_path = OUT_FILE_PATH.format(export_at=now.strftime('%Y%m%d_%H%M%S'))
        with open(out_file_path, mode='w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(data)
                
        return True

    def put_gspread(self,data):
        ss = SpreadsheetManager()
        # 書き込み
        range = "A1:A"+str(len(data)+1)
        print(range)
        ss.connect_by_sheetname(SPREADSHEET_ID, "item_list")
        ss.write(range,data)

### メイン処理
def main():
    item_master = Item_list()

    ## 課題6-2
    # キーワード入力
    keyword = input("キーワード入力：")
    # データ取得/表示
    item_lists = item_master.get_data(API_URL,keyword,"Items","Item")
    init_list = ["品名","金額[円]"]
    col_list = ['itemName','itemPrice']
    item_lists = item_master.set_Item(item_lists,init_list,col_list)

    ## 課題6-3 
    # データ取得/表示
    product_lists = item_master.get_data(P_API_URL,keyword,"Products","Product")
    init_list = ["商品","最大額","最低額"]
    col_list = ['productName','maxPrice','minPrice']
    product_lists = item_master.set_Item(product_lists,init_list,col_list)

    ## 課題6-4 
    # データ取得/表示
    rank_lists = item_master.get_data(R_API_URL,keyword,"Items","Item")
    init_list = ["rank","name","price","url"]
    col_list = ['rank','itemName','itemPrice','itemUrl']
    rank_lists = item_master.set_Item(rank_lists,init_list,col_list)
    item_master.Out_csv_rank(rank_lists)

    ## 課題6-7
    item_master.put_gspread(item_lists)
    
if __name__ == "__main__":
    main()