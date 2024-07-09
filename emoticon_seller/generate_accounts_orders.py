import os
import pandas as pd
import numpy as np
import random
from itertools import chain
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

    endDate = datetime.now().replace(microsecond=0)  # 현재 시간
    startDate = (endDate - relativedelta(months=4)).replace(microsecond=0) # 4개월 전
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


def generate_product_ids_by_preferences(age, gender, num):
    id_of_cute_products = get_products_by_category('귀여운')
    id_of_fun_products = get_products_by_category('재밌는')
    id_of_message_products = get_products_by_category('메시지')

    if 10 <= age <= 20:
        if gender == '여성':
            cute_count = int(num * 0.66)
            fun_count = int(num * 0.33)
            message_count = int(num * 0.01)
        else:
            cute_count = int(num * 0.09)
            fun_count = int(num * 0.9)
            message_count = int(num * 0.01)
    elif 21 <= age <= 30:
        if gender == '여성':
            cute_count = int(num * 0.67)
            fun_count = int(num * 0.3)
            message_count = int(num * 0.03)
        else:
            cute_count = int(num * 0.09)
            fun_count = int(num * 0.9)
            message_count = int(num * 0.01)
    elif 31 <= age <= 40:
        if gender == '여성':
            cute_count = int(num * 0.3)
            fun_count = int(num * 0.05)
            message_count = int(num * 0.65)
        else:
            cute_count = int(num * 0.1)
            fun_count = int(num * 0.01)
            message_count = int(num * 0.89)
    else:
        cute_count = int(num * 0.09)
        fun_count = int(num * 0.01)
        message_count = int(num * 0.9)

    cute_products = random.choices(id_of_cute_products, k=cute_count)
    fun_products = random.choices(id_of_fun_products, k=fun_count)
    message_products = random.choices(id_of_message_products, k=message_count)

    combined_products = list(chain(cute_products, fun_products, message_products))
    random.shuffle(combined_products)

    return combined_products


def choose_products_based_on_preferences(num, orders_ids):
    product_ids = []
    products_by_conditions = {
        "10-20여성": generate_product_ids_by_preferences(15, "여성", num),
        "10-20남성": generate_product_ids_by_preferences(15, "남성", num),
        "21-30여성": generate_product_ids_by_preferences(25, "여성", num),
        "21-30남성": generate_product_ids_by_preferences(25, "남성", num),
        "31-40여성": generate_product_ids_by_preferences(35, "여성", num),
        "31-40남성": generate_product_ids_by_preferences(35, "남성", num),
        "40+여성": generate_product_ids_by_preferences(45, "여성", num),
        "40+남성": generate_product_ids_by_preferences(45, "남성", num),
    }

    for _, row in tqdm(orders_ids.iterrows(), total=orders_ids.shape[0], desc='데이터 조작중 ... : '):
        order = Orders.objects.get(id=row['orders_id'])
        account_id = order.account_id
        report = Report.objects.get(account_id=account_id)
        age = report.age
        gender = report.gender

        if 10 <= age <= 20:
            condition_key = "10-20여성" if gender == "여성" else "10-20남성"
        elif 21 <= age <= 30:
            condition_key = "21-30여성" if gender == "여성" else "21-30남성"
        elif 31 <= age <= 40:
            condition_key = "31-40여성" if gender == "여성" else "31-40남성"
        else:
            condition_key = "40+여성" if gender == "여성" else "40+남성"

        selected_product_ids = products_by_conditions[condition_key]

        if len(selected_product_ids) >= num:
            product_ids.extend(selected_product_ids[:num])
            products_by_conditions[condition_key] = selected_product_ids[num:]
        elif selected_product_ids:
            product_ids.extend(selected_product_ids)
            additional_needed = num - len(selected_product_ids)
            additional_products = random.choices(selected_product_ids, k=additional_needed)
            product_ids.extend(additional_products)

    return product_ids
def create_orders_item_table(num=10000):
    existing_orders_ids = list(Orders.objects.values_list('id', flat=True))
    additional_orders_needed = num - len(existing_orders_ids)
    if additional_orders_needed > 0:
        additional_orders_ids = random.choices(existing_orders_ids, k=additional_orders_needed)
        orders_ids = existing_orders_ids + additional_orders_ids

    orders_df = pd.DataFrame({'orders_id': orders_ids})
    print('주문아이디 :', orders_df['orders_id'].nunique(), '주문 아이템 총 :', orders_df['orders_id'].count())

    selected_product_ids = choose_products_based_on_preferences(num, orders_df)

    orders_item_data = []
    for i in range(len(orders_ids)):
        order_id = orders_ids[i]
        product_id = selected_product_ids[i]

        orders_item_data.append({
            'id': i + 1,
            'orders_id': order_id,
            'product_id': product_id
        })

    orders_item_df = pd.DataFrame(orders_item_data)
    print('만들어진 orders_item : ', orders_item_df)
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

