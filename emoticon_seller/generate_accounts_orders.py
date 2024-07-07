import os
import pandas as pd
import numpy as np
import random
from decimal import Decimal
from dateutil.relativedelta import relativedelta

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
def create_account_table(num=1000):
    # CartItem.objects.all().delete()
    # Cart.objects.all().delete()
    # Account.objects.all().delete()

    next_id = get_next_id(Account)
    ids = range(next_id, next_id + num)

    account_df = pd.DataFrame({'id': ids})

    try:
        for _, row in tqdm(account_df.iterrows(), total=account_df.shape[0], desc='Get account data: '):
            loginType = AccountLoginType.objects.get(id=1)
            roleType = AccountRoleType.objects.get(id=1)
            Account.objects.create(
                id=row['id'],
                loginType_id=loginType.id,
                roleType_id=roleType.id
            )
        print('account table 데이터 입력 완료되었습니다.')
    except Exception as e:
        print('DB에 데이터 넣는 과정에서 에러 발생', e)

def create_profile_table(num=1000):
    next_id = get_next_id(Profile)
    ids = range(next_id, next_id + num)
    emails = [f'user{str(i).zfill(2)}@example.com' for i in range(next_id, next_id + num)]
    nicknames = [f'user{str(i).zfill(2)}' for i in range(next_id, next_id + num)]

    profile_df = pd.DataFrame({'id': ids, 'email': emails, 'nickname':nicknames})
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

def create_report_table(num=1000):
    next_id = get_next_id(Report)
    ids = range(next_id, next_id + num)
    ages = np.random.randint(10, 60, size=num)
    genders = np.random.choice(['남성', '여성'], size=num)

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

def create_orders_table(num=3000):
    # Orders.objects.all().delete()
    # ids = range(1, num + 1)
    next_id = get_next_id(Orders)
    ids = range(next_id, next_id + num)
    startDate = datetime.now().replace(microsecond=0)  # 현재 시간
    endDate = (startDate + relativedelta(months=4)).replace(microsecond=0)  # 4개월 후
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
                account_id=account.id)
        print('orders_item table 데이터 입력 완료되었습니다.')
    except Exception as e:
        print('DB에 데이터 넣는 과정에서 에러 발생', e)


def get_products_by_category(productCategory):
    selectedProductId = list(Product.objects.filter(productCategory =productCategory).values_list('productId', flat=True))
    return selectedProductId

def choose_products_based_on_preferences(num, orders_ids):
    id_of_cute_products = get_products_by_category('귀여운')
    id_of_fun_products = get_products_by_category('재밌는')
    id_of_message_products = get_products_by_category('메시지')

    product_ids = []

    for _, row in tqdm(orders_ids.iterrows(), total=orders_ids.shape[0], desc='데이터 조작중 ... : '):
        order = Orders.objects.get(id=row['orders_id'])
        account_id = order.account_id
        report = Report.objects.get(account_id=account_id)
        age = report.age
        gender = report.gender

        if 10 <= age <= 20:
            if gender == '여성':
                categories = [id_of_cute_products] * int(num * 0.6) + [id_of_fun_products] * int(num * 0.35) + [
                    id_of_message_products] * int(num * 0.05)
            else:
                categories = [id_of_cute_products] * int(num * 0.27) + [id_of_fun_products] * int(num * 0.7) + [
                    id_of_message_products] * int(num * 0.03)
        elif 21 <= age <= 30:
            categories = [id_of_cute_products] * int(num * 0.5) + [id_of_fun_products] * int(num * 0.3) + [id_of_message_products] * int(
                num * 0.2)
        elif 31 <= age <= 40:
            categories = [id_of_cute_products] * int(num * 0.5) + [id_of_fun_products] * int(num * 0.1) + [id_of_message_products] * int(
                num * 0.4)
        else:
            categories = [id_of_message_products] * int(num * 0.75) + [id_of_cute_products] * int(num * 0.2) + [id_of_fun_products] * int(
                num * 0.05)

        # random.shuffle(categories)  # 랜덤 선택을 위해 섞기

        for category in categories:
            product_id = random.choice(category)
            product_ids.append(product_id)

    return product_ids
def create_orders_item_table(num=10000):
    # next_id = get_next_id(OrdersItem)
    existing_orders_ids = list(Orders.objects.values_list('id', flat=True))
    additional_orders_needed = num - len(existing_orders_ids)
    if additional_orders_needed > 0:
        additional_orders_ids = random.choices(existing_orders_ids, k=additional_orders_needed)
        orders_ids = existing_orders_ids + additional_orders_ids
    # orders_ids를 사용하여 DataFrame 생성
    orders_df = pd.DataFrame({'orders_id': orders_ids})
    print('주문아이디 :', orders_df['orders_id'].nunique(), '주문 아이템 총 :',orders_df['orders_id'].count())
    # 상품 ID를 연령대 및 성별에 따라 선택
    selected_product_ids = choose_products_based_on_preferences(num, orders_df)
    orders_item_data = []
    for i in range(len(orders_ids)):
        order_id = orders_ids[i]
        product_id = selected_product_ids[i]

        orders_item_data.append({
            'id': i+1,
            'orders_id': order_id,
            'product_id': product_id
            })

    orders_item_df = pd.DataFrame(orders_item_data)
    print('만들어진 orders_item : ',orders_item_df)
    try:
        for _, row in tqdm(orders_item_df.iterrows(), total=orders_item_df.shape[0], desc='Get orders_item data: '):
            orders = Orders.objects.get(id=row['orders_id'])
            product = Product.objects.get(productId=row['product_id'])
            OrdersItem.objects.create(
                id=row['id'],
                price=product.productPrice,
                product_id=product.productId,
                orders_id=orders.id
            )
        print('orders_item table 데이터 입력 완료되었습니다.')
    except Exception as e:
        print('DB에 데이터 넣는 과정에서 에러 발생', e)

# service
if __name__ == '__main__':
    # create_account_table()
    # create_profile_table()
    # create_report_table()
    # create_orders_table()
    create_orders_item_table()

