package com.peng.service;

import com.peng.bean.MatchBean;
import com.peng.repository.LiveDataRepository;
import com.peng.util.DateUtil;
import com.peng.util.HttpClientUtil;

import java.text.ParseException;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LoadHistoryData {

    public static void loadHistoryData() {
        List<String> weekDays = Arrays.asList("周日", "周一", "周二", "周三", "周四", "周五", "周六");
        String lastDate = LiveDataRepository.clearLastThreeDayData();
        Calendar calendar = Calendar.getInstance();
        calendar.add(Calendar.DATE, -1);
        Date yesterday = calendar.getTime();
        boolean hasMore = true;
        int page = 1;

        String response;
        while (hasMore) {
            response = HttpClientUtil.doGet(String.format("https://info.sporttery.cn/football/match_result.php?page=%s&search_league=0&start_date=%s&end_date=%s&dan=0",
                    page, lastDate, DateUtil.getDateFormat().format(yesterday)), "gb2312");
            String matchListData = response.substring(response.indexOf("<div class=\"match_list\">"), response.indexOf("<div class=\"m-notice\">"));
            String[] matchData = matchListData.split("</tr>");
            if (matchData.length < 34) {
                hasMore = false;
            }
            for (String tr : matchData) {
                String[] tds = tr.split("\r\n|>VS<");
                StringBuilder tdData = new StringBuilder();
                for (String td : tds) {
                    if (td.contains("class=\"u-detal\"")) {
                        break;
                    }
                    if (td.contains("<td") || td.contains("</td>")) {
                        Pattern pattern = Pattern.compile(">.*?</");
                        Matcher matcher = pattern.matcher(td);
                        if (matcher.find()) {
                            String text = matcher.group(0).replace(">", " ").replace("</", "");
                            if (text.contains(" ")) {
                                text = text.substring(text.lastIndexOf(" ")).replaceAll("title=\"|class=\"blue\"|font-size:13px;\"|class=", "").split("\"")[0];
                                if (text.length() == 0) {
                                    continue;
                                }
                                if (text.trim().equals("--")) {
                                    text = "0";
                                }
                            }
                            tdData.append(text.trim()).append(",");
                        }
                    }
                }
                if (tdData.length() < 10) {
                    continue;
                }

                String[] tdDataArr = tdData.toString().split(",");
                MatchBean matchBean = new MatchBean();
                matchBean.setMatchNum(tdDataArr[1]);
                try {
                    Date liveDate = DateUtil.getDateFormat().parse(tdDataArr[0]);
                    calendar.setTime(liveDate);
                    int w = calendar.get(Calendar.DAY_OF_WEEK) - 1;
                    //如果赛事编号的星期与实际日期的星期不一致，修改日期
                    if (!matchBean.getMatchNum().contains(weekDays.get(w))) {
                        int c = weekDays.indexOf(matchBean.getMatchNum().substring(0, 2));
                        int offset = c - w;
                        if (c == 6 && w == 0) {
                            offset = -1;
                        }
                        if (c == 0 && w == 6) {
                            offset = 1;
                        }
                        if (c == 6 && w == 1) {
                            offset = -2;
                        }
                        if (c == 1 && w == 6) {
                            offset = 2;
                        }
                        if (c == 5 && w == 0) {
                            offset = -2;
                        }
                        if (c == 0 && w == 5) {
                            offset = 2;
                        }
                        calendar.add(Calendar.DAY_OF_WEEK, offset);
                    }
                    liveDate = calendar.getTime();
                    matchBean.setLiveDate(DateUtil.getDateFormat().format(liveDate));

                } catch (ParseException e) {
                    e.printStackTrace();
                    matchBean.setGroupName(tdDataArr[0]);
                }
                matchBean.setGroupName(tdDataArr[2]);
                matchBean.setHostTeam(tdDataArr[3]);
                matchBean.setGuestTeam(tdDataArr[4]);


                Float[] odds = new Float[]{Float.valueOf(tdDataArr[7]), Float.valueOf(tdDataArr[8]), Float.valueOf(tdDataArr[9])};
                matchBean.setOdds(odds);
                String status = tdDataArr[10].equals("已完成") ? "1" : "0";
                if (tdDataArr[10].equals("取消")) {
                    status = "2";
                    matchBean.setHostNum(0);
                    matchBean.setGuestNum(0);
                } else {
                    matchBean.setHostNum(Integer.parseInt(tdDataArr[6].split(":")[0]));
                    matchBean.setGuestNum(Integer.parseInt(tdDataArr[6].split(":")[1]));
                }

                matchBean.setStatus(status);
                LiveDataRepository.insert(matchBean);

            }

            page++;
            System.out.println("正在抓取第" + page + "页");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }


    }
}
