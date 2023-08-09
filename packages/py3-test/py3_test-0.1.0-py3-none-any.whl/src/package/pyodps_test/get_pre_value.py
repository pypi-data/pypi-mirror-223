from odps.distcache import get_cache_table
from odps.udf import annotate


@annotate("int,int")
class GetPreValue(object):
    # 将表数据加载到内存中
    def __init__(self):
        pass
        # self.records = list(get_cache_table("data_kezhi.ods_gq_ht_ac_contract"))
        # self.d1 = {}
        # for row in self.records:
        #     _id, pid = row[0], row[1]
        #     self.d1[_id] = pid

    def evaluate(self, id, pid):
        old_id = self.getPid(self, id, pid)
        return old_id

    def getPid(self, _id, pid):
        old_pid = self.d1.get(_id)
        if old_pid == 0:
            new_id = _id
        else:
            new_id = self.getPid(old_pid, pid)
        return new_id


if __name__ == "__main__":
    pass
