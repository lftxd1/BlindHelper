package com.wms.web;

import com.wms.WebSocketServer;
import com.wms.mapper.IntrusionDAO;
import com.wms.model.Intrusion;
import com.wms.model.ResultUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import javax.servlet.http.HttpServletRequest;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Date;
import java.util.List;
import java.util.Random;

@RestController
@RequestMapping(value = "/intrusion")
public class IntrusionController {
	@Autowired
	IntrusionDAO intrusionDAO;
	@Permissions(value ="")
	@RequestMapping(value = "/photo", method = RequestMethod.POST)
	public Object receivePhoto( HttpServletRequest request)
			throws IOException {
		MultipartFile file= ((MultipartHttpServletRequest) request).getFile("photo");
		String str= request.getParameter("warehouse");

		int len = file.getOriginalFilename().indexOf(".");
		String result = getRandomString1(10)+"."+file.getOriginalFilename().substring(len+1);
		System.out.println(file.getSize());
		Intrusion intrusion=new Intrusion();
		intrusion.setPath(result);
		intrusion.setTime(new Date());
		intrusion.setWarehouse(str);
		intrusionDAO.insert(intrusion);
		String filename= "./target/classes/static/"+result;
		BufferedOutputStream bos = null;
		FileOutputStream fos = new FileOutputStream(new File(filename));
		bos = new BufferedOutputStream(fos);
		bos.write(file.getBytes());
		bos.close();
		fos.close();
		WebSocketServer.sendInfo("photo","10");
		return ResultUtil.success();
	}
	@Permissions(value = "")
	@RequestMapping(value = "/getAllPhotoByWarehouse", method = RequestMethod.GET)
	public Object index(String warehouse){
		List<Intrusion> path =intrusionDAO.selectByByWarehouse(warehouse);
		return ResultUtil.success(path);
	}

	public static String getRandomString1(int length){
		String str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
		Random random = new Random();
		StringBuffer sb=new StringBuffer();
		for(int i=0;i<length;i++){
			int number=random.nextInt(62);
			sb.append(str.charAt(number));
		}
		return sb.toString();
	}
	@Permissions(value ="")
	@RequestMapping(value = "/deleteIntrusionById", method = RequestMethod.GET)
	public Object deleteUser(int id) {
		if(intrusionDAO.deleteByPrimaryKey(id)==0){
			return ResultUtil.fail("id不存在");
		}
		return ResultUtil.success("删除成功");
	}
}
