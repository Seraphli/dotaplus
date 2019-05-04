from dpapi.dataproc.crawler import Crawler

if __name__ == '__main__':
    print('This may take a lot of time. The debug option is enabled by default.'
          'If you don"t want to see the process, disable debug.')
    debug = True
    Crawler(debug).run()
