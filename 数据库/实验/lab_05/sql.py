import pymysql
import random
from faker import Faker

fake = Faker()


def insert_data(amount):
    conn = pymysql.connect(host='localhost', user='root', password='121312QIUjiER+', db='college')
    cursor = conn.cursor()

    try:
        for i in range(1, amount + 1):
            name = fake.name()
            age = random.randint(18, 90)
            score = round(random.uniform(50, 100), 2)
            email = fake.email()
            cursor.execute("INSERT INTO test_index(name, age, score, email) VALUES (%s, %s, %s, %s)",
                           (name, age, score, email))
            if i % 1000 == 0:
                conn.commit()
                print(f"已插入 {i} 行")  # 添加进度打印

        conn.commit()
        print(f"总共插入 {amount} 行数据完成")

    except Exception as e:
        print(f"插入数据时出错: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

insert_data(1000000)  # 修改为 100 / 10000 / 1000000 分批测试
