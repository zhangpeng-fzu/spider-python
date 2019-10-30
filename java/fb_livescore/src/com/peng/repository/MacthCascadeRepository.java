package com.peng.repository;

import com.peng.bean.MatchCascadeBean;
import com.peng.database.MysqlManager;
import com.peng.util.DateUtil;

import java.sql.*;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

public class MacthCascadeRepository {

    public static void insert(MatchCascadeBean matchCascadeBean) {
        try {
            PreparedStatement plsql;
            plsql = MysqlManager.getConn().prepareStatement("insert into match_cascade (live_date,match_cascade_num,ss,sp,sf,ps,pp,pf,fs,fp,ff) "
                    + "values(?,?,?,?,?,?,?,?,?,?,?)");
            plsql.setDate(1, Date.valueOf(DateUtil.getDateFormat().format(matchCascadeBean.getLiveDate())));              //设置参数1，创建id为3212的数据
            plsql.setString(2, matchCascadeBean.getMatchCascadeNum());      //设置参数2，name 为王刚
            plsql.setInt(3, matchCascadeBean.getSs());
            plsql.setInt(4, matchCascadeBean.getSp());
            plsql.setInt(5, matchCascadeBean.getSf());
            plsql.setInt(6, matchCascadeBean.getPs());
            plsql.setInt(7, matchCascadeBean.getPp());
            plsql.setInt(8, matchCascadeBean.getPf());
            plsql.setInt(9, matchCascadeBean.getFs());
            plsql.setInt(10, matchCascadeBean.getFp());
            plsql.setInt(11, matchCascadeBean.getFf());

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
            plsql = MysqlManager.getConn().prepareStatement("select * from match_cascade order by live_date desc limit 1");

            ResultSet rs = plsql.executeQuery();
            if (rs.next()) {
                Date lastDate = rs.getDate("live_date");
                calendar.setTime(lastDate);
                //需删除签两天的数据，由于当天可能会获取到前天的数据，导致计算不准，需重新计算前2天的遗漏值
                calendar.add(Calendar.DATE, -2);

                plsql = MysqlManager.getConn().prepareStatement("delete from match_cascade where live_date >= ?");
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

    public static MatchCascadeBean findByLiveDateAndCascadeNum(java.util.Date lastDate, String matchCascadeNum) {
        MatchCascadeBean matchCascadeBean = new MatchCascadeBean();
        try {
            PreparedStatement plsql;
            plsql = MysqlManager.getConn().prepareStatement("select * from match_cascade where live_date = ? and match_cascade_num = ?");
            plsql.setDate(1, Date.valueOf(DateUtil.getDateFormat().format(lastDate)));
            plsql.setString(2, matchCascadeNum);
            ResultSet rs = plsql.executeQuery();
            if (rs.next()) {
                matchCascadeBean.setLiveDate(rs.getDate("live_date"));
                matchCascadeBean.setMatchCascadeNum(rs.getString("match_cascade_num"));
                matchCascadeBean.setSs(rs.getInt("ss"));
                matchCascadeBean.setSp(rs.getInt("sp"));
                matchCascadeBean.setSf(rs.getInt("sf"));
                matchCascadeBean.setPs(rs.getInt("ps"));
                matchCascadeBean.setPp(rs.getInt("pp"));
                matchCascadeBean.setPf(rs.getInt("pf"));
                matchCascadeBean.setFs(rs.getInt("fs"));
                matchCascadeBean.setFp(rs.getInt("fp"));
                matchCascadeBean.setFf(rs.getInt("ff"));
            }


        } catch (Exception se) {
            se.printStackTrace();
        }
        return matchCascadeBean;
    }


    public static List<MatchCascadeBean> getMatchCascadeData(java.util.Date date) {
        List<MatchCascadeBean> matchCascadeBeans = new ArrayList<>();
        try {
            PreparedStatement plsql;
            plsql = MysqlManager.getConn().prepareStatement("select * from match_cascade where live_date = ? ");
            plsql.setDate(1, Date.valueOf(DateUtil.getDateFormat().format(date)));
            ResultSet rs = plsql.executeQuery();
            while (rs.next()) {
                MatchCascadeBean matchCascadeBean = new MatchCascadeBean();
                matchCascadeBean.setLiveDate(rs.getDate("live_date"));
                matchCascadeBean.setMatchCascadeNum(rs.getString("match_cascade_num"));
                matchCascadeBean.setSs(rs.getInt("ss"));
                matchCascadeBean.setSp(rs.getInt("sp"));
                matchCascadeBean.setSf(rs.getInt("sf"));
                matchCascadeBean.setPs(rs.getInt("ps"));
                matchCascadeBean.setPp(rs.getInt("pp"));
                matchCascadeBean.setPf(rs.getInt("pf"));
                matchCascadeBean.setFs(rs.getInt("fs"));
                matchCascadeBean.setFp(rs.getInt("fp"));
                matchCascadeBean.setFf(rs.getInt("ff"));
                matchCascadeBeans.add(matchCascadeBean);
            }


        } catch (Exception se) {
            se.printStackTrace();
        }
        return matchCascadeBeans;
    }
}
