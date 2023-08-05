
from app.plugins.common import settings, smart_database 

cunnrent_setting = settings.librarys.rtst



# def find(s, step=0, **kwargs):
#     try:
#         memory_name = kwargs.get('memory_name', 'default')
#         query = f"""{s}\ncollection='doc2vec' and sr='{memory_name}'\ndocument,sr,metadatas\n{cunnrent_setting.count}"""
#         result = smart_database.get(query)
#         select_cols = ['title', 'content', 'score']
#         docs = []
#         if len(result) > 1:
#             result[0][result[0].index("sr")] = "source"
#             result = list(map(lambda x: dict(zip(result[0], x)), result[1:]))
#             for idx, _ in enumerate(result):
#                 result[idx]['content'] = result[idx].get("document", "")
#                 if "metadatas" in result[idx]:
#                     result[idx]['metadatas'] = json.loads(result[idx]['metadatas'])
#                     result[idx]['title'] = memory_name + "/" + result[idx]['metadatas'].get("source", "")
#                     result[idx]['title'] = result[idx]['title'].strip("/")
#                 result[idx]['score'] = round(result[idx].get('distance', 0), 4)
#             docs = list(map(lambda x: {k: x[k] for k in select_cols if k in x}, result))
#         return docs
#     except Exception as e:
#         print(e)
#         return []

def find(s, step=0, **kwargs):
    from app.models import UserProfile, Collections
    request = kwargs.get('request')
    collection = request.get('collection')
    if collection:
        collection = Collections.objects.filter(code=collection)
        if collection:
            collection = collection[0]
            if not collection.users.all().filter(username=request['username']):
                return []
    else:
        profile = UserProfile.objects.filter(fromUser__username=request['username'])
        if profile:
            profile = profile[0]
        else:
            return []
        collection = profile.collection
    if collection.is_where and collection.remark:
        where = collection.remark
    else:
        where = f"collection='{collection.code}'"
    memory_name = collection.name
    # try:
    if not where:
        where = "collection='default'"
    query = f"""{s}\n{where}\ndocument,sr,m\n{cunnrent_setting.count}"""
    result = smart_database.get(query)
    select_cols = ['title', 'content', 'score']
    docs = []
    if len(result) > 1:
        result[0][1] = "title"
        result = list(map(lambda x: dict(zip(result[0], x)), result[1:]))
        for idx, _ in enumerate(result):
            result[idx]['title'] = memory_name + '/' + result[idx]['title']
            result[idx]['content'] = result[idx].get("document", "")
            result[idx]['score'] = round(result[idx].get('distance', 0), 4)
        docs = list(map(lambda x: {k: x[k] for k in select_cols if k in x}, result))
    return docs
    # except Exception as e:
    #     print(e)
    #     return []


def add(collection, sr, documents: list, **kwargs):
    smart_database.add(collection, sr, documents, **kwargs)

def clear(collection, owner):
    smart_database.clear(collection, owner)