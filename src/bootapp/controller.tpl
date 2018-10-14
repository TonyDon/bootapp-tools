/*
 * @(#){controller_name}.java {create_time}
 * 
 * Copy Right@ {copy_right}
 */ 

package {app_package}.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import {app_package}.support.view.BaseController;

/**
 * <pre>
 *
 * @author {os_user}
 * by make_bootapp_skt.py script generated
 * at {create_time}
 * </pre>
 */
@RestController
@RequestMapping("/{req_mapping}")
public class {controller_name} extends BaseController{{

    @Autowired
    private {entity_name}Service {low_entity_name}Service;
    
    @GetMapping("")
    public ModelAndView index() {{
        return makeModelView();
    }}

    @GetMapping("/{{id}}")
    public ResponseEntity<?> show(@PathVariable("id") {primary_type} id) {{
        {entity_name}  entity = {low_entity_name}Service.get(id);
        return ResponseEntity.ok(entity);
    }}
    
    @PostMapping("")
    public ResponseEntity<?> create({entity_name} entity){{
        entity.setCreateTime(DateUtil.getNowTime());
        entity.setUpdateTime(entity.getCreateTime());
        {low_entity_name}Service.insert(entity);
        return ResponseEntity.ok(entity);
    }}
    
    @PutMapping("")
    public ResponseEntity<?> update({entity_name} entity){{
        entity.setUpdateTime(DateUtil.getNowTime());
        int n = {low_entity_name}Service.update(entity);
        return ResponseEntity.ok(n);
    }}
    
    @DeleteMapping(value="", params="ids[]")
    public ResponseEntity<?> bulkDelete(@RequestParam("ids[]") List<{primary_type}> ids) {{
        Integer n = {low_entity_name}Service.bulkDelete(ids);
        return ResponseEntity.ok(n);
    }}
    
    @GetMapping("/search")
    public ResponseEntity<?> search({entity_name}Query query){{
        return ResponseEntity.ok({low_entity_name}Service.rangePage(query));
    }}

}}
