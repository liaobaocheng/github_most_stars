from scrapy.utils.project import get_project_settings
import dataset,codecs,os,json


SETTINGS = get_project_settings()


class GithubMostStarsPipeline(object):
    def __init__(self):
        db = dataset.connect('postgresql://liaobaocheng:liaobaocheng@localhost:5432/electron')
        self.table = db['github']


    def process_item(self, item, spider):
        self.table.insert(dict(name=item['name'],url=item['url'],desc=item['desc'],star=item['star']))
        return item


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')
        self.file.write('[')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) +',' "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.write(']')
        self.file.close()
