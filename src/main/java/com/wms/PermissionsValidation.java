package com.wms;

import com.wms.mapper.ApiDAO;
import com.wms.mapper.TokenDAO;
import com.wms.mapper.UserDAO;
import com.wms.mapper.UserGroupDAO;
import com.wms.model.ResultUtil;
import com.wms.model.Token;
import com.wms.model.User;
import com.wms.model.UserGroup;
import com.wms.web.Permissions;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Aspect
@Component
public class PermissionsValidation {
    //切入点
    @Pointcut("@annotation(com.wms.web.Permissions)")
    //@Pointcut("execution(public * com.wms.web.*.*(..))")
    public void permissionsPoint() {
    }
    @Autowired
    UserDAO userDAO;
    @Autowired
    TokenDAO tokenDAO;
    @Autowired
    ApiDAO apiDAO;
    @Autowired
    UserGroupDAO userGroupDAO;
    //通过方法名获取切入点
    @Around("permissionsPoint()")
    public Object hasPermissions(ProceedingJoinPoint joinPoint) throws Throwable {
//        //方法签名
//        MethodSignature methodSignature=(MethodSignature) joinPoint.getSignature();
//        //获取方法
//        Method aimMethod= methodSignature.getMethod();
//        //获取 @Permissions 的值
//        String permissions=aimMethod.getAnnotation(Permissions.class).value();

        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest request = attributes.getRequest();
        //System.out.println(request.getRequestURL());
        List<String> paths = Arrays.asList(request.getRequestURL().toString().split("/"));
        List<String> whiteList=new ArrayList<>();
        whiteList.add("login");
        whiteList.add("test");
        whiteList.add("photo");
        whiteList.add("video");
        String path=paths.get(paths.size()-1);
        //System.out.println(path);
        if(whiteList.contains(path)){
            return joinPoint.proceed();
        }
        String token=request.getParameter("token");
        if(token==null || token.equals("")){
            return ResultUtil.fail("token为空");
        }
        Token tokenObj=tokenDAO.selectByTokenvalue(token);
        if(tokenObj==null) return ResultUtil.fail("token已过期");
        User user=userDAO.selectByPrimaryKey(tokenObj.getUserId());
//        System.out.println(user.getUserGroup());
        UserGroup userGroup=userGroupDAO.selectByGroupName(user.getUserGroup());
        List<String> apis= Arrays.asList(userGroup.getRights().split(","));
        List<String> permissionsList=new ArrayList<>();

        for(int i=0;i<apis.size();i++){
            permissionsList.add(apiDAO.selectByPrimaryKey(Integer.valueOf(apis.get(i))).getPath());
        }
        if(permissionsList.contains(path)){
            return joinPoint.proceed();
        }
        return ResultUtil.fail("权限不足");
    }



    private boolean validate() {

        return false;
    }
}