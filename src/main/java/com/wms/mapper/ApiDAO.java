package com.wms.mapper;

import com.wms.model.Api;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * ApiDAO继承基类
 */
@Repository
public interface ApiDAO extends MyBatisBaseDao<Api, Integer> {
    List<Api> selectAll();
}