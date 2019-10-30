package com.peng.service;

import com.peng.bean.MatchBean;
import com.peng.bean.MatchNumBean;
import com.peng.repository.LiveDataRepository;
import com.peng.repository.MatchNumRepository;
import com.peng.util.DateUtil;

import java.text.ParseException;
import java.util.Calendar;
import java.util.Date;
import java.util.Map;

public class CalMatchNumMiss {


    public static void calculate() throws ParseException {
        Date lastDate = MatchNumRepository.clearLastThreeDayData();
        if (lastDate == null) {
            lastDate = DateUtil.getDateFormat().parse("2019-01-01");
        }

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(lastDate);
        calendar.add(Calendar.DATE, 0);
        lastDate = calendar.getTime();
        while (lastDate.before(new Date())) {
            //获取当天所有的赛事
            Map<String,MatchBean> matchBeans = LiveDataRepository.getMatchList(lastDate);
            //如果没有一场赛事，可能没有抓取数据
            if (matchBeans.size() == 0){
                break;
            }
            for (int i = 1; i <= 300; i++) {

                //获取昨天的记录
                calendar.add(Calendar.DATE, -1);
                lastDate = calendar.getTime();
                MatchNumBean matchNumBean = MatchNumRepository.findByLiveDateAndNum(lastDate, formatMatchNum(i));

                calendar.add(Calendar.DATE, 1);
                lastDate = calendar.getTime();

                matchNumBean.setLiveDate(lastDate);
                matchNumBean.setMatchNum(formatMatchNum(i));

                MatchBean matchBean = matchBeans.get(formatMatchNum(i));
                if (matchBean != null && matchBean.getStatus().equals("1")){
                    //如果有比赛，未中加1，中改0
                    matchNumBean.setZero(matchNumBean.getZero() + 1);
                    matchNumBean.setOne_three(matchNumBean.getOne_three() + 1);
                    matchNumBean.setTwo_four(matchNumBean.getTwo_four() + 1);
                    matchNumBean.setFive_(matchNumBean.getFive_() + 1);
                    if (matchBean.getNum() == 0) {
                        matchNumBean.setZero(0);
                    } else if (matchBean.getNum() == 1 || matchBean.getNum() == 3) {
                        matchNumBean.setOne_three(0);
                    } else if (matchBean.getNum() == 2 || matchBean.getNum() == 4) {
                        matchNumBean.setTwo_four(0);
                    } else {
                        matchNumBean.setFive_(0);
                    }
                }else {
                    //该场次没有比赛，使用昨日的数据
                }
                MatchNumRepository.insert(matchNumBean);
            }
            calendar.add(Calendar.DATE, 1);
            lastDate = calendar.getTime();
        }
        System.out.println("计算赛事场次数据已完成");
    }


    static String formatMatchNum(int i){
        if (i < 10){
            return "00"+i;
        }
        if (i< 100){
            return "0" + i;
        }
        return String.valueOf(i);
    }

    public static void main(String[] args) {
        try {
            calculate();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
