# -*- encoding: utf8 -*-
import datetime
import decimal

def to_dict(o, extend_columns=None):
    if extend_columns is None:
        extend_columns = []
    if isinstance(o, list):
        result = []
        for item in o:
            try:
                dict = {}
                for e in extend_columns:
                    if isinstance(getattr(item, e), decimal.Decimal):
                        dict[e] = float(getattr(item, e))
                    else:
                        dict[e] = getattr(item, e)
                for c in item.__table__.columns:
                    if isinstance(getattr(item, c.name), decimal.Decimal):
                        dict[c.name] = float(getattr(item, c.name))
                    else:
                        dict[c.name] = getattr(item, c.name)
                result.append(dict)
            except:
                continue
        return result
    else:
        try:
            dict = {}
            for e in extend_columns:
                if isinstance(getattr(o, e), decimal.Decimal):
                    dict[e] = float(getattr(o, e))
                else:
                    dict[e] = getattr(o, e)
            for c in o.__table__.columns:
                if isinstance(getattr(o, c.name), decimal.Decimal):
                    dict[c.name] = float(getattr(o, c.name))
                else:
                    dict[c.name] = getattr(o, c.name)
            return dict
        except:
            return None


def load_simplified_json(text):
    if ',' not in text:
        return [text]
    elif ':' in text:
        item_list = text.split(',')
        obj = []
        for item in item_list:
            if ':' in text:
                key_value = item.split(':')
                obj.append({key_value[0]: key_value[1]})
        return obj
    else:
        return text.split(',')


class GetInformation(object):

    def __init__(self, id):
        self.id = id
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_birthday(self):
        """通过身份证号获取出生日期"""
        birthday = "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)
        return birthday

    def get_gender(self):
        """男生：1 女生：2"""
        num = int(self.id[16:17])
        if num % 2 == 0:
            return 2
        else:
            return 1

    def get_gender_text(self):
        """男生：1 女生：2"""
        num = int(self.id[16:17])
        if num % 2 == 0:
            return '女'
        else:
            return '男'

    def get_age(self):
        """通过身份证号获取年龄"""
        now = (datetime.datetime.now() + datetime.timedelta(days=1))
        year = now.year
        month = now.month
        day = now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year