package com.wms.web;

import com.wms.mapper.UserDAO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "/token")
public class TokenController {
	@Autowired
	UserDAO userDAO;
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public Object index(){
		return "";
	}




}
