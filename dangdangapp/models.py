# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AddressInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    consignee = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(db_column='Address', max_length=40, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    cellphone = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address_info'


class Booksinfo(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=40, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    publish = models.CharField(max_length=40, blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    printing_time = models.DateField(blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=40, blank=True, null=True)  # Field name made lowercase.
    word_number = models.IntegerField(blank=True, null=True)
    page_number = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=40, blank=True, null=True)
    paper = models.CharField(max_length=40, blank=True, null=True)
    package = models.CharField(max_length=40, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    dd_price = models.FloatField(db_column='DD_price', blank=True, null=True)  # Field name made lowercase.
    all_numberl = models.IntegerField(blank=True, null=True)
    sales_volume = models.IntegerField(blank=True, null=True)
    arrival_time = models.DateField(blank=True, null=True)
    books_id = models.IntegerField(blank=True, null=True)
    print_num = models.IntegerField(blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    sort = models.ForeignKey('Sort1', models.DO_NOTHING, blank=True, null=True)
    pic = models.CharField(max_length=200, blank=True, null=True)
    series_name = models.CharField(max_length=130, blank=True, null=True)
    customer_grade = models.FloatField(blank=True, null=True)
    market = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booksinfo'


class OrderList(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Booksinfo, models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey('TOrder', models.DO_NOTHING, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    all_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_list'


class Sort1(models.Model):
    id = models.IntegerField(primary_key=True)
    sort_name = models.CharField(max_length=20, blank=True, null=True)
    books_num = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sort1'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    order_num = models.IntegerField(blank=True, null=True)
    generated_time = models.DateField(blank=True, null=True)
    order_all_price = models.IntegerField(blank=True, null=True)
    address = models.ForeignKey(AddressInfo, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TUser(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=40, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=40, blank=True, null=True)
    user_state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'


class Confirm_string(models.Model):
    code=models.CharField(max_length=256)
    user=models.ForeignKey('TUser',on_delete=models.CASCADE)
    code_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 't_confirm_string'
