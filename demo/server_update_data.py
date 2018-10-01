import time


def update_data():
    from dataproc.web_data import WebData
    print('{}, Update data'.format(time.time()))
    wd = WebData()
    wd.crawl_data()
    print('{}, Update complete'.format(time.time()))


if __name__ == '__main__':
    import multiprocessing as mp

    while True:
        p = mp.Process(target=update_data)
        p.start()
        p.join()
        time.sleep(43200)
