from channels.routing import route

channel_routing = [
    route("websocket.connect", "overlay_content.consumers.ws_connect"),
    route("websocket.disconnect", "overlay_content.consumers.ws_disconnect"),
]
