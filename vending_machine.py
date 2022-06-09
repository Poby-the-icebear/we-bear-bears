import sys
import numpy as np

items = {
    "아이시스": {'price': 700, 'pcs': 5}, "레몬워터": {'price': 1600, 'pcs': 0},
    "옥수수수염차": {'price': 1400, 'pcs': 0}, "칸타타콘트라베이스": {'price': 2100, 'pcs': 3},
    "트레비": {'price': 1100, 'pcs': 3}, "밀키스": {'price': 900, 'pcs': 5},
    "펩시": {'price': 900, 'pcs': 5}, "핫식스": {'price': 1100, 'pcs': 1},
    "칠성사이다": {'price': 100, 'pcs': 3}, "코코팜리치": {'price': 1100, 'pcs': 5},
    "립톤": {'price': 1100, 'pcs': 0}, "트로피칼사과": {'price': 1100, 'pcs': 5},
    "트로피칼포도": {'price': 1100, 'pcs': 5}, '가나초코': {'price': 700, 'pcs': 0},
    "레쓰비": {'price': 700, 'pcs': 1}, "칸타타": {'price': 1100, 'pcs': 1},
    "레쓰비카페타임": {'price': 1100, 'pcs': 5}, "게토레이": {'price': 900, 'pcs': 5},
    "코코팜포도": {'price': 900, 'pcs': 5}, "잔치집식혜": {'price': 900, 'pcs': 5}
}
coins = {"1000원": 5, "500원": 2, "100원": 2}


class Manager:

    def __init__(self):
        print("음료 자판기 현황\n")
        self.check_inven()
        print()
        self.check_coins()

    @staticmethod
    def check_inven():
        for i in items:
            if int(items[i]['pcs']) <= 1:
                print('\033[31m' + f"제품명:{i}-가격:{items[i]['price']}-수량:{items[i]['pcs']}" + '\033[0m')
            else:
                print(f"제품명:{i}-가격:{items[i]['price']}-수량:{items[i]['pcs']}")

    @staticmethod
    def check_coins():
        for c in coins:
            if int(coins[c]) <= 2:
                print('\033[31m' + f'{c}-갯수:{coins[c]}' + '\033[0m')
            else:
                print(f'{c}-갯수:{coins[c]}')

    @staticmethod
    def get_item(item_list):
        for row in item_list:
            if row[0] in items.keys():
                items[row[0]]['pcs'] += int(row[1])
            else:
                print(f"{row[0]}은/는 존재 하지 않는 음료수입니다")
                continue

    @staticmethod
    def get_coins(coins_list):
        for row in coins_list:
            if row[0] in coins.keys():
                coins[row[0]] += int(row[1])
            else:
                print(f"{row[0]}은 존재 하지 않는 단위입니다")
                continue

    def manage_inventory(self):

        query = str(input("\n물품을 추가하시겠습니까? 아니면 거스름돈을 관리하시겠습니까?: "))

        if query == '물품':
            data = []
            print("종류의 수(int)\n음료 이름(str) 음료 갯수(int)")
            number = int(input("추가할 음료의 종류의 수를 입력하고 음료의 이름과 추가할 갯수를 입력해주세요: "))
            for i in range(number):
                data.append(list(map(str, sys.stdin.readline().split())))

            self.get_item(data)
            print("업데이트 완료")
            print("갱신된 상태를 확인해주세요\n")
            self.check_inven()

            return self.manage_inventory()

        elif query == "거스름돈":

            money = []
            print("단위의 수(int)\n단위 이름(str) 화폐 갯수(int)")
            num = int(input("추가할 단위의 수, 단위의 이름과 추가할 화폐의 갯수를 입력하세요: "))
            for i in range(num):
                money.append(list(map(str, sys.stdin.readline().split())))

            self.get_coins(money)
            print("업데이트 완료")
            print("갱신된 상태를 확인해주세요\n")
            self.check_coins()

            return self.manage_inventory()

        else:
            print("관리자 모드 종료")
            return main()


class Customer:

    def __init__(self, total):
        self.total = int(total.strip("원"))
        self.store_coins(self.total)
        self.check_inven_cus()

    def check_inven_cus(self):
        print("음료 현황\n")
        for i in items:
            if items[i]['pcs'] == 0:
                print(f"{i} 현재 재고 없음 " + '\033[31m' + 'X' + '\033[0m')
            elif items[i]['pcs'] > 0 and self.total < items[i]['price']:
                print(f"제품명:{i}-가격:{items[i]['price']} " + '\033[31m' + '잔액 부족' + '\033[0m')
            elif self.not_for_sale(i, self.total) is True:
                print(f"{i}는 주문 불가 상태 " + '\033[31m' + 'X' + '\033[0m')
            else:
                print(f"제품명:{i}-가격:{items[i]['price']}")

    @staticmethod
    def not_for_sale(choice, change_value):
        coins_total = coins['500원'] * 500 + coins['100원'] * 100
        all_data = [[ne_key, ne_value] for ne_key, ne_value in items.items()]
        a = [row[1]['price'] for row in all_data]
        b = [((change_value - idx) - coins_total) for idx in a]
        c = [row[0] for row in all_data]
        res = np.array(b)
        d = np.where(res > 0)[0]
        last_list = [c[i] for i in d]
        if choice in last_list:
            return True
        else:
            return False

    def store_coins(self, input_money):
        coin = []
        a = [i for i in coins.keys()]
        print("1000원짜리 500원짜리 100원짜리 몇 개를 넣을 지 입력하시오.")
        for i in range(3):
            coin.append(list(map(str, sys.stdin.readline().split())))
        b = [row[0] for row in coin]
        c = (int(coin[0][0].strip('원')) * int(coin[0][1])) + (int(coin[1][0].strip('원')) * int(coin[1][1])) + (int(
            coin[2][0].strip('원')) * int(coin[2][1]))
        for won in a:
            if won not in b:
                try:
                    raise
                except:
                    print("존재 하지 않는 단위입니다.")
                    print(f"{input_money}원을 가져가세요")
                    self.total = 0
                    return main()

            else:
                if c != input_money:
                    question = input("입력된 수치가 다릅니다. 그냥 진행하시겠습니까? 네 or 아니요: ")
                    if question == '네':
                        coins[coin[0][0]] += int(coin[0][1])
                        coins[coin[1][0]] += int(coin[1][1])
                        coins[coin[2][0]] += int(coin[2][1])
                        self.total = c
                        print(f"현재 입력된 금액: {c}")
                        break
                    else:
                        try:
                            raise
                        except:
                            print(f"{c}원을 가져가세요")
                            self.total = 0
                            return main()

                else:
                    coins[coin[0][0]] += int(coin[0][1])
                    coins[coin[1][0]] += int(coin[1][1])
                    coins[coin[2][0]] += int(coin[2][1])

    def addition_money(self, addition):
        self.total += int(addition.strip('원'))
        self.store_coins(int(addition.strip('원')))

    @staticmethod
    def change_100(count_100):
        if count_100 <= coins['100원']:
            coins['100원'] -= count_100
            return

    def change_process(self, amount_due, left_coins):
        answer = input("거스름돈을 반환하시겠습니까? 네 or 아니요: ")
        if answer == '네':

            korean_500 = amount_due // 500
            if coins['500원'] >= korean_500:
                coins['500원'] -= korean_500
                amount_due %= 500
                korean_100 = amount_due // 100
                self.change_100(korean_100)
                print(f"500원 {korean_500}개 100원 {korean_100}개가 반환되었습니다.")
                print("확인하고 가져가세요")

            elif coins['500원'] < korean_500:
                can_provide = coins['500원']
                coins['500원'] -= can_provide
                amount_due -= can_provide * 500
                korean_100 = amount_due // 100
                self.change_100(korean_100)
                print(f"500원 {can_provide}개 100원 {korean_100}개가 반환되었습니다.")
                print("확인하고 가져가세요")

            elif coins['500원'] == 0:
                korean_500 = 0
                korean_100 = amount_due // 100
                self.change_100(korean_100)
                print(f"500원 {korean_500}개 100원 {korean_100}개가 반환되었습니다.")
                print("확인하고 가져가세요")

            return main()

        else:
            self.total = left_coins
            self.check_inven_cus()
            return self.whole_process()

    def order_process(self, selection):
        item_n = selection

        if items[item_n]['price'] > self.total:
            try:
                raise
            except:
                lack_money = items[item_n]['price'] - self.total
                print(f"잔액이 {lack_money}만큼 부족합니다")
                choice_answer = input("거스름돈을 반환하시겠습니까? 또는 돈을 더 넣으시겠습니까? 거스름돈 or 돈: ")
                if choice_answer == '거스름돈':
                    self.change_process(self.total, self.total)
                else:
                    add_money = input("얼마를 더 넣으시겠습니까?")
                    self.addition_money(add_money)
                    self.check_inven_cus()
                    return self.whole_process()

        else:
            items[item_n]['pcs'] -= 1
            change = self.total - items[item_n]['price']
            if change == 0:
                print(f"주문하신 {item_n} 나왔습니다.")
                print("잔액이 없습니다")
                return main()
            else:
                print(f"주문하신 {item_n} 나왔습니다.")
                print("잔액", change)
                self.change_process(change, change)

    def whole_process(self):
        drink_selection = input('\n음료를 골라주세요: ')
        if items[drink_selection]['pcs'] == 0 or self.not_for_sale(drink_selection, self.total) is True:
            try:
                raise
            except:
                if items[drink_selection]['pcs'] == 0:
                    print("현재 주문 불가능한 제품입니다.\n")
                    self.check_inven_cus()
                    return self.whole_process
                elif self.not_for_sale(drink_selection, self.total) is True:
                    print("현재 주문 불가능한 제품입니다.\n")
                    self.change_process(self.total, self.total)
        else:
            self.order_process(drink_selection)


def main():
    print("\n음료 자판기에 오신 것을 환영합니다")
    print("\n1000원, 500원, 100원만 투입 가능합니다.")
    actor = str(input("돈을 투입해주세요: "))
    print()

    if actor == "비밀키":
        manager = Manager()
        manager.manage_inventory()
    else:
        customer = Customer(actor)
        customer.whole_process()


main()
