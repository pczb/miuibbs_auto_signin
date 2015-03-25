import time

def defaultErrorHandler(*args):
    for x in args:
        print x
    pass

def tryExec(tryTimes = 3, errorHandler = defaultErrorHandler, sleepGap = 10):
    def _tryExec(func):
        def __tryExec(*args, **kwargs):
            tryCount = 0
            exceptions = []
            while tryCount < tryTimes:
                try:
                    return func(*args, **kwargs)
                except Exception, e:
                    tryCount += 1
                    time.sleep(sleepGap)
                    exceptions.append(e)
                    raise

            return errorHandler(exceptions)
        return __tryExec
    return _tryExec



