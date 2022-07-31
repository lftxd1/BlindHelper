package com.wms.web;

import com.wms.WebSocketServer;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/websocket")
public class TestController {
    @PostMapping("/pushToWeb")
    public void index(){
        WebSocketServer.sendInfo("你好啊","10");
    }

}

