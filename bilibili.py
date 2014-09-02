#coding:utf-8
import urllib2
import re
import gzip
import StringIO

"""
B站爬虫 - 完结动画
@好个飞飞
"""


# 页数
page_num = 201

# 获取多少观看量以上的动画
look_max_num = 50000

i = 0

dh_get_list = []

while i < page_num:
    i += 1
    print '当前第', i, '页, 总共',  page_num, '页'
    this_url = "http://www.bilibili.com/video/part-twoelement-" + str(i) + ".html"
    data = urllib2.urlopen(this_url).read()
    data = StringIO.StringIO(data)
    gz_page = gzip.GzipFile(fileobj=data)
    html = gz_page.read()

    # print '--------->', html

    #用正则表达式解析
    # re_str = '''title="观看">(.*?)</i><i class="sc'''
    re_str = '''<li class="l1">(.*?)/i>'''
    re_pat = re.compile(re_str)
    dh_list = re_pat.findall(html)

    # print '-------------------------'


    for item in dh_list:
        # print '-------->', item

        look_str = '''title="观看">(.*?)<'''
        look_pat = re.compile(look_str)
        look_list = look_pat.findall(item)

        if str(look_list[0]).find('-') < 0:

            look_num = int(look_list[0])
            if look_num > look_max_num:

                dn_str = '''class="title">(.*?)</a><div'''
                dn_pat = re.compile(dn_str)
                dn_list = dn_pat.findall(item)

                # print '-------->动画名称:', dn_list[0]
                # print '-------->观看数量:', look_list[0]

                dh_get_list.append({'name': dn_list[0], 'look': look_list[0]})


# 排序
dh_get_list.sort(key=lambda obj: int(obj.get('look')), reverse=True)

# for dh in dh_get_list:
#     print '-------->', dh['name'], '观看数量:', dh['look']
#
# print '------->获得动画总数:', len(dh_get_list)

print '------->新建文件写入结果'

# 新建文件写入结果
new_path_filename = "/Users/aaa/Desktop/dh_list.txt"
f = open(new_path_filename, 'w')

for dh in dh_get_list:
    insert_str = str(dh['name']) + '  观看数量:' + str(dh['look']) + '\n'
    f.write(insert_str)

f.close()
