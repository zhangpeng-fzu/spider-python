package com.peng.bean;

import java.util.Date;

public class MatchNumBean {
    private Date liveDate;
    private String matchNum;
    private int zero;
    private int one_three;
    private int two_four;
    private int five_;


    public MatchNumBean(){
        this.zero = 0;
        this.one_three = 0;
        this.two_four = 0;
        this.five_ = 0;

    }

    public Date getLiveDate() {
        return liveDate;
    }

    public void setLiveDate(Date liveDate) {
        this.liveDate = liveDate;
    }

    public String getMatchNum() {
        return matchNum;
    }

    public void setMatchNum(String matchNum) {
        this.matchNum = matchNum;
    }

    public int getZero() {
        return zero;
    }

    public void setZero(int zero) {
        this.zero = zero;
    }

    public int getOne_three() {
        return one_three;
    }

    public void setOne_three(int one_three) {
        this.one_three = one_three;
    }

    public int getTwo_four() {
        return two_four;
    }

    public void setTwo_four(int two_four) {
        this.two_four = two_four;
    }

    public int getFive_() {
        return five_;
    }

    public void setFive_(int five_) {
        this.five_ = five_;
    }
}
