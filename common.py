
# Login MQTT
# CODE = "VH001"
# USERNAME = "vehicle_1"
CODE = "VH002"
USERNAME = "vehicle_2"
PASSWORD = "Aa123456789"
HOST = "96cd623ad07c45fb886782e9f77079d2.s1.eu.hivemq.cloud"
PORT = 8883

# URL call API
# API_ENDPOINT = "http://localhost:8080"
API_ENDPOINT = "http://scmavrapi-env.eba-zkmkumcj.ap-southeast-1.elasticbeanstalk.com"

URI_SEND_NOTI = "/api/vehicle/login"
URI_START_DELIVERY = "/api/vehicle/start-delivery-order"
URI_ARRIVED = '/api/vehicle/arrived'
URI_TRACKING = '/api/vehicle/tracking'
URI_GO_TO_HOME = '/api/vehicle/go-to-home'
URI_FINISH = '/api/vehicle/finish'
URI_SOS = '/api/vehicle/sos'