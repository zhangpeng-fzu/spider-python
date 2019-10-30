package com.peng;

import com.peng.frame.LiveScoreFrame;
import com.peng.service.CalMatchCascadeMiss;
import com.peng.service.CalMatchNumMiss;
import com.peng.service.LoadHistoryData;
import com.peng.service.ParseTodayData;
import com.peng.util.DateUtil;

import javax.swing.*;
import java.io.IOException;
import java.net.URL;
import java.net.URLConnection;
import java.text.ParseException;
import java.util.Date;
import java.util.TimeZone;

public class Main {

    public static void main(String[] args) {
        LiveScoreFrame frame;
        try {
            frame = new LiveScoreFrame();
            try {
                if (getBjTime().after(DateUtil.getDateFormat().parse("2019-10-30"))){
                    JOptionPane.showMessageDialog(frame, "试用时间已到，请联系相关人员", "提示", JOptionPane.WARNING_MESSAGE);
                    frame.dispose();
                    return;
                }
            } catch (IOException e) {
                e.printStackTrace();
                JOptionPane.showMessageDialog(frame, "试用时间已到，请联系相关人员", "提示", JOptionPane.WARNING_MESSAGE);
                frame.dispose();
                return;
            }
            frame.setVisible(true);
            JOptionPane.showMessageDialog(frame, "当前处于试用状态，试用截止时间2019/11/3 00:00:00", "标题", JOptionPane.WARNING_MESSAGE);
            //开启异步线程计算数据
            new Thread(() -> {
                //加载所有场次数据
                System.out.println("正在加载所有场次数据");
                LoadHistoryData.loadHistoryData();
                //加载今天的数据
                try {
                    System.out.println("正在加载当天所有场次数据");
                    ParseTodayData.getMatchData();
                } catch (ParseException e) {
                    e.printStackTrace();
                }
                new Thread(() -> {
                    System.out.println("正在计算赛事场次数据");
                    try {
                        CalMatchNumMiss.calculate();
                    } catch (ParseException e) {
                        e.printStackTrace();
                    }
                }).start();
                try {
                    System.out.println("正在计算串关场次数据");
                    CalMatchCascadeMiss.calculate();
                } catch (ParseException e) {
                    e.printStackTrace();
                }

            }).start();

        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

    private static Date getBjTime() throws IOException {
        TimeZone.setDefault(TimeZone.getTimeZone("GMT+8")); // 时区设置
        URL url = new URL("http://www.baidu.com");//取得资源对象
        URLConnection uc = url.openConnection();//生成连接对象
        uc.connect(); //发出连接
        long ld = uc.getDate(); //取得网站日期时间（时间戳）
        if (ld == 0){
            return new Date();
        }
        return new Date(ld);
    }
}
