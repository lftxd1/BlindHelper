package com.wms.mapper;

import com.wms.model.Intrusion;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * IntrusionDAO继承基类
 */
@Repository
public interface IntrusionDAO extends MyBatisBaseDao<Intrusion, Integer> {
    List<Intrusion> selectByByWarehouse(String warehouse);
}