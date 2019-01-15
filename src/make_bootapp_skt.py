import os, sys
import pymysql
import time
import getpass

os_user = getpass.getuser()
mysql_info = input('请输入MYSQL连接信息(如: 127.0.0.1 3306 root root utf8 db_name):')
table_name = input('请输入MYSQL表名称:')
app_pack_name = input('请输入项目包名称(如：com.uuola.app):')
out_dir = input('请输入输出目录:')
copy_right= input('请输入版权信息:')

curr_dir = None
if getattr(sys, 'frozen', False):
        curr_dir = os.path.dirname(sys.executable)
elif __file__ :
        curr_dir = os.path.dirname(os.path.realpath(__file__))

table_cols = None
table_comments = None 
mysql_conn_info = mysql_info.split(' ')
if mysql_conn_info and len(mysql_conn_info)==0:
    raise Exception('mysql连接信息错误.')
    
conn = pymysql.connect(host=mysql_conn_info[0],
                       port=int(mysql_conn_info[1]), 
                       user=mysql_conn_info[2], 
                       password=mysql_conn_info[3], 
                       charset=mysql_conn_info[4], 
                       db=mysql_conn_info[5])
# 查询表字段信息
sql = """
        SELECT
          column_name AS col_name,
          column_type AS type ,
          column_default AS col_val,
          character_maximum_length as char_max_len,
          numeric_precision as number_len,
          numeric_scale as number_scale,
          column_comment as comment,
          column_key as pri
        FROM information_schema.columns
        WHERE table_name = '{}'
        ORDER BY ORDINAL_POSITION asc
    """.format(table_name)


sql2 = """
        SELECT TABLE_NAME,TABLE_COMMENT FROM information_schema.TABLES WHERE table_name='{}';
    """.format(table_name)
    
try:
        with conn.cursor() as cur :
            cur.execute(sql)
            table_cols = cur.fetchall()
        with conn.cursor() as cur :
            cur.execute(sql2)
            table_comments = cur.fetchall()
        conn.commit()
except Exception as e:
        conn.rollback()
        print(str(e))
finally:
        conn.close()

if not table_comments :
    raise Exception('table comment not exist!')

table_comment = str(table_comments[0][1]).replace('表', '')

#构建包输出目录
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

def get_field_type(cdesc):
    desc = str(cdesc).lower()
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

def get_field_comment(col):
    col_val = "default:"+str(col[2])+" " if col[2] else ''
    char_max_len = "char length:"+str(col[3])+" " if col[3] else ''
    number_len = "length:"+str(col[4]) if col[4] else ''
    number_scale = "scale:"+str(col[5]) if col[5] else ''
    comment = col[6] if col[6] else ''
    field_cmt="\n        ".join([comment, col_val + char_max_len + number_len +" "+ number_scale])
    return field_cmt

#输出实体类文件
def out_entity_file(package_dir, table_name, table_columns, table_comment):
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
        'copy_right'  : copy_right,
        'comment' : table_comment+' 实体类'
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
            'field_type' : get_field_type(col_type),
            'field_comment' : get_field_comment(col)
        }
        if field_desc['field_annotation']=='@Id':
            primary_type = field_desc['field_type']
        field_list.append(
        """
        /**
        {field_comment}
        */   
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

def out_query_file(package_dir, table_name, table_columns, table_comment):
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
        'copy_right'  : copy_right,
        'comment' : table_comment + ' 条件查询对象'
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
def out_dao_file(package_dir, table_name, table_comment):
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
        'copy_right'  : copy_right,
        'comment' : table_comment + ' 数据操作对象'
    }
    out_content = file_tpl.format(**model)
    with open(file=out_file, mode='w', encoding="utf-8") as fw :
        fw.write(out_content)
        print('--DAO file out done. {}'.format(out_file))
    pass

# 输出mapper xml 文件
def out_mapper_xml_file(package_dir, table_name, table_columns, table_comment):
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
        'copy_right'  : copy_right,
        'comment' : table_comment
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
def out_service_file(package_dir, table_name, table_comment):
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
        'copy_right'  : copy_right,
        'comment' : table_comment +' 业务操作类'
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
def out_controller_file(package_dir, table_name, primary_type, table_comment):
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
        'copy_right'  : copy_right,
        'comment' : table_comment + ' 控制层'
    }
    out_content = file_tpl.format(**model)
    with open(file=out_file, mode='w', encoding="utf-8") as fw :
        fw.write(out_content)
        print('--Controller file out done. {}'.format(out_file))
    pass


# execute file out
primary_type = out_entity_file(out_package_dir, table_name, table_cols, table_comment)
out_query_file(out_package_dir, table_name, table_cols, table_comment)
out_dao_file(out_package_dir, table_name, table_comment)
out_mapper_xml_file(out_package_dir, table_name, table_cols, table_comment)
out_service_file(out_package_dir, table_name, table_comment)
out_controller_file(out_package_dir, table_name, primary_type, table_comment)
