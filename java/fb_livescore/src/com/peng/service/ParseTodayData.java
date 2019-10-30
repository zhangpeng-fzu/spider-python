package com.peng.service;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.peng.bean.MatchBean;
import com.peng.repository.LiveDataRepository;
import com.peng.util.DateUtil;
import com.peng.util.HttpClientUtil;

import java.nio.charset.StandardCharsets;
import java.text.ParseException;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class ParseTodayData {
    static String queryToday() {

        return HttpClientUtil
                .doGet("https://i.sporttery.cn/api/match_live_2/get_match_list?callback=?&_=" + System.currentTimeMillis(), StandardCharsets.UTF_8.displayName());

    }

    public static void getMatchData() throws ParseException {
        List<String> weekDays = Arrays.asList("周日", "周一", "周二", "周三", "周四", "周五", "周六");
        String queryData = queryToday().replace("var match_list = ", "");
        queryData = queryData.substring(0, queryData.lastIndexOf(";"));
        Calendar calendar = Calendar.getInstance();
        JSONObject matchList = JSON.parseObject(queryData);
        for (String key : matchList.keySet()) {

            JSONObject match = (JSONObject) matchList.get(key);
            MatchBean matchBean = new MatchBean();
            matchBean.setMatchNum(match.getString("match_num"));
            matchBean.setLiveDate(match.getString("date_cn"));
            matchBean.setGroupName(match.getString("l_cn"));
            matchBean.setStatus(match.getString("status"));
            matchBean.setHostTeam(match.getString("h_cn"));
            matchBean.setGuestTeam(match.getString("a_cn"));
            matchBean.setOdds(new Float[]{match.getFloat("h"), match.getFloat("d"), match.getFloat("a")});
            if (matchBean.getStatus().equals("Played")) {
                matchBean.setHostNum(match.getInteger("fs_h"));
                matchBean.setGuestNum(match.getInteger("fs_a"));
                matchBean.setStatus("1");
            }else {
                matchBean.setHostNum(0);
                matchBean.setGuestNum(0);
                matchBean.setStatus("0");
            }

            Date liveDate = DateUtil.getDateFormat().parse(matchBean.getLiveDate());
            calendar.setTime(liveDate);
            int w = calendar.get(Calendar.DAY_OF_WEEK) - 1;
            //如果赛事编号的星期与实际日期的星期不一致，修改日期
            if (!matchBean.getMatchNum().contains(weekDays.get(w))){
                int c = weekDays.indexOf(matchBean.getMatchNum().substring(0,2));
                int offset =  c - w;
                if (c == 6 && w == 0){
                    offset = -1;
                }
                if (c == 0 && w == 6){
                    offset = 1;
                }
                if (c == 6 && w == 1){
                    offset = -2;
                }
                if (c == 1 && w == 6){
                    offset = 2;
                }
                if (c == 5 && w == 0){
                    offset = -2;
                }
                if (c == 0 && w == 5){
                    offset = 2;
                }
                calendar.add(Calendar.DAY_OF_WEEK,offset);
            }
            liveDate = calendar.getTime();
            matchBean.setLiveDate(DateUtil.getDateFormat().format(liveDate));

            LiveDataRepository.insert(matchBean);
        }
    }

    public static void main(String[] args) {
        try {
            getMatchData();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
}
