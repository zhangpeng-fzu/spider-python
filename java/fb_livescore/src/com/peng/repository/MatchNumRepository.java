package com.peng.repository;

import com.peng.bean.MatchNumBean;
import com.peng.database.MysqlManager;
import com.peng.util.DateUtil;

import java.sql.*;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

public class MatchNumRepository {



    public static void insert(MatchNumBean matchNumBean) {
        try {
            PreparedStatement plsql;
            plsql = MysqlManager.getConn().prepareStatement("insert into match_num (live_date,match_num,zero,one_three,two_four,five_) "
                    + "values(?,?,?,?,?,?)");
            plsql.setDate(1, Date.valueOf(DateUtil.getDateFormat().format(matchNumBean.getLiveDate())));              //设置参数1，创建id为3212的数据
            plsql.setString(2, matchNumBean.getMatchNum());      //设置参数2，name 为王刚
            plsql.setInt(3, matchNumBean.getZero());
            plsql.setInt(4, matchNumBean.getOne_three());
            plsql.setInt(5, matchNumBean.getTwo_four());
            plsql.setInt(6, matchNumBean.getFive_());
            plsql.executeUpdate();
        } catch (Exception se) {
            // 处理 JDBC 错误
            se.printStackTrace();
        }
    }

    public static java.util.Date clearLastThreeDayData() {
        Calendar calendar = Calendar.getInstance();

        try {
            PreparedStatement plsql;
            plsql = MysqlManager.getConn().prepareStatement("select * from match_num order by live_date desc limit 1");

            ResultSet rs = plsql.executeQuery();
            if (rs.next()) {
                Date lastDate = rs.getDate("live_date");
                calendar.setTime(lastDate);
                //需删除签两天的数据，由于当天可能会获取到前天的数据，导致计算不准，需重新计算前2天的遗漏值
                calendar.add(Calendar.DATE, -2);

                plsql = MysqlManager.getConn().prepareStatement("delete from match_num where live_date >= ?");
                plsql.setDate(1, Date.valueOf(DateUtil.getDateFormat().format(calendar.getTime())));
                plsql.execute();
            }else {
                return null;
            }


        } catch (Exception se) {
            se.printStackTrace();
            return null;
        }

        return calendar.getTime();
    }

    public static MatchNumBean findByLiveDateAndNum(java.util.Date lastDate, String matchNum) {
        MatchNumBean matchNumBean = new MatchNumBean();
        try {
            PreparedStatement plsql;
            plsql = MysqlManager.getConn().prepareStatement("select * from match_num where live_date = ? and match_num = ?");
            plsql.setDate(1, Date.valueOf(DateUtil.getDateFormat().format(lastDate)));
            plsql.setString(2, matchNum);
            ResultSet rs = plsql.executeQuery();
            if (rs.next()) {
                matchNumBean.setLiveDate(rs.getDate("live_date"));
                matchNumBean.setMatchNum(rs.getString("match_num"));
                matchNumBean.setZero(rs.getInt("zero"));
                matchNumBean.setOne_three(rs.getInt("one_three"));
                matchNumBean.setTwo_four(rs.getInt("two_four"));
                matchNumBean.setFive_(rs.getInt("five_"));

            }


        } catch (Exception se) {
            se.printStackTrace();
        }
        return matchNumBean;
    }

    public static List<MatchNumBean> getMatchNumData(java.util.Date date) {
        List<MatchNumBean> matchNumBeans = new ArrayList<>();
        try {
            PreparedStatement plsql;
            plsql = MysqlManager.getConn().prepareStatement("select * from match_num where live_date = ?");
            plsql.setDate(1, Date.valueOf(DateUtil.getDateFormat().format(date)));
            ResultSet rs = plsql.executeQuery();
            while (rs.next()) {
                MatchNumBean matchNumBean = new MatchNumBean();
                matchNumBean.setLiveDate(rs.getDate("live_date"));
                matchNumBean.setMatchNum(rs.getString("match_num"));
                matchNumBean.setZero(rs.getInt("zero"));
                matchNumBean.setOne_three(rs.getInt("one_three"));
                matchNumBean.setTwo_four(rs.getInt("two_four"));
                matchNumBean.setFive_(rs.getInt("five_"));
                matchNumBeans.add(matchNumBean);
            }


        } catch (Exception se) {
            se.printStackTrace();
        }
        return matchNumBeans;
    }
}
