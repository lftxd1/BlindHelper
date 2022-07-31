package com.wms.mapper;

import com.wms.model.Token;
import org.springframework.stereotype.Repository;

/**
 * TokenDAO继承基类
 */
@Repository
public interface TokenDAO extends MyBatisBaseDao<Token, Integer> {
    Token selectByTokenvalue(String value);
}