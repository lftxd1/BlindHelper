package com.wms.web;

import com.wms.mapper.TokenDAO;
import com.wms.mapper.UserDAO;
import com.wms.model.ResultUtil;
import com.wms.model.Token;
import com.wms.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collection;
import java.util.Date;
import java.util.List;

@RestController
@RequestMapping(value = "/user")
//@CrossOrigin(originPatterns = "*",allowCredentials = "true")
public class UserController {
	@Autowired
	UserDAO userDAO;
	@Autowired
	TokenDAO tokenDAO;
	@Permissions(value ="")
	@RequestMapping(value = "/login", method = RequestMethod.GET)
	public Object index(String username,String password){
		User user= userDAO.selectByUsername(username);
		if(user==null) return ResultUtil.fail("账户不存在");
		else {
			//System.out.println(user.getPassword());
			if(!password.equals(user.getPassword())) return ResultUtil.fail("密码错误");
			else{
				if(tokenDAO.selectByPrimaryKey(user.getId())!=null){
					tokenDAO.deleteByPrimaryKey(user.getId());
				}
				Token token = new Token();
				token.setUserId(user.getId());
				token.setTime(new Date());
				token.setValue(String.valueOf(token.hashCode()));
				tokenDAO.insert(token);
				return ResultUtil.success("登录成功",token);
			}
		}

	}
	@Permissions(value ="")
	@RequestMapping(value = "/register", method = RequestMethod.GET)
	public Object register(String username,String password,String email,String group){

		User user1= userDAO.selectByUsername(username);
		if(user1!=null) return ResultUtil.fail("用户已存在");

			User user =new User();
			user.setUsername(username);
			user.setPassword(password);
			user.setEmail(email);
			user.setUserGroup(group);
			userDAO.insert(user);
			return ResultUtil.success();
	}

	@Permissions(value ="")
	@RequestMapping(value = "/updateGroup", method = RequestMethod.GET)
	public Object update(String token,String group) {
		if(tokenDAO.selectByTokenvalue(token)==null) return ResultUtil.fail();
		int id = tokenDAO.selectByTokenvalue(token).getUserId();
		User user = userDAO.selectByPrimaryKey(id);
		user.setUserGroup(group);
		userDAO.updateByPrimaryKey(user);
		return ResultUtil.success();
	}
	@Permissions(value ="")
	@RequestMapping(value = "/getAllUser", method = RequestMethod.GET)
	public Object getAllUser() {
		List<User> users=userDAO.selectAll();
		return ResultUtil.success(users);
	}
	@Permissions(value ="")
	@RequestMapping(value = "/deleteUserById", method = RequestMethod.GET)
	public Object deleteUser(int id) {
		if(userDAO.deleteByPrimaryKey(id)==0){
			return ResultUtil.fail("id不存在");
		}
		return ResultUtil.success("删除成功");
	}

}
