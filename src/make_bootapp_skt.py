import os
import pymysql
import time
import getpass

os_user = getpass.getuser()
table_name = input('请输入表名称:')
app_pack_name = input('请输入项目包名称（如：com.uuola.app:')
out_dir = input('请输入输出目录:')
copy_right= input('请输入版权信息:')

sql = 'desc {}'.format(table_name)
curr_dir = os.path.dirname(os.path.realpath(__file__))
table_cols = None
conn = pymysql.connect(host='127.0.0.1',port=3306, user='root', charset='utf8', password='root', db='ny_site')

try:
        with conn.cursor() as cur :
            cur.execute(sql)
            table_cols = cur.fetchall()
        conn.commit()
except Exception as e:
        conn.rollback()
        print(str(e))
finally:
        conn.close()

out_package_dir = os.path.join(out_dir, app_pack_name.replace('.', '/')) 
if not os.path.exists(out_package_dir) :
    os.makedirs(out_package_dir)

def try_make_dirs(dir):
    if not os.path.exists(dir) :
        os.makedirs(dir)
    pass

def read_file(in_file):
    with open(file=in_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    return ''.join(lines)
    pass   
    
def get_camelcase(str, first_upper=False):
    if str  :
        strSegs = str.lower().split('_')
        segs = [ seg.capitalize() for seg in strSegs]
        #如果转换后第一个字符需要小写
        if not first_upper :
            segs[0] = segs[0].lower()
        return ''.join(segs)
    else:
        return ''
    pass

def get_field_type(desc):
    if 'varchar' in desc or 'char' in desc or 'text' in desc:
        return 'String'
    elif desc.find('int(')==0 or 'tinyint' in desc:
        return 'Integer'
    elif 'bigint' in desc:
        return 'Long'
    elif 'datetime' in desc :
        return 'Date'
    elif 'double' in desc :
        return 'Double'
    elif 'decimal' in desc :
        return 'BigDecimal'
    else:
        return 'void'
    pass

#输出实体类文件
def out_entity_file(package_dir, table_name, table_columns):
    entity_dir = 'model/entity'
    entity_name = get_camelcase(table_name, True)
    try_make_dirs(os.path.join(package_dir, entity_dir))
    out_file = os.path.join(package_dir, entity_dir+'/'+entity_name+'.java')
    file_tpl = read_file(curr_dir+'/bootapp/entity.tpl')
    model = {
        'entity_name' : entity_name,
        'create_time' : time.strftime("%Y-%m-%d %H:%M:%S"),
        'app_package' : app_pack_name,
        'table_name'  : table_name,
        'os_user'     : os_user,
        'copy_right'  : copy_right
    }
    #TODO:
    field_list = []
    method_list = []
    primary_type='Long'
    # 处理每行字段信息
    for col in table_columns:
        col_name = col[0]
        col_type = col[1]
        field_desc = {
            'field_annotation' : '@Id' if 'PRI' in col else '@Column' ,
            'field_name' : get_camelcase(col_name),
            'field_type' : get_field_type(col_type)
        }
        if field_desc['field_annotation']=='@Id':
            primary_type = field_desc['field_type']
        field_list.append(
        """        
        {field_annotation}
        private {field_type} {field_name};
        """.format(**field_desc)
        )
        method_desc={
            'method' : get_camelcase(col_name, True),
            'field_name' : field_desc['field_name'],
            'field_type' : field_desc['field_type']
        }
        method_list.append(
        """
        public {field_type} get{method}() {{
            return {field_name};
        }}
        
        public void set{method}({field_type} {field_name}) {{
            this.{field_name} = {field_name};
        }}
        """.format(**method_desc)
        )
        pass
    
    model['field_area']=''.join(field_list)
    model['method_area']=''.join(method_list)
    out_content = file_tpl.format(**model)
    with open(file=out_file, mode='w', encoding="utf-8") as fw :
        fw.write(out_content)
        print('--Entity file out done. {}'.format(out_file))
    return primary_type
    pass

def out_query_file(package_dir, table_name, table_columns):
    query_dir = 'model/query'
    entity_name = get_camelcase(table_name, True)
    query_name = entity_name+'Query'
    try_make_dirs(os.path.join(package_dir, query_dir))
    out_file = os.path.join(package_dir, query_dir+'/'+query_name+'.java')
    file_tpl = read_file(curr_dir+'/bootapp/query.tpl')
    model = {
        'create_time' : time.strftime("%Y-%m-%d %H:%M:%S"),
        'app_package' : app_pack_name,
        'query_name'  : query_name,
        'os_user'     : os_user,
        'copy_right'  : copy_right
    }
    #TODO:
    field_list = []
    method_list = []
    # 处理每行字段信息
    for col in table_columns:
        col_name = col[0]
        col_type = col[1]
        field_desc = {
            'field_name' : get_camelcase(col_name),
            'field_type' : get_field_type(col_type)
        }
        field_list.append(
        """
        private {field_type} {field_name};
        """.format(**field_desc)
        )
        method_desc={
            'method' : get_camelcase(col_name, True),
            'field_name' : field_desc['field_name'],
            'field_type' : field_desc['field_type']
        }
        method_list.append(
        """
        public {field_type} get{method}() {{
            return {field_name};
        }}
        
        public void set{method}({field_type} {field_name}) {{
            this.{field_name} = {field_name};
        }}
        """.format(**method_desc)
        )
        
        if col_name == 'create_time':
            field_list.append(
        """
        private Date beginCreateTime;
        
        private Date endCreateTime;
        """
        )
            method_list.append(
        """
        public Date getBeginCreateTime() {
            return beginCreateTime;
        }
    
        public void setBeginCreateTime(Date beginCreateTime) {
            this.beginCreateTime = beginCreateTime;
        }
    
        public Date getEndCreateTime() {
            return endCreateTime;
        }
    
        public void setEndCreateTime(Date endCreateTime) {
            this.endCreateTime = endCreateTime;
        }
        """
        )
            pass
        pass
    
    model['field_area']=''.join(field_list)
    model['method_area']=''.join(method_list)
    out_content = file_tpl.format(**model)
    with open(file=out_file, mode='w', encoding="utf-8") as fw :
        fw.write(out_content)
        print('--Query file out done. {}'.format(out_file))
    pass

# 输出DAO类文件
def out_dao_file(package_dir, table_name):
    dao_dir = 'dao'
    entity_name = get_camelcase(table_name, True)
    dao_name = entity_name+'DAO'
    try_make_dirs(os.path.join(package_dir, dao_dir))
    out_file = os.path.join(package_dir, dao_dir+'/'+dao_name+'.java')
    file_tpl = read_file(curr_dir+'/bootapp/dao.tpl')
    model = {
        'dao_name' : dao_name,
        'create_time' : time.strftime("%Y-%m-%d %H:%M:%S"),
        'app_package' : app_pack_name,
        'entity_name' : entity_name,
        'os_user'     : os_user,
        'copy_right'  : copy_right
    }
    out_content = file_tpl.format(**model)
    with open(file=out_file, mode='w', encoding="utf-8") as fw :
        fw.write(out_content)
        print('--DAO file out done. {}'.format(out_file))
    pass

# 输出mapper xml 文件
def out_mapper_xml_file(package_dir, table_name, table_columns):
    mapper_xml_dir = 'mapper_xml'
    entity_name = get_camelcase(table_name, True)
    try_make_dirs(os.path.join(package_dir, mapper_xml_dir))
    out_file = os.path.join(package_dir, mapper_xml_dir+'/'+entity_name+'Mapper.xml')
    file_tpl = read_file(curr_dir+'/bootapp/mapper.xml.tpl')
    model = {
        'entity_name' : entity_name,
        'app_package' : app_pack_name,
        'table_name'  : table_name,
        'os_user'     : os_user,
        'copy_right'  : copy_right
    }
    query_cond_list = []
    insert_cols = []
    insert_entity_fields=[]
    # 处理每行字段信息
    for col in table_columns:
        col_name = col[0]
        field_name = get_camelcase(col_name);
        if 'PRI' in col :
            model['pri_col']=col_name
            model['pri_field']=field_name
        else:
            insert_cols.append(col_name)
            insert_entity_fields.append('#{{{0}.{1}}}'.format(entity_name,field_name))
        field_desc = {
            'field_name' : field_name,
            'col_name' : col_name
        }
        if col_name == 'create_time':
            query_cond_list.append(
            """
            <if test="beginCreateTime!=null and endCreateTime!=null">
                and ( create_time <![CDATA[ >= ]]> #{{beginCreateTime}} and create_time <![CDATA[ < ]]> #{{endCreateTime}} )
            </if>""".format(**field_desc)
            )
        else:
            query_cond_list.append(
            """
            <if test="{field_name}!=null">and {col_name}=#{{{field_name}}}</if>""".format(**field_desc)
            )
        pass
    
    model['query_condition']=''.join(query_cond_list)
    model['insert_cols']=',\n          '.join(insert_cols)
    model['insert_entity_fields']=',\n          '.join(insert_entity_fields)
    out_content = file_tpl.format(**model)
    with open(file=out_file, mode='w', encoding="utf-8") as fw :
        fw.write(out_content)
        print('--mapper xml file out done. {}'.format(out_file))
    pass

# 输出 service 文件
def out_service_file(package_dir, table_name):
    #TODO:
    service_dir = 'service'
    service_impl_dir = 'service/impl'
    
    entity_name = get_camelcase(table_name, True)
    service_name = entity_name+'Service'
    service_impl_name = entity_name+'ServiceImpl'
    
    try_make_dirs(os.path.join(package_dir, service_dir))
    try_make_dirs(os.path.join(package_dir, service_impl_dir))
    
    service_out_file = os.path.join(package_dir, service_dir+'/'+service_name+'.java')
    service_file_tpl = read_file(curr_dir+'/bootapp/service.tpl')
    
    service_impl_out_file = os.path.join(package_dir, service_impl_dir+'/'+service_impl_name+'.java')
    service_impl_file_tpl = read_file(curr_dir+'/bootapp/service.impl.tpl')
    
    model = {
        'service_name' : service_name,
        'service_impl_name' : service_impl_name,
        'create_time' : time.strftime("%Y-%m-%d %H:%M:%S"),
        'app_package' : app_pack_name,
        'entity_name' : entity_name,
        'os_user'     : os_user,
        'copy_right'  : copy_right
    }
    service_out_content = service_file_tpl.format(**model)
    with open(file=service_out_file, mode='w', encoding="utf-8") as fw :
        fw.write(service_out_content)
        print('--Service file out done. {}'.format(service_out_file))
        
    service_impl_out_content = service_impl_file_tpl.format(**model)
    with open(file=service_impl_out_file, mode='w', encoding="utf-8") as fw :
        fw.write(service_impl_out_content)
        print('--Service Impl file out done. {}'.format(service_impl_out_file))
    pass

# 输出 controller 文件
def out_controller_file(package_dir, table_name, primary_type):
    #TODO:
    controller_dir = 'controller'
    entity_name = get_camelcase(table_name, True)
    low_entity_name = get_camelcase(table_name)
    controller_name = entity_name+'Controller'
    try_make_dirs(os.path.join(package_dir, controller_dir))
    out_file = os.path.join(package_dir, controller_dir+'/'+controller_name+'.java')
    file_tpl = read_file(curr_dir+'/bootapp/controller.tpl')
    model = {
        'controller_name' : controller_name,
        'create_time' : time.strftime("%Y-%m-%d %H:%M:%S"),
        'app_package' : app_pack_name,
        'req_mapping' : entity_name.lower(),
        'entity_name' : entity_name,
        'primary_type': primary_type,
        'low_entity_name' : low_entity_name,
        'os_user'     : os_user,
        'copy_right'  : copy_right
    }
    out_content = file_tpl.format(**model)
    with open(file=out_file, mode='w', encoding="utf-8") as fw :
        fw.write(out_content)
        print('--Controller file out done. {}'.format(out_file))
    pass


# execute file out
primary_type = out_entity_file(out_package_dir, table_name, table_cols)
out_query_file(out_package_dir, table_name, table_cols)
out_dao_file(out_package_dir, table_name)
out_mapper_xml_file(out_package_dir, table_name, table_cols)
out_service_file(out_package_dir, table_name)
out_controller_file(out_package_dir, table_name, primary_type)
