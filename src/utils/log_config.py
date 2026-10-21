import logging as log

def logging_setup():
    
    log.basicConfig(
        level=log.INFO,
        format= "%(asctime)s / %(levelname)s / %(message)s / %(name)s"
    )