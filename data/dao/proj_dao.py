# coding=utf-8
from commons.utils import to_dict, time_util
from data.manager import PicMgr, RichTextMgr, PluginMgr
from data.manager.proj import ProjMgr, ProjOfferMgr


class ProjDao:
    @staticmethod
    def add_logo_url(org_id, data):
        """
        获取项目logo图片链接
        """
        logo_pic = PicMgr.get_img_by_type(org_id, data['id'], 'logo')
        data['logo_url'] = logo_pic[0].url if len(logo_pic) else ''

    @staticmethod
    def add_intro_list_pics(org_id, proj_id, data):
        """
        获取项目介绍图片链接列表，格式为{url: 'xx', id: '1'}
        """
        intro_pic_list = PicMgr.get_img_by_type(org_id, proj_id, 'intro')
        result = []
        for item in intro_pic_list:
            result.append({'url': item.url, 'id': item.id})
        data['intro_list_pics'] = result

    @staticmethod
    def add_recruit_post_details(org_id, proj_id, post_id, data):
        """
        获取项目招工贴中的招工详情介绍，为富文本+图片集的形式
        """
        rich_text_list = RichTextMgr.get_richtext_by_type(org_id, proj_id, 'proj_recruit_detail' + '_post'+post_id)
        result = []
        for item in rich_text_list:
            rich_text = to_dict(item)
            intro_pic_list = PicMgr.get_img_by_type(org_id, proj_id, item.title + '_post'+post_id)
            rich_text['pic_list'] = []
            for pic in intro_pic_list:
                rich_text['pic_list'].append({'url': pic.url, 'id': pic.id})
            result.append(rich_text)
        data['recruit_post_details'] = result

    @staticmethod
    def add_recruit_post_highlight(org_id, proj_id, post_id, data):
        """
        获取项目招工贴中的高亮信息，为富文本+图片集的形式， 范围一个dict
        """
        rich_text = RichTextMgr.query_first({'org_id': org_id, 'proj_id': proj_id, 'text_type': 'proj_highlight' + '_post'+post_id},
                                            order_list=[RichTextMgr.model.sequence.desc()])
        if not rich_text:
            return None
        rich_text = to_dict(rich_text)
        intro_pic_list = PicMgr.query({'org_id': org_id, 'proj_id': proj_id, 'img_type': 'proj_highlight' + '_post'+post_id},
                                      order_list=[PicMgr.model.sequence.desc()])
        rich_text['pic_list'] = []
        for pic in intro_pic_list:
            rich_text['pic_list'].append({'url': pic.url, 'sequence': pic.sequence})
        data['recruit_post_highlight'] = rich_text

    @staticmethod
    def add_update_time_str(data):
        """
        获取更新时间字段
        """
        if 'update_time' in data:
            data['update_time_str'] = data['update_time'].strftime("%Y-%m-%d")

    @staticmethod
    def add_start_time_str(data):
        """
        获取开始时间字段
        """
        if 'start_time' in data:
            data['start_time_str'] = time_util.timestamp2dateString(data['start_time'])

    @staticmethod
    def add_end_time_str(data):
        """
        获取结束时间字段
        """
        if 'end_time' in data:
            data['end_time_str'] = time_util.timestamp2dateString(data['end_time'])

    @staticmethod
    def add_offer_type_str(data):
        """
        获取报价单类型字段
        """
        if 'offer_type' in data:
            data['offer_type_str'] = '员工到手' if data['offer_type'] == 0 else '供应商应收'

    @staticmethod
    def add_offer_plugins(data):
        """
        获取工资规则插件
        """
        if 'id' in data:
            plugins = PluginMgr.query({'module_type': 'offer', 'module_id': data['id'], 'is_del': 0})
            data['plugins'] = to_dict(plugins)

    @staticmethod
    def list_proj(org_id, page, page_size=10):
        """获取项目列表并分页"""
        filter_condition = {'is_del': 0, 'org_id': org_id}
        count = ProjMgr.count(filter_conditions=filter_condition)
        if page_size > 5000:
            page_size = 5000
        records = ProjMgr.query(filter_conditions=filter_condition, limit=page_size,
                                offset=(page - 1) * page_size, order_list=[ProjMgr.model.create_time.desc()])
        return {'total_count': count, 'datas': to_dict(records)}

    @staticmethod
    def get_proj_by_id(proj_id):
        """通过项目id获取单个项目"""
        return to_dict(ProjMgr.get(proj_id))

    @staticmethod
    def list_proj_offers(proj_id, page, page_size=10):
        """获取项目列表并分页"""
        filter_condition = {'is_del': 0, 'proj_id': proj_id}
        count = ProjOfferMgr.count(filter_conditions=filter_condition)
        if page_size > 5000:
            page_size = 5000
        records = ProjOfferMgr.query(filter_conditions=filter_condition, limit=page_size,
                                     offset=(page - 1) * page_size, order_list=[ProjOfferMgr.model.start_time.desc()])
        return {'total_count': count, 'datas': to_dict(records)}