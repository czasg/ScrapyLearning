# crontab -e
# 0 6 * * * /onlineSpider/czaSpider/task.sh ziru

python3 command.py czaSpider.spiders.online.$1 cza_run_spider --myspider