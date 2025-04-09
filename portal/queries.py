# Query para SELECIONAR as informações já pré-definidas de um partnumber
def query_select_to_add():
    return """
	SELECT p.id_parts, p.part_number, obs.status as "Obsolescence", obs.level as "Obsolescence_level", v.name as "Vendor"
    FROM parts p
    INNER JOIN obsolescence obs on p.obsolescence_id = obs.id_obs
    INNER JOIN vendors v on p.vendor_id = v.id_vendors
	ORDER BY p.part_number
    """

# Query para SELECIONAR informações que deseja-se inserir 
# próximo passo é usar a query de 'query_insert_input'
def query_select_input(ci_value, sa_value, sc_value, plant):
    return f"""
    select ci.id_c_impact as "Costumer Impact", sc.id_spare_cond as "Spare Condition", 
    sa.id_spare_av as "Spare Availibility", l.id_location as "Plant"
    from rpn
    inner join costumer_impact ci on rpn.c_impact_id = ci.id_c_impact and ci.title = '{ci_value}'
    inner join spare_availability sa on rpn.spare_av_id = sa.id_spare_av and sa.title = '{sa_value}'
    inner join spare_condition sc on rpn.spare_c_id = sc.id_spare_cond and sc.title = '{sc_value}'
    inner join location l on rpn.loc_id = l.id_location and l.plant = '{plant}';
    """

# Query para INSERIR um novo RPN
def query_insert_input(rows):
    return f"""
    INSERT INTO rpn(
    id_rpn, vendorsuport_id, loc_id, obs_id, sgroup_id, part_id, spare_av_id, spare_c_id, scomplexity_id, 
    c_impact_id, description, data_modificacao, modified_by, created_by)
    VALUES (8034, null, '{rows[3]}', null, null, null, '{rows[1]}', '{rows[2]}', null, '{rows[0]}', null, null, null, null);
    """

# Query para RETORNAR as informações do item que deseja editar 
# quando o usuário clica no botão do dashboard
def query_select_item_to_edit(id):
    return f"""
    SELECT p.part_number, l.description_category, l.groups, v.name, obs.status,
    sg.system_group, syc.description, sa.status, ci.impact, sc.status, vs.status, rpn.quantity, rpn.description
    FROM rpn
    INNER JOIN location l ON rpn.id_rpn = {id} and rpn.loc_id = l.id_location
    INNER JOIN parts p ON rpn.part_id = p.id_parts
    INNER JOIN obsolescence obs ON p.obsolescence_id = obs.id_obs
    INNER JOIN vendors v ON p.vendor_id = v.id_vendors
    INNER JOIN spare_availability sa ON rpn.spare_av_id = sa.id_spare_av
    INNER JOIN spare_condition sc ON rpn.spare_c_id = sc.id_spare_cond
    INNER JOIN system_groups sg ON rpn.sgroups_id = sg.id_s_group 
    INNER JOIN system_complexity syc ON rpn.scomplexity_id = syc.id_scomplexity
    INNER JOIN customer_impact ci ON rpn.c_impact_id = ci.id_c_impact
    INNER JOIN vendor_suport vs ON rpn.vendorsuport_id = vs.id_v_suport
    """

# Query para SELECIONAR as informações (part number) ao editar um item 
def query_select_to_edit_pnumber():
    return """
    SELECT DISTINCT p.part_number, obs.title as "Obsolescence", v.titulo as "Vendor"
    FROM parts p
    INNER JOIN rpn on p.id_parts = rpn.part_id 
    INNER JOIN obsolescence obs on p.obsolescence_id = obs.id_obs
    INNER JOIN vendors v on p.vendor_id = v.id_vendors
    where p.part_number IS NOT null
    """

def query_to_update_item_rpn(list_rpn):
    return f"""
    UPDATE rpn
    SET
    vendorsuport_id = '{list_rpn[1]}', 
    loc_id = '{list_rpn[2]}', obs_id = '{list_rpn[3]}', 
    sgroup_id = '{list_rpn[4]}', part_id = '{list_rpn[5]}', 
    spare_av_id = '{list_rpn[6]}', spare_c_id = '{list_rpn[7]}', 
    scomplexity_id = '{list_rpn[8]}', c_impact_id = '{list_rpn[9]}', 
    description = '{list_rpn[10]}', data_modificacao = '{list_rpn[11]}', 
    modified_by = '{list_rpn[12]}', created_by = '{list_rpn[13]}'
    WHERE rpn.id_rpn = '{list_rpn[0]}';
    """
