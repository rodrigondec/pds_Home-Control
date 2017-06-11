from flask import render_template, Blueprint, session, abort, flash, redirect, url_for, request
from app.models import *
from app.forms import MonitorForm, RegraTipoDispositivoForm, RegraSensorForm, RegraPotenciometroForm, RegraInterruptorForm

mod_monitor = Blueprint('monitor', __name__, url_prefix='/monitor', template_folder='templates')

@mod_monitor.route('/<id_leaf>')
def monitor(id_leaf):
    if 'logged_in' in session:
        usuario = Usuario.query.filter_by(id_usuario=session['id_usuario']).first()
        leaf = Component.query.filter_by(id_component=id_leaf).first()
        if not leaf.acessivel_por(usuario):
            flash('Você não tem permissão para acessar o monitor desse leaf')
            return redirect('/dashboard/')
        if leaf.monitor is None:
            flash('Cadastre um monitor')
            return redirect('/monitor/cadastrar/'+id_leaf)
        return render_template('monitor/monitor.html/', leaf=leaf)
    else:
        flash('Entre no sistema primeiro!')
        return redirect('/')


@mod_monitor.route('/cadastrar/<id_leaf>', methods=['GET', 'POST'])
def cadastrar_monitor(id_leaf):
    if 'logged_in' in session:
        usuario = Usuario.query.filter_by(id_usuario=session['id_usuario']).first()
        leaf = Component.query.filter_by(id_component=id_leaf).first()
        if not leaf.alteravel_por(usuario):
            flash('Você não tem permissão para cadastrar um monitor para esse leaf')
            return redirect('/dashboard/')

        form = MonitorForm()
        if form.validate_on_submit():
            monitor = eval(form.tipo_monitor.data)(form.nome.data)

            leaf.monitor = monitor

            db.session.add(monitor)
            db.session.commit()
            flash('Monitor criado com sucesso')

            return redirect('/dashboard/leaf/'+id_leaf)
        return render_template('monitor/cadastrar_monitor.html', form=form, leaf=leaf)
    else:
        flash('Entre no sistema primeiro!')
        return redirect('/')


@mod_monitor.route('/cadastrar_regra/<id_monitor>', methods=['GET', 'POST'])
def regra_tipo_dispositivo(id_monitor):
    if 'logged_in' in session:
        usuario = Usuario.query.filter_by(id_usuario=session['id_usuario']).first()
        monitor = Monitor.query.filter_by(id_monitor=id_monitor).first()
        if not monitor.leaf.alteravel_por(usuario):
            flash('Você não tem permissão para cadastrar uma regra para esse monitor')
            return redirect('/dashboard/')

        form = RegraTipoDispositivoForm()
        if form.validate_on_submit():
            return redirect('/monitor/cadastrar_regra/'+id_monitor+'/'+form.tipo_dispositivo.data)
        return render_template('monitor/regra_tipo_dispositivo.html', form=form, monitor=monitor)
    else:
        flash('Entre no sistema primeiro!')
        return redirect('/')


@mod_monitor.route('/cadastrar_regra/<id_monitor>/<tipo_dispositivo>', methods=['GET', 'POST'])
def regra_dispositivo(id_monitor, tipo_dispositivo):
    if 'logged_in' in session:
        usuario = Usuario.query.filter_by(id_usuario=session['id_usuario']).first()
        monitor = Monitor.query.filter_by(id_monitor=id_monitor).first()
        if not monitor.leaf.alteravel_por(usuario):
            flash('Você não tem permissão para cadastrar uma regra para esse monitor')
            return redirect('/dashboard/')

        if tipo_dispositivo == 'sensor':
            form = RegraSensorForm(tipo_dispositivo, monitor.leaf_id)
        elif tipo_dispositivo == 'interruptor':
            form = RegraInterruptorForm(tipo_dispositivo, monitor.leaf_id)
        else:
            form = RegraPotenciometroForm(tipo_dispositivo, monitor.leaf_id)

        if form.validate_on_submit():
            dispositivo = Dispositivo.query.filter_by(id_dispositivo=form.dispositivo.data).first()

            if dispositivo.tipo == 'sensor':
                atuador = Dispositivo.query.filter_by(id_dispositivo=form.atuador.data).first()
                if atuador.tipo == 'interruptor':
                    regra_atuadora = RegraInterruptor(atuador, form.valor_atuador.data)
                else:
                    regra_atuadora = RegraPotenciometro(atuador, form.valor_atuador.data)

                if form.cronometrado.data:
                    regra = RegraSensorCronometrada(dispositivo, form.valor_inicial.data, form.valor_final.data, regra_atuadora, form.hora.data, form.minuto.data)
                else:
                    regra = RegraSensor(dispositivo, form.valor_inicial.data, form.valor_final.data, regra_atuadora)

            elif dispositivo.tipo == 'interruptor':
                if form.cronometrado.data:
                    regra = RegraInterruptorCronometrada(dispositivo, form.valor.data, form.hora.data, form.minuto.data)
                else:
                    regra = RegraInterruptor(dispositivo, form.valor.data)

            else:
                if form.cronometrado.data:
                    regra = RegraPotenciometroCronometrada(dispositivo, form.valor.data, form.hora.data, form.minuto.data)
                else:
                    regra = RegraPotenciometro(dispositivo, form.valor.data)

            monitor.add_regra(regra)
            db.session.commit()
            return redirect('/monitor/' + str(monitor.leaf_id))

        if tipo_dispositivo == 'sensor':
            return render_template('monitor/regra_sensor.html', form=form, monitor=monitor)
        else:
            return render_template('monitor/regra_int_pot.html', form=form, monitor=monitor)
    else:
        flash('Entre no sistema primeiro!')
        return redirect('/')
