import ConfigParser
import re,datetime
import logging

cp = ConfigParser.SafeConfigParser()

cp.read("blacklist_match.conf")
sections =  cp.sections()

#############################################################################################################################

parse_blacklist_key = cp.options(sections[0])

#function module
moudle_func = cp.get("parse_blacklist", parse_blacklist_key[0])
moudle_list = moudle_func.split(',')
# print moudle_list
moudle_name = []
for temp in moudle_list:
    temp = temp.strip()
    moudle_name.append(temp)
# print moudle_name

#############################################################################################################################

#source_data_path
source_store_path_key = cp.options(sections[1])
source_store_path = []
for temp in source_store_path_key:
    source_store_path.append(cp.get('source_store_path', temp))

#############################################################################################################################

#trie_store_path
trie_store_path_key = cp.options(sections[2])
trie_store_path  = []
for temp in trie_store_path_key:
    trie_store_path.append(cp.get('Trie_store_path', temp))

#############################################################################################################################

#cun period
frequency_key = cp.options(sections[3])
frequency = []
for temp in frequency_key:
    frequency.append(cp.get('frequency', temp))

# print frequency
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

#############################################################################################################################

#ES configuration
ES_key = cp.options(sections[4])
ES_config = []
for temp in ES_key:
    ES_config.append(cp.get('ES_config',temp))

############################################################################################################################

# logging config
logs_key = cp.options(sections[5])
logs_path = cp.get('logs_path',logs_key[0])
# create logger
logger_info = logging.getLogger('DNS_logs')
logger_error = logging.getLogger('DNS_logs.error')
logger_info.setLevel(logging.INFO)
logger_error.setLevel(logging.ERROR)
# set logs file handler
main_logs_handler = logging.FileHandler(logs_path+'theat_DNS.log')
error_logs_handler = logging.FileHandler(logs_path+'theat_DNS-error.log')
# set logs formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
main_logs_handler.setFormatter(formatter)
error_logs_handler.setFormatter(formatter)
# add handler to logger
logger_info.addHandler(main_logs_handler)
logger_error.addHandler(error_logs_handler)

#############################################################################################################################
