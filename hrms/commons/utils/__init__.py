# -*- encoding: utf8 -*-

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
