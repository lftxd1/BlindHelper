package com.wms;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetSocketAddress;

/**
 * 默认发送方式
 *
 * @author wliduo[i@dolyw.com]
 * @date 2020/5/20 15:53
 */
@Service
public class UdpSimpleClient {

    private final static Logger logger = LoggerFactory.getLogger(UdpSimpleClient.class);


    private Integer udpPort=1777;

    public void sendMessage(String message) {
        logger.info("发送UDP: {}", message);
        InetSocketAddress inetSocketAddress = new InetSocketAddress("192.168.123.209", udpPort);
        byte[] udpMessage = message.getBytes();
        DatagramPacket datagramPacket = null;
        try (DatagramSocket datagramSocket = new DatagramSocket()) {
            datagramPacket = new DatagramPacket(udpMessage, udpMessage.length, inetSocketAddress);
            datagramSocket.send(datagramPacket);
        } catch (IOException e) {
            logger.error(e.getMessage(), e);
        }
        logger.info("发送成功");
    }
}