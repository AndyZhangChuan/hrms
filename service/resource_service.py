from commons.utils import to_dict
from data.manager import RichTextMgr, PicMgr


def create_or_update_rich_text(org_id, proj_id, title, text_type, content, sequence=0, subtitle='', rich_text_id=0):
    if rich_text_id:
        rich_text = RichTextMgr.get(rich_text_id)
        RichTextMgr.update(rich_text, title=title, sequence=sequence, rich_text=content, subtitle=subtitle)
    else:
        sequence = RichTextMgr.get_last_sequence_by_type(org_id, proj_id, text_type) + 1
        rich_text = RichTextMgr.create(org_id=org_id, proj_id=proj_id, title=title, text_type=text_type,
                                       sequence=sequence, rich_text=content, subtitle=subtitle)
    return to_dict(rich_text)


def delete_rich_text(rich_text_id):
    rich_text = RichTextMgr.get(rich_text_id)
    if rich_text:
        RichTextMgr.delete(rich_text)


def create_pic(org_id, proj_id, img_type, url, override=False):
    if override:
        PicMgr.clear_pic_list(org_id, proj_id, img_type)
        sequence = 1
    else:
        sequence = PicMgr.get_last_sequence_by_type(org_id, proj_id, img_type) + 1
    return PicMgr.create(org_id=org_id, proj_id=proj_id, img_type=img_type, url=url, sequence=sequence)


def delete_pic(pic_id):
    pic = PicMgr.get(pic_id)
    if pic:
        PicMgr.delete(pic)
