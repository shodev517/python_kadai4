import csv
import datetime

now = datetime.datetime.now()
filename = './receipt/' + now.strftime('%Y%m%d_%H%M%S') + '.txt'
path =(filename)

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order(Item):
    total_price = 0
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_cnt_list=[]
        self.item_master=item_master
    
    def add_item_order(self, item_code, item_cnt):
        self.item_order_list.append(item_code)
        self.item_cnt_list.append(item_cnt)       
        
    def view_item_list(self):
        
        for item_code,item_cnt in zip(self.item_order_list, self.item_cnt_list):
            # オーダー番号から商品情報取得
            result = self.get_item_order(item_code)
            self.total_price += int(result[1])*int(item_cnt)
            self.write_receipt("商品コード:{}".format(item_code)+"　商品名：{}".format(result[0])+"　価格：{}円　".format(result[1]))
            self.write_receipt("個数：{}".format(item_cnt)+"　合計金額は{}円です。".format(self.total_price)+"\n")
        
    # オーダー番号から商品情報を取得        
    def get_item_order(self, item_code):
        for i in self.item_master:
            if item_code == i.item_code:
                return i.item_name, i.price
    
    # オーダー登録
    def register_order(self, order, item_master):
        order.add_item_order(input("商品コードを入力してください。："),input("個数を入力してください。："))
    
    # 会計
    def order_payment(self):
        input_money = int(input("お支払い金額を入力してください。："))
        self.write_receipt("{}円お預かりしました。".format(input_money)+"\n")
        if input_money >= self.total_price:
            change_money = input_money - self.total_price
            self.write_receipt("おつりは{}円です。".format(change_money))
        else :
            change_money = self.total_price - input_money
            print("金額が{}円足りません。".format(change_money))
            
    # レシート発行
    def write_receipt(self, text):
        print(text)
        # レシートに書き込み
        with open(path, mode='a', encoding='utf-8', newline="\n") as f:
                f.write(text) 
    
### メイン処理
def main():
    # マスタ登録
    item_master=[]
    csv_file = open("./master_list.csv", "r", encoding="utf-8", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)    
    for i in f:
        item_master.append(Item(i[0],i[1],i[2]))

    # オーダー登録
    order=Order(item_master)
    order.register_order(order, item_master)
    
    # オーダー表示
    order.view_item_list()
    
    # 会計
    order.order_payment()
    
if __name__ == "__main__":
    main()