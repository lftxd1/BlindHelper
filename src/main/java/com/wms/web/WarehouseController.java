package com.wms.web;

import com.wms.mapper.TokenDAO;
import com.wms.mapper.UserDAO;
import com.wms.mapper.WarehouseDAO;
import com.wms.model.ResultUtil;
import com.wms.model.Warehouse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(value = "/warehouse")
public class WarehouseController {
	@Autowired
	WarehouseDAO warehouseDAO;
	@Autowired
	UserDAO userDAO;
	@Autowired
	TokenDAO tokenDAO;
	@Permissions(value ="")
	@RequestMapping(value = "/getAllWareHouse", method = RequestMethod.GET)
	public Object index(){
		List<Warehouse> warehouse = warehouseDAO.selectAll();
		return ResultUtil.success(warehouse);
	}
	@Permissions(value = "")
	@RequestMapping(value = "/addWarehouse", method = RequestMethod.GET)
	public Object add(String name,String departmentId){
		if(warehouseDAO.selectByName(name)!=null) return ResultUtil.fail("仓库已存在");
		Warehouse warehouse = new Warehouse();
		warehouse.setName(name);
		warehouse.setDepartment(departmentId);
		warehouseDAO.insert(warehouse);
		return ResultUtil.success(warehouse);
	}
	@Permissions(value = "")
	@RequestMapping(value = "/deleteWarehouseById", method = RequestMethod.GET)
	public Object delete(int id) {
		if(warehouseDAO.deleteByPrimaryKey(id)==0){
			return ResultUtil.fail("id不存在");
		}
		return ResultUtil.success("删除成功");
	}
}
