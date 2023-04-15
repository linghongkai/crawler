def start_spider_thread():
    from demo.threads import SpiderThread
    spider_thread = SpiderThread()
    spider_thread.start()
