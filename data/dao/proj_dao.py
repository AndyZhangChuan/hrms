# coding=utf-8
from commons.utils import to_dict
from data.manager.proj import ProjMgr, ProjPicMgr


class ProjDao:
    @staticmethod
    def add_logo_url(proj_id, data):
        """
        获取项目logo图片链接
        """
        logo_pic = ProjPicMgr.get_img_by_type(proj_id, 'logo')
        data['logo_url'] = logo_pic[0].url if len(logo_pic) else ''

    @staticmethod
    def add_intro_list_pics(proj_id, data):
        """
        获取项目介绍图片链接列表，格式为{url: 'xx', id: '1'}
        """
        intro_pic_list = ProjPicMgr.get_img_by_type(proj_id, 'intro')
        result = []
        for item in intro_pic_list:
            result.append({'url': item.url, 'id': item.id})
        data['intro_list_pics'] = result

    @staticmethod
    def add_update_time_str(data):
        """
        获取更新时间字段
        """
        if 'update_time' in data:
            data['update_time_str'] = data['update_time'].strftime("%Y-%m-%d")

    @staticmethod
    def list_proj(company_id, page, page_size=10):
        """获取项目列表并分页"""
        return to_dict(ProjMgr.query({'company_id': company_id, 'is_del': 0},
                                     order_list=[ProjMgr.model.create_time.desc()],
                                     offset=(page-1)*page_size, page_size=page_size))

    @staticmethod
    def get_proj_by_id(proj_id):
        """通过项目id获取单个项目"""
        return to_dict(ProjMgr.get(proj_id))