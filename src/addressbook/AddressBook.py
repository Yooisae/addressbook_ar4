# coding: utf-8

import sys
from datetime import datetime

from faker import Faker
from tabulate import tabulate
import tablib

from random import randint


class AddressBook:
    headers = ["이름", "전화번호", "주소", "직업", "생년월일", "수정한 날짜"]

    def __init__(self):
        self.address_book = []

    def _now(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _sort(self, array, key = lambda x:x):
        if len(array) < 2:
            return array

        pivot = array[randint(0, len(array) - 1)] # 배열이니까 맨 마지막 index는 길이 - 1 이다.
        _pivot = key(pivot)
        # pivot = array[0] # 배열이니까 맨 마지막 index는 길이 - 1 이다.

        low, same, high = [], [], []

        # n번 O(n)
        for item in array:
            _item = key(item)
            if _item < _pivot:
                low.append(item)
            elif _item == _pivot:
                same.append(item)
            elif _item > _pivot:
                high.append(item)

        return self._sort(low, key) + same + self._sort(high, key)
    
    def sort(self, method):
        if method == '1':
            self.address_book = self._sort(self.address_book, key = lambda x:x[0])
        elif method == '2':
            self.address_book = self._sort(self.address_book, key = lambda x:x[4])
        elif method == '3':
            self.address_book = self._sort(self.address_book, key = lambda x:x[5])
        else :
            sys.stderr.write("1 또는 2 를 입력해주세요.\n")
            sys.stderr.write("정렬 방법은 1 이름 정렬, 2 생년월일 정렬, 3 수정한 날짜 정렬입니다.\n")

    def table(self):
        return tabulate(self.address_book, headers=self.headers,
                        showindex=True, tablefmt="fancy_grid")

    def show(self):
        print(self.table())

    def add(self, name, phone_number, address, job, birth):
        self.address_book.append(
            [name, phone_number, address, job, birth, self._now()])

    def remove(self, index):
        del self.address_book[index]

    def modify(self, index, name, phone_number, address, birth, job):
        self.address_book[index] = [
            name, phone_number, address, job, birth, self._now()]

    def save(self, fname, type='csv'):
        if type not in ['csv', 'xlsx']:
            sys.stderr.write('파일 타입은 csv 또는 xlsx 이어야 합니다.\n')
            return

        address_book_data = tablib.Dataset()
        address_book_data.headers = self.headers
        for address in self.address_book:
            address_book_data.append(address)

        filepath = fname+'.'+type

        if type == 'xlsx':
            with open(filepath, 'wb') as f:
                f.write(address_book_data.export('xlsx'))
        elif type == 'csv':
            with open(filepath, 'w') as f:
                f.write(address_book_data.export('csv'))

    def load(self, fname, type='csv'):
        if type not in ['csv', 'xlsx']:
            sys.stderr.write('파일 타입은 csv 또는 xlsx 이어야 합니다.\n')
            return

        address_book_data = tablib.Dataset()
        address_book_data.headers = self.headers
        filepath = fname+'.'+type

        try:
            if type == 'xlsx':
                with open(filepath, 'rb') as f:
                    address_book_data.load(f, 'xlsx')
            elif type == 'csv':
                with open(filepath, 'r') as f:
                    address_book_data.load(f, 'csv')
        except FileNotFoundError:
            sys.stderr.write('존재하지 않는 파일입니다.\n')
            return

        self.address_book = address_book_data



class FakeAddressBook(AddressBook):
    def __init__(self):
        super().__init__()
        self.fake = Faker('ko_KR')

    def _fake_person(self):
        return [self.fake.name(), self.fake.phone_number(),
                self.fake.address(), self.fake.job(), self.fake.date(), self._now()]

    def add_fake(self, num):
        for _ in range(num):
            self.address_book.append(self._fake_person())

def main():
    address_book = FakeAddressBook()

    while 1:
        sel = input("1) 추가 2) 가짜 추가 3) 수정 4) 삭제 "
                    "5) 보기 6) 주소록 저장 7) 주소록 불러오기 8) 정렬 9) 종료 > ")
        if sel == '1':
            address_book.add(input("이름: "), input("전화번호: "),
                                input("주소: "), input("직업: "), input("생년월일: "))
        elif sel == '2':
            address_book.add_fake(int(input("가짜 프로필 갯수: ")))
        elif sel == '3':
            param = int(input("번호: ")), input("이름: "), input(
                "전화번호: "), input("주소: "), input("직업: "), input("생년월일: ")
            address_book.modify(*param)
        elif sel == '4':
            address_book.remove(int(input("번호: ")))
        elif sel == '5':
            address_book.show()
        elif sel == '6':
            address_book.save(input("파일명: "), input("파일 타입(csv 또는 xlsx): "))
        elif sel == '7':
            address_book.load(input("파일명: "), input("파일 타입(csv 또는 xlsx): "))
        elif sel == '8':
            method = input("정렬 방법( 1. 이름 정렬  2. 생년월일 정렬  3. 수정한 날짜 ): ")
            address_book.sort(method)
        elif sel == '9':
            break
        else:
            print("잘못된 입력입니다.")
            continue

if __name__ == '__main__':
    main()


"""
1. 수정한 날짜를 기준으로 정렬하는 기능 
2. reverse 기능 추가 => 정렬을 반대로 하는거
"""