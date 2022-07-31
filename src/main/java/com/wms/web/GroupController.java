package com.wms.web;

import com.wms.mapper.TokenDAO;
import com.wms.mapper.UserDAO;
import com.wms.mapper.UserGroupDAO;
import com.wms.model.ResultUtil;
import com.wms.model.UserGroup;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController

@RequestMapping(value = "/group")

public class GroupController {
	@Autowired
	UserGroupDAO userGroupDAO;
	@Autowired
	UserDAO userDAO;
	@Autowired
	TokenDAO tokenDAO;
	@Permissions(value = "")
	@RequestMapping(value = "/getAllGroup", method = RequestMethod.GET)
	public Object index(){
		List<UserGroup> group = userGroupDAO.selectAll();
		return ResultUtil.success(group);
	}

	@Permissions(value = "")
	@RequestMapping(value = "/addGroup", method = RequestMethod.GET)
	public Object add(String name,String rights){
		UserGroup userGroup = new UserGroup();
		userGroup.setName(name);
		userGroup.setRights(rights);
		userGroupDAO.insert(userGroup);
		return ResultUtil.success(userGroup);
	}
	@Permissions(value = "")
	@RequestMapping(value = "/deleteGroupById", method = RequestMethod.GET)
	public Object delete(int id) {
		if(userGroupDAO.deleteByPrimaryKey(id)==0){
			return ResultUtil.fail("id不存在");
		}
		return ResultUtil.success("删除成功");
	}


}
