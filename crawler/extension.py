class SearchTypeExtension(object):

    def __init__(self, search_type, settings):
        self.search_type = search_type

        if search_type == 'bfs':
            settings['DEPTH_PRIORITY'] = 1
            settings['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeues.PickleFifoDiskQueue'
            settings['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeues.FifoMemoryQueue'


    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        # --------- HOW? ---------------
        # get the user's dfs/bfs setting
        search_type = 'dfs'

        # instantiate the extension object
        ext = cls(search_type, settings)


