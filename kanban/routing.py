from channels.routing import route

# 先ほど作った sample/consumers.py から引っ張ってきてるだけ
from kanban.views import ws_add, ws_disconnect

channel_routing = [
    # path を指定する 127.0.0.1:8000/ws に繋げるという感じ
    route("websocket.connect", ws_add, path=r'^/ws$'),
    route("websocket.disconnect", ws_disconnect),
]
