package com.wms.mapper;

import com.wms.model.Department;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * DepartmentDAO继承基类
 */
@Repository
public interface DepartmentDAO extends MyBatisBaseDao<Department, Integer> {
    List<Department> selectAll();

}