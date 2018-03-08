import ConfigParser

cp = ConfigParser.SafeConfigParser()

cp.read("blacklist_match.conf")
sections =  cp.sections()
# print sections[0]
parse_blacklist = cp.options(sections[0])
# print type(parameter[0])
# print 'items of [ssh]:', cp.items('parse_blacklist')    # items of [ssh]: [('host', '192.168.1.101'), ('user', 'huey'), ('pass', 'huey')]
blacklist_function = []
for temp in parse_blacklist:
    blacklist_function.append(cp.get("parse_blacklist", temp))

source_store_path_key = cp.options(sections[1])
source_store_path = []
for temp in source_store_path_key:
    source_store_path.append(cp.get('source_store_path', temp))


trie_store_path_key = cp.options(sections[2])
trie_store_path  = []
for temp in trie_store_path_key:
    trie_store_path.append('Trie_store_path', temp)