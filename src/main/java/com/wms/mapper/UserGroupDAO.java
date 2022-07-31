package com.wms.mapper;

import com.wms.model.UserGroup;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * UserGroupDAO继承基类
 */
@Repository
public interface UserGroupDAO extends MyBatisBaseDao<UserGroup, Integer> {
    List<UserGroup> selectAll();
    UserGroup selectByGroupName(String name);

}