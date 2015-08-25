# coding=utf-8
#
# Template by @ALEJANDROJ19
# https://github.com/ALEJANDROJ19
# Original from: https://github.com/yukuku/telebot
#
# TELEGRAM BOT Template v1
# Plantilla de un bot simple para Telegram.

import StringIO
import json
import logging
import random
import urllib
import urllib2
from time import strftime, gmtime

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

from tocken import BASE_URL

# ================================
# No tocar esto!

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================
# No tocar esto!
def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()


def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


def foo():
    logging.error('No hay funcionalidad implementada')
    return

# ================================
# No tocar esto!
class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))

##########################################

class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))


        # IMPORTANTE: Cambiar esto!
        self_id = '@UserNamedetuBot'
        self_name = 'NombredetuBot'

        indiscreto = False  # Poner a True si queremos interactuar con mensajes destinados a otras personas.

        # Variables del programa.
        msg_destinado = True
        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        fr = message.get('from')
        text = message.get('text')
        chat = message['chat']
        chat_id = chat['id']


        username = fr.get('username')
        nombre = fr.get('first_name')
        apellido = fr.get('last_name')
        _text = message.get('from')
        _sticker = message.get('sticker')
        _photo = message.get('photo')
        _location = message.get('location')
        _document = message.get('document')
        _audio = message.get('audio')
        _contact = message.get('contact')



            ##################################
            #                                #
            #    Definición de Funciones     #
            #                                #
            ##################################

        def enviar(msg=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg,
                    'disable_web_page_preview': 'true',
                })).read()
            else:
                logging.error('No se ha especificado ningún mensaje!')
                resp = None

            logging.info('Respuesta enviada:')
            logging.info(resp)

        def sticker(sticker_id=None):
            if sticker_id:
                resp = urllib2.urlopen(BASE_URL + 'sendSticker', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'sticker': sticker_id
                })).read()
            else:
                logging.error('No se ha especificado ningún sticker!')
                resp = None
            logging.info('Respuesta enviada:')
            logging.info(resp)

        def responder(msg=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg,
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            else:
                logging.error('No se ha especificado ningún mensaje!')
                resp = None

            logging.info('Respuesta enviada:')
            logging.info(resp)

            ##################################
            #                                #
            #     Definición de Comandos     #
            #                                #
            ##################################


        if _sticker:
            # Programar que hacer cuando se recibe un sticker.
            foo()
            return  # No quitar este return
        elif _audio:
            # Programar que hacer cuando se recibe un audio.
            foo()
            return  # No quitar este return
        elif _document:
            # Programar que hacer cuando se recibe un documento/foto sin comprimir.
            foo()
            return  # No quitar este return
        elif _location:
            # Programar que hacer cuando se recibe una localización.
            foo()
            return  # No quitar este return
        elif _photo:
            # Programar que hacer cuando se recibe una foto (comprimida).
            foo()
            return  # No quitar este return
        elif _contact:
            # Programar que hacer cuando se recibe un contacto.
            foo()
            return  # No quitar este return
        elif _text:
            # Programar que hacer cuando se recibe un texto.
            text = text.lower()  # Todos los textos recividos se leerán en minusculas.
            # Filtro de menciones: Si un usuario está mencionando a otro bot/usuario, podemos configurar
            # como se va a comportar nuestro bot en función de lo que queramos.
            if text.startswith('@') and not text.startswith(self_id):
                if not indiscreto:
                    logging.info('Este mensaje es un mensaje para otra persona. El modo indiscreto está desactivado.')
                    return
                else:
                    msg_destinado = False

            # COMANDOS DEL BOT: Impementar aqui todos los comandos que queremos reconocer.
            # Este bot solo ejecutará comandos los cuales hayan sido escritos con una '/' delante
            # del texto. Solo ejecutará comandos que sean dirigidos para él.
            # Telegram destinará los comandos seguidos del username del bot a ese bot. Es decir, el comando
            # /start@1bot solo será enviado al @bot1, mientras que @bot2 no lo leerá.
            if text.startswith('/'):
                if '/start' in text:
                    enviar('Bot encendido. Modo de captura de frases encendido.')
                    setEnabled(chat_id, True)
                elif '/stop' in text:
                    enviar('Bot desactivado. Modo de captura de frases desactivado.')
                    setEnabled(chat_id, False)
                elif '/help' in text:
                    enviar('Comandos disponibles:\n'
                          '- /comando1 - Descripción.\n'
                          '- /comando2 - Descripción.\n'
                          '- etc...')
                elif '/comando1' in text:
                    enviar('Contestación1')
                else:
                    enviar('Comando no reconocido.')

            # MENSAJES DEL USUARIO: Implementar aqui todas las acciones a realizar por el bot al reconocer
            # un texto/palabra/dijito/mención que se quiera. Hay que tener en cuenta que la privacidad del bot
            # tiene que estar habilitada para poder leer estos mensajes en caso de insertar el bot en un grupo.
            # Para esto, se ha de configurar desde el @BotFather.
            elif 'texto de ejemplo' in text:
                enviar('He reconocido en lo que me has enviado \'texto de ejemplo\'')
            elif 'que hora es' in text:
                dia = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
                enviar(dia)
            elif 'quien soy' in text:
                repl = ''
                repl += 'Te llamas ' + nombre + ' ' + apellido + '. '
                if username:
                    repl += 'Tu username es: @' + username
                else:
                    repl += 'No tienes actualmente un username!'
                enviar(repl)
            else:
                # En caso de no tener una respuesta programada para el mensaje reconocido, se puede crear un caso
                # general de una respuesta (por ejemplo: "No se que contestarte a eso.") o implementar cualquier
                # otra cosa. Por ejemplo, aqui está implementado un generador de respuestas por internet.

                # Si se quiere programar otra cosa, quitar este bloque
                if getEnabled(chat_id):
                    try:
                        resp1 = json.load(urllib2.urlopen('http://www.simsimi.com/requestChat?lc=en&ft=1.0&req=' + urllib.quote_plus(text.encode('utf-8'))))
                        back = resp1.get('res')
                    except urllib2.HTTPError, err:
                        logging.error(err)
                        back = str(err)
                    if not back:
                        enviar('okay...')
                    elif 'I HAVE NO RESPONSE' in back:
                        enviar('No se que contestar a eso que me has enviado, lo siento.')
                    else:
                        enviar(back)
                else:
                    logging.info('No puedes enviar mensajes en este chat! chat_id {}'.format(chat_id))
                # Quitar hasta aqui.

            return
        else:
            # ERROR: Tipo recibido desconocido
            logging.error('ERROR: Tipo recibido no reconocido!')
            return



# Comandos internos, no tocar.
app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
