#! /usr/bin/python3


"""
Ejercicio de cachés de SARO
X-Serv-App-Cache-Anotada

Ejercicio de asignaturas de aplicaciones web. Servicios que interoperan. Cache de contenidos anotado
Enunciado

Construir una aplicación como "Cache de contenidos", pero que anote cada página, en
la primera línea, con un enlace a la página original, y que incluya también un enlace para
 ``recargar'' la página (volverla a refrescar a partir del original), otro enlace para ver
 el HTTP (de ida y de vuelta, si fuera posible) que se intercambió para conseguir la página original,
y otro enlace para ver el HTTP de la consulta del navegador y de la respuesta del servidor
al pedir esta página (de nuevo si fuera posible)
"""

import webapp
import urllib.request

class cacheApp(webapp.webApp):
    cachedicc = {}

    def parse(self, request):
        troceado = request.split()
        verb = troceado[0]
        recurso = troceado[1][1:]
        return (verb, recurso)
    def process(self, parsedRequest):
        """
        tiene que devolver
        código y respuesta html
        """

        print(parsedRequest)
        verb, recurso = parsedRequest
        if verb == 'GET':
            if recurso.split("/")[0] == "reload":
                url = recurso.split("/")[1]
                url = "http://" + url
                httpCode = "302"
                htmlBody = ("<meta http-equiv='refresh' content=3;url=" +
                            url + ">")
            else:
                try:
                    if recurso in self.cachedicc:
                        httpCode = '200 OK'
                        htmlBody = self.cachedicc[recurso]
                    else:
                        url = 'http://'+recurso
                        print('URL anotada: '+url)
                        httpCode = '200 OK'
                        links = ("<a href=" + url + ">Pagina original</a>" +
                                   "<a href=/reload/" + recurso +
                                   "> Reload </a>")
                        htmlBody = ('<html><p>'+links+'</p></html>')
                except urllib.error.URLError:
                    httpCode = "404 Not Found"
                    htmlBody = "No se ha introducido ninguna URL"
                except UnicodeDecodeError:
                    httpCode = "404 Not Found"
                    htmlBody = "Error al decodificar"
        else:
            httpCode = '405 Method Not Allowed'
            htmlBody = ('<html><h1>405 Method Not Allowed</h1><br>'+
                        '<p>Valid methods: GET</p></html>')
            print('Method ' + verb + ' not allowed')
        return (httpCode, htmlBody)







if __name__ == '__main__':
    myapp = cacheApp('localhost', 8080)
