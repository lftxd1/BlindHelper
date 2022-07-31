package com.wms.web;

import com.wms.UdpSimpleClient;
import com.wms.WebSocketServer;
import com.wms.mapper.UserDAO;
import com.wms.model.Intrusion;
import com.wms.model.ResultUtil;
import com.wms.model.User;
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

@RestController
public class IndexController {
	@Autowired
	UserDAO userDAO;
	@Autowired
	UdpSimpleClient udpSimpleClient;
	@RequestMapping(value = "/test", method = RequestMethod.GET)
	public Object index(Integer id){
		udpSimpleClient.sendMessage("open");
//		WebSocketServer.sendInfo("date","10");
		return "user1";
	}
	@RequestMapping(value = "/sendUdp", method = RequestMethod.GET)
	public Object index(String order){
		udpSimpleClient.sendMessage(order);
		return order+"已发送";
	}
	@RequestMapping(value = "/video", method = RequestMethod.POST)
	public void receivePhoto( HttpServletRequest request)
			throws IOException {
		MultipartFile file= ((MultipartHttpServletRequest) request).getFile("photo");
		String filename= "./target/classes/static/video.jpg";
		BufferedOutputStream bos = null;
		FileOutputStream fos = new FileOutputStream(new File(filename));
		bos = new BufferedOutputStream(fos);
		bos.write(file.getBytes());
		bos.close();
		fos.close();
		WebSocketServer.sendInfo("livevideo","10");
	}


}
