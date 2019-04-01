import os
import pymysql
import random
import time
import platform


class BootappSktMaker :
    
    SCRIPT_NAME = 'bootapp_skt_maker.py v1.0'
    ENTITY_DIR = 'model/entity'
    QUERY_DIR = 'model/query'
    CONTROLLER_DIR = 'controller'
    SERVICE_DIR = 'service'
    SERVICE_IMPL_DIR = 'service/impl'
    MAPPER_XML_DIR = 'mapper_xml'
    DAO_DIR = 'dao'
    COMMONS_DATA = {}
    
    
    def __init__(self, out_dir=None, package_name=None, tb_name=None, tb_cols=None, tb_comment=None, copy_right='@copyright '):
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.curr_dir = None
        import sys
        if getattr(sys, 'frozen', False):
                self.curr_dir = os.path.dirname(sys.executable)
        elif __file__ :
                self.curr_dir = os.path.dirname(os.path.realpath(__file__))
        import getpass
        self.os_user = getpass.getuser()
        if out_dir and len(out_dir)>1 :
            self.out_dir = os.path.join(out_dir, 'out')
        else:
            self.out_dir = os.path.join(self.curr_dir, 'out')
            
        if not package_name :
            raise Exception('package_name is required.')
        else:
            self.package_dir = os.path.join(self.out_dir, package_name.replace('.', '/')) 
            self.make_dirs(self.package_dir)
            self.entity_dir = os.path.join(self.package_dir, self.ENTITY_DIR) 
            self.make_dirs(self.entity_dir)
            self.controller_dir = os.path.join(self.package_dir, self.CONTROLLER_DIR)
            self.make_dirs(self.controller_dir)
            self.service_dir = os.path.join(self.package_dir, self.SERVICE_DIR)
            self.make_dirs(self.service_dir)
            self.service_impl_dir = os.path.join(self.package_dir, self.SERVICE_IMPL_DIR)
            self.make_dirs(self.service_impl_dir)
            self.dao_dir = os.path.join(self.package_dir, self.DAO_DIR)
            self.make_dirs(self.dao_dir)
            self.query_dir = os.path.join(self.package_dir, self.QUERY_DIR)
            self.make_dirs(self.query_dir)
            self.mapper_dir = os.path.join(self.package_dir, self.MAPPER_XML_DIR)
            self.make_dirs(self.mapper_dir)
        
        if not tb_name :
            raise Exception('table_name is required.')
        else:
            self.entity_name = self.get_camelcase(tb_name, True)
            self.low_entity_name = self.get_camelcase(tb_name)
            self.tb_name=tb_name
        
        if not tb_cols :
            raise Exception('table_cols data is empty.')
        else:
            self.tb_cols = tb_cols
        
        if not tb_comment :
            raise Exception('table_comment data is empty.')
        
        self.COMMONS_DATA = {
                'entity_name' : self.entity_name,
                'low_entity_name' : self.low_entity_name,
                'controller_name' : self.entity_name+'Controller',
                'query_name'  : self.entity_name+'Query',
                'dao_name' : self.entity_name+'DAO',
                'service_name' : self.entity_name+'Service',
                'service_impl_name' : self.entity_name+'ServiceImpl',
                'create_time' : self.create_time,
                'app_package' : package_name,
                'table_name'  : self.tb_name,
                'os_user'     : self.os_user,
                'copy_right'  : copy_right,
                'comment' : tb_comment,
                'script_name' : self.SCRIPT_NAME
            }
    
    def make_dirs(self, dir):
        if not os.path.exists(dir) :
            os.makedirs(dir)
    
    def read_file(self, in_file):
        with open(file=in_file, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
        return ''.join(lines)

    def get_camelcase(self, str, first_upper=False):
        """
                     将下划线分割词转换为驼峰写发，eg: user_name-> UserName, or userName
        """
        if str  :
            strSegs = str.lower().split('_')
            segs = [ seg.capitalize() for seg in strSegs]
            #如果转换后第一个字符需要小写
            if not first_upper :
                segs[0] = segs[0].lower()
            return ''.join(segs)
        else:
            return ''
    
    def get_field_type(self, cdesc):
        """
                        根据字段类型返回对应的JAVA类型
        """
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
        
        
    def get_field_comment(self, col):
        col_val = "default:"+str(col[2])+" " if col[2] else ''
        char_max_len = "char length:"+str(col[3])+" " if col[3] else ''
        number_len = "length:"+str(col[4]) if col[4] else ''
        number_scale = "scale:"+str(col[5]) if col[5] else ''
        comment = col[6] if col[6] else ''
        field_cmt="\n        ".join([comment, col_val + char_max_len + number_len +" "+ number_scale])
        return field_cmt
    
    def get_serial_uid(self):
        return -int(time.time()*1000000)<<2
    
    def out_entity(self):
        out_file = os.path.join(self.entity_dir, self.entity_name+'.java')
        file_tpl = self.read_file(self.curr_dir+'/bootapp/entity.tpl')
        field_list = []
        method_list = []
        self.primary_type='Long'
        # 处理每行字段信息
        for col in self.tb_cols:
            col_name = col[0]
            col_type = col[1]
            field_desc = {
                'field_annotation' : '@Id' if 'PRI' in col else '@Column' ,
                'field_name' : self.get_camelcase(col_name),
                'field_type' : self.get_field_type(col_type),
                'field_comment' : self.get_field_comment(col)
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
                'method' : self.get_camelcase(col_name, True),
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
        model = {}
        model['field_area']=''.join(field_list)
        model['method_area']=''.join(method_list)
        model['serial_uid']=self.get_serial_uid()
        model.update(self.COMMONS_DATA)
        out_content = file_tpl.format(**model)
        with open(file=out_file, mode='w', encoding="utf-8") as fw :
            fw.write(out_content)
            print('--Entity file out done. {}'.format(out_file))
        pass
    
    def out_query(self):
        out_file = os.path.join(self.query_dir, self.COMMONS_DATA['query_name']+'.java')
        file_tpl = self.read_file(self.curr_dir+'/bootapp/query.tpl')
        #TODO:
        field_list = []
        method_list = []
        # 处理每行字段信息
        for col in self.tb_cols:
            col_name = col[0]
            col_type = col[1]
            field_desc = {
                'field_name' : self.get_camelcase(col_name),
                'field_type' : self.get_field_type(col_type)
            }
            field_list.append(
            """
            private {field_type} {field_name};
            """.format(**field_desc)
            )
            method_desc={
                'method' : self.get_camelcase(col_name, True),
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
        model = {}
        model['field_area']=''.join(field_list)
        model['method_area']=''.join(method_list)
        model.update(self.COMMONS_DATA)
        out_content = file_tpl.format(**model)
        with open(file=out_file, mode='w', encoding="utf-8") as fw :
            fw.write(out_content)
            print('--Query file out done. {}'.format(out_file))
    
    def out_dao(self):
        out_file = os.path.join(self.dao_dir, self.COMMONS_DATA['dao_name']+'.java')
        file_tpl = self.read_file(self.curr_dir+'/bootapp/dao.tpl')
        out_content = file_tpl.format(**self.COMMONS_DATA)
        with open(file=out_file, mode='w', encoding="utf-8") as fw :
            fw.write(out_content)
            print('--DAO file out done. {}'.format(out_file))
            
    def out_mapper(self):
        out_file = os.path.join(self.mapper_dir, self.entity_name+'Mapper.xml')
        file_tpl = self.read_file(self.curr_dir+'/bootapp/mapper.xml.tpl')
        model = {}
        query_cond_list = []
        insert_cols = []
        insert_entity_fields=[]
        # 处理每行字段信息
        for col in self.tb_cols:
            col_name = col[0]
            field_name = self.get_camelcase(col_name);
            if 'PRI' in col :
                model['pri_col']=col_name
                model['pri_field']=field_name
            else:
                insert_cols.append(col_name)
                insert_entity_fields.append('#{{{0}.{1}}}'.format(self.entity_name,field_name))
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
        model.update(self.COMMONS_DATA)
        out_content = file_tpl.format(**model)
        with open(file=out_file, mode='w', encoding="utf-8") as fw :
            fw.write(out_content)
            print('--mapper xml file out done. {}'.format(out_file))
            
    def out_services(self):
        service_out_file = os.path.join(self.service_dir, self.COMMONS_DATA['service_name']+'.java')
        service_file_tpl = self.read_file(self.curr_dir+'/bootapp/service.tpl')
        
        service_impl_out_file = os.path.join(self.service_impl_dir, self.COMMONS_DATA['service_impl_name']+'.java')
        service_impl_file_tpl = self.read_file(self.curr_dir+'/bootapp/service.impl.tpl')
        model={}
        model.update(self.COMMONS_DATA)
        service_out_content = service_file_tpl.format(**model)
        with open(file=service_out_file, mode='w', encoding="utf-8") as fw :
            fw.write(service_out_content)
            print('--Service file out done. {}'.format(service_out_file))
            
        service_impl_out_content = service_impl_file_tpl.format(**model)
        with open(file=service_impl_out_file, mode='w', encoding="utf-8") as fw :
            fw.write(service_impl_out_content)
            print('--Service Impl file out done. {}'.format(service_impl_out_file))
            
    def out_controller(self):
        out_file = os.path.join(self.controller_dir, self.COMMONS_DATA['controller_name']+'.java')
        file_tpl = self.read_file(self.curr_dir+'/bootapp/controller.tpl')
        model={
            'req_mapping' : self.entity_name.lower(),
            'primary_type': self.primary_type
            }
        model.update(self.COMMONS_DATA)
        out_content = file_tpl.format(**model)
        with open(file=out_file, mode='w', encoding="utf-8") as fw :
            fw.write(out_content)
            print('--Controller file out done. {}'.format(out_file))




if __name__ == '__main__' :
    mysql_info = input('请输入MYSQL连接信息(如: 127.0.0.1 3306 root root utf8 db_name):')
    table_name = input('请输入MYSQL表名称:')
    package_name = input('请输入项目包名称(如：com.uuola.app):')
    out_dir = input('请输入输出目录(当前目录请直接回车):')
    copy_right= input('请输入版权信息:')
    
    table_cols = None
    table_comments = None 
    mysql_conn_info = mysql_info.split(' ')
    if mysql_conn_info and len(mysql_conn_info)<6:
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
    
    # 查表备注信息
    sql2 = """
        SELECT TABLE_NAME, TABLE_COMMENT FROM information_schema.TABLES WHERE table_name='{}';
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
    
    maker = BootappSktMaker(out_dir, package_name, table_name, table_cols, table_comment, copy_right)
    maker.out_entity()
    maker.out_dao()
    maker.out_mapper()
    maker.out_services()
    maker.out_query()
    maker.out_controller()
    
    if  'win' in str(platform.system()).lower() :
        os.popen('cmd /c explorer {}'.format(os.path.abspath(maker.package_dir)))
    print('输出包目录为：', maker.package_dir)
    input('请按回车键结束...')