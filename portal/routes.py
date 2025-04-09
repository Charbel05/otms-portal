from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.orm import aliased
import datetime
import psycopg2
import pandas as pd
from portal import app, db, bcrypt
from portal.forms import FormLogin
from portal.models import Location, Obsolescence, Parts, System_groups, User_otms, Rpn, Vendors
from flask_login import current_user, login_required, login_user, logout_user
import portal.queries as queries

from dotenv import load_dotenv
import os
load_dotenv()

def connection(query, option="all"):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DBNAME'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'),
            port=os.getenv('PORT')
        )
        cur = conn.cursor()
        cur.execute(query)

        if option == "one":            
            return cur.fetchone()   # retorna apenas a primeira linha da consulta
        if option == "description":            
            return cur.description  # retorna o nome das colunas da consulta
        else:            
            return cur.fetchall()   # retorna todas as linhas da consulta   
    except Exception as e:
        print("Erro ao conectar com o banco: " + str(e))
    
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Conexão fechada com sucesso!")

@app.route('/', methods=['GET', 'POST'])
def login():
    form_Login = FormLogin()
    if form_Login.validate_on_submit() and "enviar_login" in request.form:
        user = User_otms.query.filter_by(email=form_Login.email.data).first()
        if user:
            # Verifique o tipo de dados da senha armazenada
            senha_armazenada = str(user.password).strip()
            # Verifique o tipo de dados da senha fornecida
            senha_fornecida = str(form_Login.senha.data).strip()
            
            # Verifique se a senha fornecida corresponde à senha armazenada
            if bcrypt.check_password_hash(senha_armazenada, senha_fornecida):
                login_user(user, remember=form_Login.lembrar.data)
                flash("Login realizado com sucesso!", 'alert-success')
                return redirect(url_for('home'))
            else:
                flash("Falha no login!! E-mail ou senha não conferem", 'alert-danger')
        else:
                flash("Falha no login!! E-mail ou senha não conferem", 'alert-danger')

    # # # # #  DESCOMENTAR PARA CADASTRO  # # # # #
    # else:
    #     senha_cript = bcrypt.generate_password_hash("123456").decode('utf-8')
    #     novo_usuario = User_otms(id_user=1, name="adm", email="adm@gmail.com", password=senha_cript, group_loc="adm")
    #     try:
    #         db.session.add(novo_usuario)
    #         db.session.commit()
    #         flash("Cadastro do adm realizado com sucesso!", 'alert-success')
    #         return redirect(url_for('home'))
    #     except Exception as e:
    #         db.session.rollback()
    #         flash(f"Erro ao cadastrar: {str(e)}", 'alert-danger')
    #         return render_template('login.html', form_Login=form_Login)
          

    return render_template('login.html', form_Login=form_Login)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/perfil')
@login_required
def perfil():
    return f"Nome do usuário atual: {current_user.get_name()}"

@app.route('/add-rpn', methods=['GET', 'POST'])
def add_rpn(): 

    # Obtendo o partnumber e, por consequência, o de obsolesce e vendor
    rows_view = connection(queries.query_select_to_add())
    # Obtendo os nomes das colunas
    col = connection(queries.query_select_to_add(), option="description")
    colunas = [descricao[0] for descricao in col]
    # Converte para DF
    options = pd.DataFrame(rows_view, columns=colunas)
    # Elimina as opções nulas, as opções duplicadas e tranforma o dataframe em dicionário
    options.dropna(inplace=True)
    options.drop_duplicates(inplace=True)
    options = options.to_dict(orient='records')

    # Seleciona a tabela de location
    loc = Location.query.order_by(Location.description_category).all()
    loc_dict = [item.to_dict() for item in loc]

    # Seleciona a tabela de System Groups
    sgroup = System_groups.query.order_by(System_groups.id_s_group).all()

    if request.method == 'POST':
        try:   
            part_id = request.form.get('options')
            ci_id = request.form.get('ci_value')
            sa_id = request.form.get('sa_value')
            sc_id = request.form.get('sc_value')
            v_support_id = request.form.get('vendor_support')
            loc_id = request.form.get('loc')
            sgroups_id = request.form.get('sgroup')
            scomplexity_id = request.form.get('system_complexity')
            quantity = request.form.get('quantity')
            description = request.form.get('description')

            # Faz a consulta no banco para saber qual o último id
            last_id = Rpn.query.order_by(Rpn.id_rpn.desc()).first()
            id_rpn = last_id.id_rpn + 1

            # Cria um novo objeto rpn e adiciona 
            new_rpn = Rpn(id_rpn=id_rpn, part_id=part_id, c_impact_id=ci_id, spare_av_id=sa_id, spare_c_id=sc_id, vendorsuport_id=v_support_id, loc_id=loc_id, sgroups_id=sgroups_id, scomplexity_id=scomplexity_id, quantity=quantity, description=description)
            db.session.add(new_rpn)
            db.session.commit()

        except Exception as e:
            flash(f"Erro ao adicionar o item: {str(e)}")
            return render_template('add_rpn.html')

    return render_template('add_rpn.html', options=options, loc=loc_dict, sgroup=sgroup)
        
@app.route('/add-part-number', methods=['GET', 'POST'])
def add_partnumber(): 

    # Seleciona a tabela de Vendor
    vendor = Vendors.query.order_by(Vendors.id_vendors).all()
    # Seleciona a tabela de Obsolescence
    obsolescence = Obsolescence.query.order_by(Obsolescence.level).all()
    
    if request.method == 'POST':
        try: 
            part_number = request.form.get('part_number')
            product = request.form.get('product')
            vendor_id = request.form.get('vendor_id')
            obsolescence_id = request.form.get('obsolescence')
            end_life = request.form.get('end_life')
            # Faz a consulta no banco para saber qual o último id
            last_id = Parts.query.order_by(Parts.id_parts.desc()).first()
            id_parts = last_id.id_parts + 1
            # Cria um novo objeto rpn e adiciona           
            new_part = Parts(id_parts=id_parts, part_number=part_number, product=product, vendor_id=vendor_id, obsolescence_id=obsolescence_id, end_life=end_life, created=datetime.date.today(), modified_by=current_user.get_name())
            db.session.add(new_part)
            db.session.commit()

        except Exception as e:
            flash(f"Erro ao adicionar o part number: {str(e)}")
            return render_template('add_part.html')

        finally:
            return render_template('add_part.html', vendor=vendor, obsolescence=obsolescence)

    return render_template('add_part.html', vendor=vendor, obsolescence=obsolescence)

@app.route('/edit-rpn/<id_rpn>', methods=['GET', 'POST'])
def edit_rpn(id_rpn):

    rpn = db.session.query(Rpn).filter_by(id_rpn=id_rpn).first()
    part = db.session.query(Parts).filter_by(id_parts=rpn.part_id).first()

    vendors_list = db.session.query(Vendors).filter_by().all()
    part_list = db.session.query(Parts).filter_by().all()
    obs = db.session.query(Obsolescence).filter_by().all()
    loc = db.session.query(Location).filter_by().all()
    sgroup = db.session.query(System_groups).filter_by().all()


    if request.method == 'POST':
        try:   
            rpn = db.session.query(Rpn).filter_by(id_rpn=id_rpn).first()
            rpn.c_impact_id = request.form.get('ci_value')
            rpn.spare_av_id = request.form.get('sa_value')
            rpn.spare_c_id = request.form.get('sc_value')
            rpn.scomplexity_id = request.form.get('syc_value')
            rpn.loc_id = request.form.get('loc')
            rpn.part_id = request.form.get('part_number')
            rpn.sgroups_id = request.form.get('sg_value')
            rpn.vendorsuport_id = request.form.get('vendor_suport')
            rpn.description = request.form.get('description')
            rpn.quantity = request.form.get('quantity')

            try:
                # Procura o objeto RPN e filtra o que queremos para realizar o UPDATE 
                db.session.merge(rpn)
                db.session.commit()
                flash("RPN alterado com sucesso!!")
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                print("Erro ao editar: " + str(e))
        except Exception as e:
            db.session.rollback()
            print("Erro ao editar: " + str(e))

    return render_template('edit_rpn.html', rpn=rpn, part=part, vendors_list=vendors_list, part_list=part_list, sgroup=sgroup, obs=obs, loc=loc)

@app.route('/edit-part-number/<partnumber>', methods=['GET', 'POST'])
def edit_part_number(partnumber):

    part = db.session.query(Parts).filter_by(part_number=partnumber).first()
    vendor = db.session.query(Vendors).filter_by().all()
    obsolescence = db.session.query(Obsolescence).filter_by().all()

    if request.method == 'POST':
        try: 
            part_edit = db.session.query(Parts).filter_by(id_parts=part.id_parts).first()
            part_edit.part_number = request.form.get('part_number')
            part_edit.product = request.form.get('product')
            part_edit.vendor_id = request.form.get('vendor_id')
            part_edit.end_life = request.form.get('end_life')

            try:
                db.session.merge(part_edit)
                db.session.commit()
                flash("Part Number alterado com sucesso!", 'sucess')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                print("Erro ao editar: " + str(e))
        except Exception as e:
            db.session.rollback()
            print("Erro ao editar: " + str(e))


    return render_template('edit_part.html', part=part, vendor=vendor, obsolescence=obsolescence)

@app.route('/logout')
def logout():

    logout_user()
    flash("Logout realizado com sucesso!", 'alert-success')
    return redirect(url_for('login'))

@app.route('/last_id')
def get_last_id():
    last_user = Rpn.query.order_by(Rpn.id_rpn.desc()).first()
    if last_user:
        return f"Last user ID: {last_user.id_rpn} "
    else:
        return "No users found"
