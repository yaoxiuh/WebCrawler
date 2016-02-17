rm crawler.db
echo "URL='$1'" > crawler/spiders/settings.py
echo "KEYWORD='java'" >> crawler/spiders/settings.py

type=$2
if [ $type = 'bfs' ]; then
  cp crawler/bfs_setting.py crawler/settings.py
else
  cp crawler/dfs_setting.py crawler/settings.py
fi

scrapy crawl crawler
