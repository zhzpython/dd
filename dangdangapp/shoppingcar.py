from dangdangapp.models import Booksinfo
class Caritem():
    def __init__(self,book,amount):
        self.amount=amount
        self.book=book


class Car():
    def __init__(self):
        self.save_price=0
        self.total_price=0
        self.caritems=[]

    def sums(self):
        self.total_price=0
        self.save_price=0
        for i in self.caritems:
            self.total_price+=i.book.dd_price * i.amount
            self.save_price+=(i.book.price-i.book.dd_price)*i.amount

    def add_book_toCar(self,bookid,changenum=1):   #添加购物车书的数量
        for j in self.caritems:
            if j.book.id == bookid:
                j.amount+=changenum
                self.sums()
                return
        book=Booksinfo.objects.filter(id=bookid)[0]
        self.caritems.append(Caritem(book,changenum))
        self.sums()



    def change_car_count(self,bookid,amount):  #变更购物车书的数量
        for k in self.caritems:
            if k.book.id==bookid:
                k.amount=amount
            self.sums()


    def delete_book(self,bookid):    #删除购物车的书
        for b in self.caritems:
            if b.book.id==bookid:
                self.caritems.remove(b)
        self.sums()