import parser_config, os,sys
from blacklist_tools import *
sys.dont_write_bytecode = True

# 存储原始数据
def get_blacklist_module():
    parse_blacklist = parser_config.blacklist_function
    for file_name in parse_blacklist:
         command = 'python .\get_blacklist\\' + file_name +'.py'
         try:
              status = os.popen(command)
              print status.read()
         except Exception, e:
                print e

def merge_blacklist(dir,date,name):
    parse_blacklist = parser_config.blacklist_function
    i = 0
    merge_result = {}
    for file_name in parse_blacklist:
        result = load_dict(file_name + '.json')
        if i ==0:
            merge_result = result
        else:
            merge_result = update_dict(result,merge_result)
    saveAsJSON(date,merge_result,dir,name)

    for file_name in parse_blacklist:
        if os.path.exists(file_name+'.json'):
            os.remove(file_name+'.json')

#建Trie树

def store_trie(dir, date, name):
    source_store_path =parser_config.source_store_path
    result = load_dict(source_store_path[1] + source_store_path[0] + "-" +date + '.json')
    saveAsJSON(date,create_Trie(result),dir,name)



if __name__ == '__main__':
    source_store_path =parser_config.source_store_path
    trie_store_path = parser_config.trie_store_path
    get_blacklist_module()
    merge_blacklist(source_store_path[1],sys.argv[1],source_store_path[0])
    store_trie(trie_store_path[1],sys.argv[1],trie_store_path[0])


