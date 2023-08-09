"""
@Time   : 2019/5/13
@author : lijc210@163.com
@Desc:  : 功能描述。
"""

from multiprocessing import Pool

from geo import geo

company_address_list = []
with open("company.txt") as f:
    for line in f.readlines():
        line_list = line.replace("\n", "").split("\t")
        company_address_list.append(line_list)


def get(company, address):
    res = geo(address)
    return company, res


if __name__ == "__main__":
    with open("company_res.txt", "a") as f:
        num = len(company_address_list) // 50000 + 1

        for i in range(num):
            print(i)
            tmp_list = company_address_list[i * 50000 : (i + 1) * 50000]
            pool = Pool(5)
            res = pool.starmap(get, tmp_list)
            pool.close()
            pool.join()
            for tmp_list2 in res:
                f.write("\t".join(tmp_list2) + "\n")
