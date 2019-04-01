/*
 * @(#){entity_name}.java {create_time}
 * 
 * Copy Right@ {copy_right}
 */ 

package {app_package}.model.entity;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

/**
* <pre>
* {comment}
* @author {os_user}
* by {script_name} generated
* at {create_time} , table_name:{table_name}
* </pre>
*/
@Table(name = "{table_name}")
@Entity
public class {entity_name} implements Serializable{{

	private static final long serialVersionUID = {serial_uid}L;

{field_area}

{method_area}
    
}}
