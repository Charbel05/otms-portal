from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename
import datetime
import psycopg2
from portal import app, db, bcrypt
from portal.forms import FormAddVendor, FormEditRPN, FormLogin, FormAddPartNumber, FormRPN
from portal.models import Almox, Location, Manufactoring_unit, Obsolescence, Parts, Region, System_groups, User_otms, Rpn, Vendors
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
@login_required
def home():
    return render_template('home.html')

@app.route('/perfil')
@login_required
def perfil():
    return f"Nome do usuário atual: {current_user.get_name()}"

@app.route('/add-rpn', methods=['GET', 'POST'])
@login_required
def add_rpn(): 
    formItem = FormRPN()

    vendor_alias = aliased(Vendors)
    obsolescence_alias = aliased(Obsolescence)
    parts = db.session.query(Parts, vendor_alias, obsolescence_alias).join(vendor_alias, Parts.vendor_id == vendor_alias.id_vendors).join(obsolescence_alias, Parts.obsolescence_id == obsolescence_alias.id_obs).order_by(Parts.part_number).all()
    formItem.part_number.choices = [(part.id_parts, part.part_number) for part, vendor, obsolescence in parts]

    mu_alias = aliased(Manufactoring_unit)
    loc = db.session.query(Location, mu_alias).join(mu_alias, Location.mu_id == mu_alias.id_mu).order_by(Location.mu_id).all()

    sgroup = System_groups.query.order_by(System_groups.id_s_group).all()
    formItem.sgroup.choices += [(row.id_s_group, row.system_group) for row in sgroup]

    almox = Almox.query.all()

    if request.method == 'POST':
        try:   
            new_rpn = Rpn()
            new_rpn.part_id = request.form.get('parts')
            new_rpn.c_impact_id = formItem.ci_level.data
            new_rpn.spare_av_id = formItem.savailability.data
            new_rpn.spare_c_id = formItem.scondition.data
            new_rpn.vendorsuport_id = formItem.vsupport.data
            new_rpn.loc_id = request.form.get('loc')
            new_rpn.sgroups_id = formItem.sgroup.data
            new_rpn.scomplexity_id = formItem.scomplexity.data
            new_rpn.quantity = formItem.quantity.data
            new_rpn.description = formItem.description.data
            new_rpn.created_by = current_user.get_name()
            new_rpn.modified_by = current_user.get_name()
            new_rpn.last_modified = datetime.date.today()
            new_rpn.pa = formItem.project_number.data
            new_rpn.cost = formItem.cost.data            
            new_rpn.inactive = formItem.inactive.data
            new_rpn.almox_id = request.form.get('almox')

            # Faz a consulta no banco para saber qual o último id
            last_id = Rpn.query.order_by(Rpn.id_rpn.desc()).first()
            new_rpn.id_rpn = last_id.id_rpn + 1

            # Cria um novo objeto rpn e adiciona 
            db.session.add(new_rpn)
            db.session.commit()

            return redirect(url_for('add_rpn'))

        except Exception as e:
            flash(f"Erro ao adicionar o item: {str(e)}")
            return render_template('add_rpn.html')

    return render_template('add_rpn.html', formItem=formItem, loc=loc, almox=almox, parts=parts)
        
@app.route('/add-part-number', methods=['GET', 'POST'])
@login_required
def add_partnumber(): 

    vendor = Vendors.query.order_by().all()
    obsolescence = Obsolescence.query.order_by().all()

    form_pnumber = FormAddPartNumber()
    form_pnumber.vendor.choices = [(row.id_vendors, row.name) for row in vendor]
    form_pnumber.obsolescence.choices = [(row.id_obs, row.status) for row in obsolescence]
    
    nome_seguro = ""
    if request.method == 'POST':
        try: 
            # Cria um novo objeto rpn e adiciona           
            new_part = Parts(created=datetime.date.today(), modified_by=current_user.get_name())
            new_part.part_number = form_pnumber.part_number.data
            new_part.product = form_pnumber.product.data
            new_part.vendor_id = form_pnumber.vendor.data
            new_part.obsolescence_id = form_pnumber.obsolescence.data
            new_part.end_life = form_pnumber.year_discontinued.data
            # Faz a consulta no banco para saber qual o último id
            last_id = Parts.query.order_by(Parts.id_parts.desc()).first()
            new_part.id_parts = last_id.id_parts + 1

            arquivo = form_pnumber.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            new_part.fotos = nome_seguro            

            db.session.add(new_part)
            db.session.commit()
            return redirect(url_for('add_partnumber'))

        except Exception as e:
            flash(f"Erro ao adicionar o part number: {str(e)}")
            return render_template('add_part.html')

    return render_template('add_part.html', form_pnumber=form_pnumber, filename=nome_seguro)

@app.route('/add-vendor', methods=['GET', 'POST'])
@login_required
def add_vendor():
    
    region = Region.query.order_by().all()
    form_addVendor = FormAddVendor()
    form_addVendor.region.choices = [(row.id_region, row.region) for row in region]

    if request.method == 'POST':
        # Cria um novo objeto vendor   
        new_vendor = Vendors()
        new_vendor.name = form_addVendor.name.data
        new_vendor.region_id = form_addVendor.region.data
        new_vendor.support_after_sales = form_addVendor.after_sales_support.data
        new_vendor.active = form_addVendor.active.data
        new_vendor.site = form_addVendor.site.data
        new_vendor.email = form_addVendor.email.data
        new_vendor.phone = form_addVendor.contact_phone.data
        new_vendor.modified_by = current_user.get_name()

        # Faz a consulta no banco para saber qual o último id
        id_vendor = Vendors.query.order_by(Vendors.id_vendors.desc()).first()
        id_vendor = id_vendor.id_vendors + 1
        new_vendor.id_vendors = id_vendor
        
        db.session.add(new_vendor)
        db.session.commit()
        return redirect(url_for('add_vendor'))

    return render_template('add_vendor.html', form_addVendor=form_addVendor)

@app.route('/edit-item/<id_rpn>', methods=['GET', 'POST'])
@login_required
def edit_rpn(id_rpn):

    form_editItem = FormEditRPN()

    vendor_alias = aliased(Vendors)
    obsolescence_alias = aliased(Obsolescence)
    parts = db.session.query(Parts, vendor_alias, obsolescence_alias).join(vendor_alias, Parts.vendor_id == vendor_alias.id_vendors).join(obsolescence_alias, Parts.obsolescence_id == obsolescence_alias.id_obs).order_by(Parts.part_number).all()

    rpn = db.session.query(Rpn).filter_by(id_rpn=id_rpn).first()
    current_part = db.session.query(Parts).filter_by(id_parts=rpn.part_id).first()

    vendors_list = db.session.query(Vendors).filter_by().all()
    obs = db.session.query(Obsolescence).filter_by().all()
    sgroup = db.session.query(System_groups).filter_by().all()

    mu_alias = aliased(Manufactoring_unit)
    loc = db.session.query(Location, mu_alias).join(mu_alias, Location.mu_id == mu_alias.id_mu).filter_by().all()

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

    return render_template('edit_rpn.html', form_editItem=form_editItem, rpn=rpn, parts=parts, current_part=current_part, vendors_list=vendors_list, sgroup=sgroup, obs=obs, loc=loc)

@app.route('/edit-part-number/<partnumber>', methods=['GET', 'POST'])
@login_required
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
