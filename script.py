from app.models import *
from app import db

# client = Client()
# db.session.add(client)
client = Client.query.filter_by(id_client=1).first()

# casa = ModuloPrivado('Casa rod')
casa = ModuloPrivado.query.filter_by(id_modulo_privado=1).first()
# client.component = casa

# usuario = Usuario('rodrigo', 'rodrigondec@gmail.com', 'rodrigo123')
usuario = Usuario.query.filter_by(id_usuario=1).first()
# casa.add_usuario(usuario)

# quarto = ModuloPrivado('Quarto de rods')
quarto = ModuloPrivado.query.filter_by(id_modulo_privado=2).first()
# casa.add_component(quarto)

# leaf = Leaf('Dispositivos do quarto de rods')
leaf = Leaf.query.filter_by(id_leaf=3).first()
# quarto.add_component(leaf)

# embarcado = Embarcado('0.0.0.0', 'ex:abcd:efgh:ijkl')
embarcado = Embarcado.query.filter_by(id_embarcado=1).first()
# leaf.embarcado = embarcado

# sensor = Sensor(13)
sensor = Sensor.query.filter_by(id_sensor=1).first()
# leaf.add_dispositivo(sensor)

# interruptor = Interruptor(12)
interruptor = Interruptor.query.filter_by(id_interruptor=2).first()
# leaf.add_dispositivo(interruptor)
# leaf.alterar_interruptor(interruptor, True)

# potenciometro = Potenciometro(11)
potenciometro = Potenciometro.query.filter_by(id_potenciometro=3).first()
# leaf.add_dispositivo(potenciometro)
# leaf.alterar_potenciometro(potenciometro, 80.5)



# @TODO adicionar regra
# @TODO adicionar monitor

db.session.commit()
