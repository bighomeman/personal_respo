import ConfigParser

cp = ConfigParser.SafeConfigParser()

cp.read("blacklist_match.conf")
sections =  cp.sections()
# print sections[0]
parameter = cp.options(sections[0])
# print type(parameter[0])
# print 'items of [ssh]:', cp.items('parse_blacklist')    # items of [ssh]: [('host', '192.168.1.101'), ('user', 'huey'), ('pass', 'huey')]
# print cp.get("parse_blacklist", parameter[0])