package com.wms.mapper;

import com.wms.model.Warehouse;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * WarehouseDAO继承基类
 */
@Repository
public interface WarehouseDAO extends MyBatisBaseDao<Warehouse, Integer> {
    List<Warehouse> selectAll();
    Warehouse selectByName(String name);

}