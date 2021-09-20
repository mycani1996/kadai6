import pytest
from kadai6 import Item_list

# 定数を定義
API_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'
P_API_URL = "https://app.rakuten.co.jp/services/api/Product/Search/20170426"
R_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"

item_data = [{"itemName":"PC1","itemPrice":100},{"itemName":"PC2","itemPrice":200}]
product_data = [{"productName":"PCa","maxPrice":200,"minPrice":100},{"productName":"PCb","maxPrice":1000,"minPrice":500}]
rank_data = [{"rank":1,"itemName":"PC1","itemPrice":100,"itemUrl":"htts://www1"},{"rank":2,"itemName":"PC2","itemPrice":50,"itemUrl":"htts://www2"}]

@pytest.mark.parametrize(
    "url,word,columns,column", [
        (API_URL,"PC","Items","Item"),
        (P_API_URL,"PC","Products","Product"),
        (R_API_URL,"PC","Items","Item")
    ]
)
def test_get_data(url,word,columns,column):
    item = Item_list()  
    data = item.get_data(url,word,columns,column)
    print(data)
    assert len(data) >= 1

@pytest.mark.parametrize(
    "data,init_list,columns_list", [
        (item_data,["品名","金額[円]"],['itemName','itemPrice']),
        (product_data,["商品","最大額","最低額"],['productName','maxPrice','minPrice']),
        (rank_data,["rank","name","price","url"],['rank','itemName','itemPrice','itemUrl'])
    ]
)
def test_set_Item(data,init_list,columns_list):
    item = Item_list()  
    item_lists = item.set_Item(data,init_list,columns_list)
    assert len(item_lists) >= 1

@pytest.mark.parametrize("rank_data", [rank_data])
def test_Out_csv_rank(rank_data):
   item = Item_list()
   assert item.Out_csv_rank(rank_data)



