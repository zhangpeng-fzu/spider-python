package com.peng.service;

import com.peng.bean.MatchBean;
import com.peng.bean.MatchCascadeBean;
import com.peng.repository.LiveDataRepository;
import com.peng.repository.MacthCascadeRepository;
import com.peng.util.DateUtil;

import java.text.ParseException;
import java.util.Calendar;
import java.util.Date;
import java.util.Map;

public class CalMatchCascadeMiss {

    public static void calculate() throws ParseException {
        Date lastDate = MacthCascadeRepository.clearLastThreeDayData();
        if (lastDate == null) {
            lastDate = DateUtil.getDateFormat().parse("2019-01-01");
        }

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(lastDate);
        calendar.add(Calendar.DATE, 0);
        lastDate = calendar.getTime();
        while (lastDate.before(new Date())) {
            //获取当天所有的赛事
            Map<String, MatchBean> matchBeans = LiveDataRepository.getMatchList(lastDate);

            //如果没有一场赛事，可能没有抓取数据
            if (matchBeans.size() == 0){
                break;
            }


            for (int i = 2; i <= 300; i++) {
                //获取昨天的记录
                calendar.add(Calendar.DATE, -1);
                lastDate = calendar.getTime();
                MatchCascadeBean matchCascadeBean = MacthCascadeRepository.findByLiveDateAndCascadeNum(lastDate, formatMatchNum(i - 1) + "串" + formatMatchNum(i));
                calendar.add(Calendar.DATE, 1);
                lastDate = calendar.getTime();
                matchCascadeBean.setLiveDate(lastDate);
                matchCascadeBean.setMatchCascadeNum(formatMatchNum(i - 1) + "串" + formatMatchNum(i));

                if (matchBeans.containsKey(formatMatchNum(i - 1)) && matchBeans.containsKey(formatMatchNum(i))
                        && matchBeans.get(formatMatchNum(i - 1)).getStatus().equals("1") && matchBeans.get(formatMatchNum(i)).getStatus().equals("1")) {
                    matchCascadeBean.setSs(matchCascadeBean.getSs() + 1);
                    matchCascadeBean.setSp(matchCascadeBean.getSp() + 1);
                    matchCascadeBean.setSf(matchCascadeBean.getSf() + 1);
                    matchCascadeBean.setPs(matchCascadeBean.getPs() + 1);
                    matchCascadeBean.setPp(matchCascadeBean.getPp() + 1);
                    matchCascadeBean.setPf(matchCascadeBean.getPf() + 1);
                    matchCascadeBean.setFs(matchCascadeBean.getFs() + 1);
                    matchCascadeBean.setFp(matchCascadeBean.getFp() + 1);
                    matchCascadeBean.setFf(matchCascadeBean.getFf() + 1);

                    MatchBean pre = matchBeans.get(formatMatchNum(i - 1));
                    MatchBean cur = matchBeans.get(formatMatchNum(i));

                    if (pre.getHostNum() - pre.getGuestNum() > 0 && cur.getHostNum() - cur.getGuestNum() > 0) {
                        matchCascadeBean.setSs(0);
                    } else if (pre.getHostNum() - pre.getGuestNum() > 0 && cur.getHostNum() - cur.getGuestNum() == 0) {
                        matchCascadeBean.setSp(0);
                    } else if (pre.getHostNum() - pre.getGuestNum() > 0 && cur.getHostNum() - cur.getGuestNum() < 0) {
                        matchCascadeBean.setSf(0);
                    } else if (pre.getHostNum() - pre.getGuestNum() == 0 && cur.getHostNum() - cur.getGuestNum() > 0) {
                        matchCascadeBean.setPs(0);
                    } else if (pre.getHostNum() - pre.getGuestNum() == 0 && cur.getHostNum() - cur.getGuestNum() == 0) {
                        matchCascadeBean.setPp(0);
                    } else if (pre.getHostNum() - pre.getGuestNum() == 0 && cur.getHostNum() - cur.getGuestNum() < 0) {
                        matchCascadeBean.setPf(0);
                    } else if (pre.getHostNum() - pre.getGuestNum() < 0 && cur.getHostNum() - cur.getGuestNum() > 0) {
                        matchCascadeBean.setFs(0);
                    } else if (pre.getHostNum() - pre.getGuestNum() < 0 && cur.getHostNum() - cur.getGuestNum() == 0) {
                        matchCascadeBean.setFp(0);
                    } else {
                        matchCascadeBean.setFf(0);
                    }
                }
                MacthCascadeRepository.insert(matchCascadeBean);
            }
            calendar.add(Calendar.DATE, 1);
            lastDate = calendar.getTime();
        }
        System.out.println("计算串关场次数据已完成");
    }

    public static void main(String[] args) {
        try {
            calculate();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static String formatMatchNum(int i) {
        if (i < 10) {
            return "00" + i;
        }
        if (i < 100) {
            return "0" + i;
        }
        return String.valueOf(i);
    }

}
