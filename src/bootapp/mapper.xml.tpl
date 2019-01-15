<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//ibatis.apache.org//DTD Mapper 3.0//EN"
        "http://ibatis.apache.org/dtd/ibatis-3-mapper.dtd">
<mapper namespace="{app_package}.dao.{entity_name}DAO">
<!-- {comment} -->

	<sql id="queryCond">
		{query_condition}
	</sql>

	<select id="count" parameterType="{entity_name}Query" resultType="java.lang.Integer">
        select count(*) from {table_name} where id!=0 <include refid="queryCond"/>
    </select>
    
	<select id="range" resultType="{entity_name}" parameterType="{entity_name}Query">
		select * from {table_name} where id <![CDATA[ <= ]]> (
			select id from {table_name} where id!=0 <include refid="queryCond"/> 
			order by id desc limit #{{crow}}, 1
		) <include refid="queryCond"/> order by id desc limit 0, #{{listSize}}
	</select>
	
	<select id="list" resultType="{entity_name}" parameterType="{entity_name}Query">
		select * from {table_name} where id!=0 <include refid="queryCond"/> order by id desc limit 0, 10000
	</select>
	
	<insert id="bulkInsert" parameterType="java.util.List" useGeneratedKeys="true" keyProperty="{pri_field}" keyColumn="{pri_col}">
      insert into {table_name}({insert_cols}) values
      <foreach collection="list" item="{entity_name}" separator=",">
          ({insert_entity_fields})
      </foreach>
    </insert>
	
</mapper>