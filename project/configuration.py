import ConfigParser
import re,datetime,platform,os
import logging

cp = ConfigParser.SafeConfigParser()
cp.read(os.path.join(os.path.split(__file__)[0],"configuration.conf"))

def platform_detection():
    pattern_platform = re.compile("^[^-]*")
    loc_platform = pattern_platform.findall(platform.platform())
    return loc_platform[0]
# print platform_detection()

#############################################################################################################################        
    
# get blacklist function module
def get_moudle_name():
    moudle_func = cp.get("function_list",'funclist')
    moudle_list = moudle_func.split(',')
    # print moudle_list
    moudle_name = []
    for temp in moudle_list:
        temp = temp.strip()
        moudle_name.append(temp)
    return moudle_name

# print get_moudle_name()

#############################################################################################################################

# Set store path .
def set_data_path():
    if platform_detection() == "Windows":
        data_path = cp.get("Windows_path","data_path")
        if not os.path.isabs(data_path):
            data_path = os.path.abspath(os.path.join(os.path.split(__file__)[0],data_path))
    else:
        data_path = cp.get("Linux_path","data_path")
        if not os.path.isabs(data_path):
            data_path = os.path.abspath(os.path.join(os.path.split(__file__)[0],data_path))
    return data_path

# print set_data_path()

#############################################################################################################################

def set_logger():
    if platform_detection() == "Windows":
        log_path = cp.get("Windows_path","log_path")
        if not os.path.isabs(log_path):
           log_path = os.path.abspath(os.path.join(os.path.split(__file__)[0],log_path))
    else:
        log_path = cp.get("Linux_path","log_path")
        if not os.path.isabs(log_path):
            log_path = os.path.abspath(os.path.join(os.path.split(__file__)[0],log_path))
    logger_info = logging.getLogger('DNS_logs')
    logger_error = logging.getLogger('DNS_logs.error')
    logger_info.setLevel(logging.INFO)
    logger_error.setLevel(logging.ERROR)
    # set logs file handler
    main_logs_handler = logging.FileHandler(os.path.join(log_path,'theat_DNS.log'))
    error_logs_handler = logging.FileHandler(os.path.join(log_path,'theat_DNS-error.log'))
    # set logs formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    main_logs_handler.setFormatter(formatter)
    error_logs_handler.setFormatter(formatter)
    # add handler to logger
    logger_info.addHandler(main_logs_handler)
    logger_error.addHandler(error_logs_handler)

    return logger_info,logger_error

logger_info,logger_error = set_logger()

#############################################################################################################################

def set_frequency():
    frequency_key = cp.options('frequency')
    frequency = []
    for temp in frequency_key:
        frequency.append(cp.get('frequency', temp))

    regex1=re.compile(r'\d+')
    regex2=re.compile(r'[a-zA-Z]+')
    period_num = regex1.findall(frequency[1])[0]
    period_scale = regex2.findall(frequency[1])[0]
    if period_scale == 's'or period_scale == 'S' :
        period  = datetime.timedelta(seconds = int(period_num))
    elif period_scale == 'm'or period_scale == 'M':
        period = datetime.timedelta(minutes = int(period_num))
    elif period_scale == 'd' or period_scale == 'D':
        period = datetime.timedelta(days = int(period_num))
    frequency[1] = period

    if frequency[0] == 'now':
        frequency[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return frequency

# print set_frequency()

#############################################################################################################################

def get_es_config():
    #ES configuration
    ES_key = cp.options("Elasticsearch")
    ES_config = []
    for temp in ES_key:
        ES_config.append(cp.get('Elasticsearch',temp))
    return ES_config

# print get_es_config()

############################################################################################################################





