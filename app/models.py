from app import db

# Many-to-many helper tables (for public access, use models only) -----------

modulo_usuario = db.Table(
    'modulo_usuario',
    db.Column(
        'id_modulo_privado',
        db.Integer,
        db.ForeignKey('modulo_privado.id_modulo_privado')
    ),
    db.Column(
        'id_usuario',
        db.Integer,
        db.ForeignKey('usuario.id_usuario')
    )
)

modulo_component = db.Table(
    'modulo_component',
    db.Column(
        'id_modulo',
        db.Integer,
        db.ForeignKey('modulo.id_modulo')
    ),
    db.Column(
        'id_component',
        db.Integer,
        db.ForeignKey('component.id_component'),
        unique=True
    )
)


# Models and their simple relantionships -------------------------------------


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(64))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


class Client(db.Model):
    __tablename__ = 'client'
    id_client = db.Column(db.Integer, primary_key=True)

    component_id = db.Column(db.Integer, db.ForeignKey('component.id_component'))
    component = db.relationship("Component", uselist=False)


class Component(db.Model):
    __tablename__ = 'component'
    id_component = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))

    tipo = db.Column(db.String(30))
    __mapper_args__ = {'polymorphic_on': tipo}

    def __init__(self, nome):
        if self.__class__ is Dispositivo:
            raise TypeError('abstract class cannot be instantiated')
        self.nome = nome


class Leaf(Component):
    __tablename__ = 'leaf'
    id_leaf = db.Column(db.Integer(), db.ForeignKey("component.id_component", ondelete="CASCADE"), primary_key=True)

    embarcado = db.relationship("Embarcado", uselist=False, back_populates="leaf")

    dispositivos = db.relationship("Dispositivo", back_populates="leaf")

    usos = db.relationship("Uso", back_populates="leaf")

    monitor = db.relationship("Monitor", uselist=False, back_populates="leaf")

    __mapper_args__ = {'polymorphic_identity': __tablename__}

    def __init__(self, nome):
        Component.__init__(self, nome)

    def add_uso(self, uso):
        if uso in self.usos:
            raise Exception("Component duplicado")
        self.usos.append(uso)

    def add_dispositivo(self, dispositivo):
        if dispositivo in self.dispositivos:
            raise Exception("Component duplicado")
        self.dispositivos.append(dispositivo)

    def remove_dispositivo(self, dispositivo):
        self.dispositivos.remove(dispositivo)


class Modulo(Component):
    __tablename__ = 'modulo'
    id_modulo = db.Column(db.Integer(), db.ForeignKey("component.id_component"), primary_key=True)

    components = db.relationship(
        'Component',
        secondary=modulo_component,
        backref=db.backref('component_modulo', lazy='dynamic')
    )

    __mapper_args__ = {'polymorphic_identity': __tablename__}

    def __init__(self, nome):
        Component.__init__(self, nome)

    def add_component(self, component):
        if component in self.components:
            raise Exception("Component duplicado")
        self.components.append(component)

    def remove_component(self, component):
        self.components.remove(component)


class ModuloPrivado(Modulo):
    __tablename__ = 'modulo_privado'
    id_modulo_privado = db.Column(db.Integer(), db.ForeignKey("modulo.id_modulo"), primary_key=True)

    usuarios = db.relationship(
        'Usuario',
        secondary=modulo_usuario,
        backref=db.backref('modulos', lazy='dynamic')
    )

    __mapper_args__ = {'polymorphic_identity': __tablename__}

    def __init__(self, nome):
        Component.__init__(self, nome)

    def add_usuario(self, usuario):
        if usuario in self.usuarios:
            raise Exception("Usuário duplicado")
        self.usuarios.append(usuario)

    def remove_usuario(self, usuario):
        self.usuarios.remove(usuario)

    def add_component(self, component):
        if component in self.components:
            raise Exception("Component duplicado")
        self.components.append(component)

    def remove_component(self, component):
        self.components.remove(component)


class Embarcado(db.Model):
    __tablename__ = 'embarcado'
    id_embarcado = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15))
    mac = db.Column(db.String(20))

    leaf_id = db.Column(db.Integer, db.ForeignKey('leaf.id_leaf'))
    leaf = db.relationship("Leaf", back_populates="embarcado")

    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac


class Dispositivo(db.Model):
    __tablename__ = 'dispositivo'
    id_dispositivo = db.Column(db.Integer, primary_key=True)
    porta = db.Column(db.Integer)

    leaf_id = db.Column(db.Integer, db.ForeignKey('leaf.id_leaf'))
    leaf = db.relationship("Leaf", back_populates="dispositivos")

    usos = db.relationship("Uso", back_populates="dispositivo")

    regras = db.relationship("Regra", back_populates="dispositivo")

    tipo = db.Column(db.String(30))
    __mapper_args__ = {'polymorphic_on': tipo}

    def __init__(self, porta):
        if self.__class__ is Dispositivo:
            raise TypeError('abstract class cannot be instantiated')
        self.porta = porta


class Sensor(Dispositivo):
    __tablename__ = 'sensor'
    id_sensor = db.Column(db.Integer(), db.ForeignKey("dispositivo.id_dispositivo"), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': __tablename__}

    def __init__(self, porta):
        Dispositivo.__init__(self, porta)


class Interruptor(Dispositivo):
    __tablename__ = 'interruptor'
    id_interruptor = db.Column(db.Integer(), db.ForeignKey("dispositivo.id_dispositivo"), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': __tablename__}

    def __init__(self, porta):
        Dispositivo.__init__(self, porta, self.__tablename__)


class Potenciometro(Dispositivo):
    __tablename__ = 'potenciometro'
    id_potenciometro = db.Column(db.Integer(), db.ForeignKey("dispositivo.id_dispositivo"), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': __tablename__}

    def __init__(self, porta):
        Dispositivo.__init__(self, porta, self.__tablename__)


class Uso(db.Model):
    __tablename__ = 'uso'
    id_uso = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.DateTime, default=db.func.now())

    leaf_id = db.Column(db.Integer, db.ForeignKey('leaf.id_leaf'))
    leaf = db.relationship("Leaf", back_populates="usos")

    dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivo.id_dispositivo'))
    dispositivo = db.relationship("Dispositivo", back_populates="usos")
    comando = db.Column(db.String(30))
    hora = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, status):
        TemplateStatus.__init__(self, status)


class Regra(db.Model):
    __tablename__ = 'regra'
    id_regra = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30))

    dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivo.id_dispositivo'))
    dispositivo = db.relationship("Dispositivo", back_populates="regras")

    monitor_id = db.Column(db.Integer, db.ForeignKey('monitor.id_monitor'))
    monitor = db.relationship("Monitor", back_populates="regras")

    tipo = db.Column(db.String(30))
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': tipo
    }

    def __init__(self, status):
        self.status = status


class RegraCronometrada(Regra):
    __tablename__ = 'regra_cronometrada'
    id_regra_cronometrada = db.Column(db.Integer(), db.ForeignKey("regra.id_regra"), primary_key=True)
    hora = db.Column(db.DateTime)

    __mapper_args__ = {'polymorphic_identity': __tablename__}

    def __init__(self, hora, status):
        Regra.__init__(self, status)
        self.hora = hora


class RegraConometradaInterruptor(RegraCronometrada):
    __tablename__ = 'monitor'
    id_monitor = db.Column(db.Integer, primary_key=True)
    leaf_id = db.Column(db.Integer, db.ForeignKey('leaf.id_leaf'))
    leaf = db.relationship("Leaf", back_populates="monitor")
    regras = db.relationship("Regra", back_populates="monitor")

    def __init__(self, nome):
        TemplateName.__init__(self, nome)
