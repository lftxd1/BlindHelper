package com.wms.web;

import com.wms.mapper.DepartmentDAO;
import com.wms.mapper.TokenDAO;
import com.wms.mapper.UserDAO;
import com.wms.model.Department;
import com.wms.model.ResultUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(value = "/department")
public class DeparmentController {
	@Autowired
	DepartmentDAO departmentDAO;

	@Autowired
	UserDAO userDAO;
	@Autowired
	TokenDAO tokenDAO;
	@Permissions(value ="")
	@RequestMapping(value = "/getAllDepartment", method = RequestMethod.GET)
	public Object index(){
		List<Department> department = departmentDAO.selectAll();
		return ResultUtil.success(department);
	}
	@Permissions(value = "")
	@RequestMapping(value = "/addDepartment", method = RequestMethod.GET)
	public Object add(String name){
		Department department = new Department();
		department.setName(name);
		departmentDAO.insert(department);
		return ResultUtil.success(department);
	}
	@Permissions(value = "")
	@RequestMapping(value = "/deleteDepartmentById", method = RequestMethod.GET)
	public Object delete(int id) {
		if(departmentDAO.deleteByPrimaryKey(id)==0){
			return ResultUtil.fail("id不存在");
		}
		return ResultUtil.success("删除成功");
	}
}
