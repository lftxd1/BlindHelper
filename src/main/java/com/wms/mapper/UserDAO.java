package com.wms.mapper;

import com.wms.model.User;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * UserDAO继承基类
 */
@Repository
public interface UserDAO extends MyBatisBaseDao<User, Integer> {
    User selectByUsername(String username);
    List<User> selectAll();
}