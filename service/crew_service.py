# coding=utf-8
import json

from data.manager import CrewMgr, CrewProjMapMgr, CrewLevelMgr


def create_crew_record(proj_id, lines):
    line_index = 0
    for line in lines:
        line_index += 1
        record = {'proj_id': proj_id, 'meta': {}}
        for key, value in line.items():
            line[key] = value.strip()
            if key in CrewMgr.params:
                record[key] = value
            else:
                record['meta'][key] = value
        record['id_card_num'] = record['id_card_num'].lower()
        record['meta'] = json.dumps(record['meta'])
        crew = CrewMgr.create_override_if_exist(record)
        level = CrewLevelMgr.query_first({'crew_id': crew.id, 'is_del': 0})
        if not level:
            CrewLevelMgr.create(crew_id=record['crew_id'], crew_name=record['crew_name'], level_name='青铜')


def update_crew_records(crew_id, content):
    crew = CrewMgr.get(crew_id)
    if crew:
        CrewMgr.update(crew, **content)


def delete_crew_record(crew_id):
    record = CrewMgr.get(crew_id)
    if record:
        CrewMgr.delete(record)
