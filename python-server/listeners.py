import os
from logic import mq

LISTENERS = {
    'videos.test':[
        {
            'routing':['videos.general', 'videos.general.app2'], 
            'queue':'app2videosgeneral', 
            'listener':mq.videos_remote.on_message
        },
    ],
    'vuelos.registrar.test':[
        {
            'routing': ['vuelos.registrar', 'vuelos.registrar.app2'],
            'queue': 'v1.TremendaCola',
            'listener': mq.vuelos_registrar_remote.on_message
        }
        #, puedo generar mas colas dependiendo del topic 1 cola por topic
    ],
    'RFC11.test':[
        {
            'routing': ['RFC11', 'RFC11.app2'],
            'queue': 'v2.TremendaCola',
            'listener': mq.RFC11_remote.on_message
        }
        #, puedo generar mas colas dependiendo del topic 1 cola por topic
    ]
}