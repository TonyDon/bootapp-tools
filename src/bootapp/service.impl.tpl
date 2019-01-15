/*
 * @(#){service_impl_name}.java {create_time}
 * 
 * Copy Right@ {copy_right}
 */ 
package {app_package}.service.impl;

import org.springframework.stereotype.Service;

import {app_package}.model.entity.{entity_name};
import {app_package}.service.{service_name};
import {app_package}.support.db.CrudOperator;
import {app_package}.support.db.PrimaryTx;


/**
 * <pre>
 * {comment}
 * @author {os_user}
 * by make_bootapp_skt.py script generated
 * at {create_time}
 * </pre>
 */
@Service
@PrimaryTx
public class {service_impl_name} extends CrudOperator<{entity_name}> implements {service_name} {{

}}
