from pandas import json_normalize
import pandas as pd

pd.pandas.set_option("expand_frame_repr", False)


def test1():
    """
    解析一般的json对象
                   school location  ranking
    0  ABC primary school   London        2
    """
    a_dict = {
        'school': 'ABC primary school',
        'location': 'London',
        'ranking': 2
    }
    df = pd.json_normalize(a_dict)


def test2():
    """
    解析json列表
        class  student number    room
    0  Year 1              20  Yellow
    1  Year 2              25    Blue
    """
    json_list = [
        {'class': 'Year 1', 'student number': 20, 'room': 'Yellow'},
        {'class': 'Year 2', 'student number': 25, 'room': 'Blue'}
    ]
    df = pd.json_normalize(json_list)
    print(df)


def test3():
    """
    解析一个有多层数据的Json对象

    默认展开最大的层数
    -----------------
                   school location  ranking info.president info.contacts.email.admission info.contacts.email.general info.contacts.tel
    0  ABC primary school   London        2    John Kasich             admission@abc.com                info@abc.com         123456789

    max_level=1
    -----------------
                   school location  ranking info.president                                      info.contacts
    0  ABC primary school   London        2    John Kasich  {'email': {'admission': 'admission@abc.com', '...
    """
    json_obj = {
        'school': 'ABC primary school',
        'location': 'London',
        'ranking': 2,
        'info': {
            'president': 'John Kasich',
            'contacts': {
                'email': {
                    'admission': 'admission@abc.com',
                    'general': 'info@abc.com'
                },
                'tel': '123456789',
            }
        }
    }
    df = pd.json_normalize(json_obj)
    df1 = pd.json_normalize(json_obj, max_level=1)
    print(df1)


def test4():
    """
    解析带有嵌套列表的json
    默认不处理列表
    --------------
                   school location  ranking                                           students info.president info.contacts.email.admission info.contacts.email.general info.contacts.tel
    0  ABC primary school   London        2  [{'name': 'Tom'}, {'name': 'James'}, {'name': ...    John Kasich             admission@abc.com                info@abc.com         123456789

    解析record_path中的键, record_path='students'
    --------------
             name
    0         Tom
    1       James
    2  Jacqueline

    解析record_path中的键，同时增加其他字段 record_path='students', meta=['school', 'location', ['info', 'contacts', 'tel']]
    -------------
             name              school location info.contacts.tel
    0         Tom  ABC primary school   London         123456789
    1       James  ABC primary school   London         123456789
    2  Jacqueline  ABC primary school   London         123456789

    解析record_path中的键，同时增加其他字段 record_path='students', meta=['school', 'location', ['info', 'contacts', 'tel'], ['info', 'contacts', 'email', 'general']]
    -------------
             name              school location info.contacts.tel info.contacts.email.general
    0         Tom  ABC primary school   London         123456789                info@abc.com
    1       James  ABC primary school   London         123456789                info@abc.com
    2  Jacqueline  ABC primary school   London         123456789                info@abc.com

    """
    json_obj = {
        'school': 'ABC primary school',
        'location': 'London',
        'ranking': 2,
        'info': {
            'president': 'John Kasich',
            'contacts': {
                'email': {
                    'admission': 'admission@abc.com',
                    'general': 'info@abc.com'
                },
                'tel': '123456789',
            }
        },
        'students': [
            {'name': 'Tom'},
            {'name': 'James'},
            {'name': 'Jacqueline'}
        ],
    }
    df = pd.json_normalize(json_obj)
    df1 = pd.json_normalize(json_obj, record_path='students')
    df2 = pd.json_normalize(
        json_obj,
        record_path='students',
        meta=['school', 'location', ['info', 'contacts', 'tel']]
    )
    df3 = pd.json_normalize(
        json_obj,
        record_path='students',
        meta=['school', 'location', ['info', 'contacts', 'tel'], ['info', 'contacts', 'email', 'general']]
    )

    print(df3)


def test5():
    """
    当键不存在时的处理 errors='ignore'
             name sex   class    room info.teachers.math
    0         Tom   M  Year 1  Yellow         Rick Scott
    1       James   M  Year 1  Yellow         Rick Scott
    2        Tony   M  Year 2    Blue                NaN
    3  Jacqueline   F  Year 2    Blue                NaN
    """
    data = [
        {
            'class': 'Year 1',
            'student count': 20,
            'room': 'Yellow',
            'info': {
                'teachers': {
                    'math': 'Rick Scott',
                    'physics': 'Elon Mask',
                }
            },
            'students': [
                {'name': 'Tom', 'sex': 'M'},
                {'name': 'James', 'sex': 'M'},
            ]
        },
        {
            'class': 'Year 2',
            'student count': 25,
            'room': 'Blue',
            'info': {
                'teachers': {
                    # no math teacher
                    'physics': 'Albert Einstein'
                }
            },
            'students': [
                {'name': 'Tony', 'sex': 'M'},
                {'name': 'Jacqueline', 'sex': 'F'},
            ]
        },
    ]
    df = pd.json_normalize(
        data,
        record_path=['students'],
        meta=['class', 'room', ['info', 'teachers', 'math']],
        errors='ignore'
    )
    print(df)


if __name__ == '__main__':
    test5()
