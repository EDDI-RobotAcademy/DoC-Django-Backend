import os
import pandas as pd
import numpy as np
import random
from decimal import Decimal

from django.db.models import Max
from tqdm import tqdm
from datetime import datetime, timedelta

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emoticon_seller.settings")
django.setup()

from account.entity.account_role_type import AccountRoleType
from account.entity.account_login_type import AccountLoginType
from product.entity.models import Product
from orders.entity.orders import Orders
from orders.entity.orders_item import OrdersItem
from account.entity.account import Account
from account.entity.profile import Profile
from report.entity.report import Report
from cart.entity.cart import Cart
from cart.entity.cart_item import CartItem

import warnings
warnings.filterwarnings("ignore")

def get_next_id(model):
    max_id = model.objects.aggregate(max_id=Max('id'))['max_id']
    return (max_id or 0) + 1
def create_account_table(num=3000):
    # CartItem.objects.all().delete()
    # Cart.objects.all().delete()
    # Account.objects.all().delete()

    next_id = get_next_id(Account)
    ids = range(next_id, next_id + num)

    loginType_ids = [1]*num
    roleType_ids = [1]*num
    account_df = pd.DataFrame({'id': ids, 'loginType_id': loginType_ids, 'roleType_id': roleType_ids})

    try:
        for _, row in tqdm(account_df.iterrows(), total=account_df.shape[0], desc='Get account data: '):
            loginType_id = AccountLoginType.objects.get(id=row['loginType_id']).id
            roleType_id = AccountRoleType.objects.get(id=row['roleType_id']).id
            Account.objects.create(
                id=row['id'],
                loginType_id=loginType_id,
                roleType_id=roleType_id
            )
        print('account table 데이터 입력 완료되었습니다.')
    except Exception as e:
        print('DB에 데이터 넣는 과정에서 에러 발생', e)

def create_profile_table(num=3000):
    next_id = get_next_id(Profile)
    ids = range(next_id, next_id + num)
    emails = [f'user{str(i).zfill(2)}@example.com' for i in range(next_id, next_id + num)]
    nicknames = [f'user{str(i).zfill(2)}' for i in range(next_id, next_id + num)]
    account_ids = list(Account.objects.values_list('id', flat=True))

    profile_df = pd.DataFrame({'id': ids, 'email': emails, 'nickname':nicknames})#, 'account_id': account_ids})
    try:
        for _, row in tqdm(profile_df.iterrows(), total=profile_df.shape[0],  desc='Get profile data: '):
            account = Account.objects.get(id=row['id'])
            Profile.objects.create(
                id=row['id'],
                email=row['email'],
                nickname=row['nickname'],
                account_id=account.id
            )
        print('profile table 데이터 입력 완료되었습니다.')
    except Exception as e:
        print('DB에 데이터 넣는 과정에서 에러 발생', e)

def create_report_table(num=3000):
    # Report.objects.all().delete()
    next_id = get_next_id(Report)
    ids = range(next_id, next_id + num)
    # ids = range(1, num + 1)
    ages = np.random.randint(10, 60, size=num)
    genders = np.random.choice(['남성', '여성'], size=num)
    # account_ids = list(Account.objects.values_list('id', flat=True))

    report_df = pd.DataFrame({'id': ids, 'age': ages, 'gender':genders})

    try:
        for _, row in tqdm(report_df.iterrows(), total=report_df.shape[0], desc='Get report data: '):
            account = Account.objects.get(id=row['id'])
            Report.objects.create(
                id=row['id'],
                age=row['age'],
                gender=row['gender'],
                account_id=account.id
            )
        print('report table 데이터 입력 완료되었습니다.')
    except Exception as e:
        print('DB에 데이터 넣는 과정에서 에러 발생', e)

def create_orders_table(num=500):
    # Orders.objects.all().delete()
    # columns
    # ids = range(1, num + 1)
    next_id = get_next_id(Orders)
    ids = range(next_id, next_id + num)
    startDate = datetime(2024, 6, 1)
    endDate = datetime(2024, 6, 30, 23, 59, 59)
    createdDates = [startDate + timedelta(
        seconds=random.randint(0, int((endDate - startDate).total_seconds()))) for _ in range(num)]

    account_ids = list(Account.objects.values_list('id', flat=True))
    account_ids = random.choices(account_ids, k=num)

    orders_df = pd.DataFrame({'id':ids, 'createdDate': createdDates, 'account_id':account_ids})
    try:
        for _, row in tqdm(orders_df.iterrows(), total=orders_df.shape[0], desc='Get orders data: '):
            account = Account.objects.get(id=row['account_id'])
            Orders.objects.create(
                id=row['id'],
                createdDate=row['createdDate'],
                account_id=account.id )
        print('orders_item table 데이터 입력 완료되었습니다.')
    except Exception as e:
        print('DB에 데이터 넣는 과정에서 에러 발생', e)


def create_orders_item_table(num=10000):
    # OrdersItem.objects.all().delete()
    next_id = get_next_id(OrdersItem)
    ids = range(next_id, next_id + num)
    # ids = range(1, num + 1)
    orders_ids = list(Orders.objects.values_list('id', flat=True))
    orders_ids = random.choices(orders_ids, k=num)
    product_ids = list(Product.objects.values_list('productId', flat=True))
    product_ids = random.choices(product_ids, k=num)
    orders_item_df = pd.DataFrame({'id':ids,'orders_id':orders_ids,'product_id':product_ids})
    try:
        for _, row in tqdm(orders_item_df.iterrows(), total=orders_item_df.shape[0], desc='Get orders_item data: '):
            orders = Orders.objects.get(id=row['orders_id'])
            product_id = Product.objects.get(productId=row['product_id'])
            OrdersItem.objects.create(
                id=row['id'],
                price=product_id.productPrice,
                product_id=product_id.productId,
                orders_id=orders.id)
        print('orders_item table 데이터 입력 완료되었습니다.')
    except Exception as e:
        print('DB에 데이터 넣는 과정에서 에러 발생', e)


# service
if __name__ == '__main__':
    create_account_table(1)
    create_profile_table(1)
    create_report_table(1)
    create_orders_table(1)
    create_orders_item_table(1)
