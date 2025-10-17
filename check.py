import sys,json
d=json.load(sys.stdin)
for x in d:
    print("#{0} uid={1} - {2}".format(x.get("id"), x.get("user_id"), x.get("title")))
