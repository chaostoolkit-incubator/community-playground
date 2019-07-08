import platform

import cherrypy


class Root:
    @cherrypy.expose
    def index(self) -> str:
        return "Hello world from {}".format(platform.node())


if __name__ == "__main__":
    cherrypy.config.update({
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 8080
    })
    cherrypy.quickstart(Root())

