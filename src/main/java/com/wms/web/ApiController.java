package com.wms.web;

import com.wms.mapper.ApiDAO;
import com.wms.mapper.TokenDAO;
import com.wms.mapper.UserDAO;
import com.wms.model.Api;
import com.wms.model.ResultUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(value = "/api")
public class ApiController {
	@Autowired
	ApiDAO apiDAO;
	@Autowired
	UserDAO userDAO;
	@Autowired
	TokenDAO tokenDAO;
	@Permissions(value ="")
	@RequestMapping(value = "/getAllApi", method = RequestMethod.GET)
	public Object index(){
		List<Api> api = apiDAO.selectAll();
		return ResultUtil.success(api);
	}
	@Permissions(value = "")
	@RequestMapping(value = "/addApi", method = RequestMethod.GET)
	public Object add(String name,String path){
		Api api = new Api();
		api.setName(name);
		api.setPath(path);
		apiDAO.insert(api);
		return ResultUtil.success(api);
	}
	@Permissions(value = "")
	@RequestMapping(value = "/deleteApiById", method = RequestMethod.GET)
	public Object deleteApi(int id) {
		if(apiDAO.deleteByPrimaryKey(id)==0){
			return ResultUtil.fail("id不存在");
		}
		return ResultUtil.success("删除成功");
	}

}
