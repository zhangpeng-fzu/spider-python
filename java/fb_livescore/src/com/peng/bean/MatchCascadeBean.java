package com.peng.bean;

import java.util.Date;

public class MatchCascadeBean {
    private Date liveDate;
    private String matchCascadeNum;
    private int ss;
    private int sp;
    private int sf;
    private int ps;
    private int pp;
    private int pf;
    private int fs;
    private int fp;
    private int ff;

    public MatchCascadeBean(){
        this.ss = 0;
        this.sp = 0;
        this.sf = 0;
        this.ps = 0;
        this.pp = 0;
        this.pf = 0;
        this.fs = 0;
        this.fp = 0;
        this.ff = 0;
    }

    public Date getLiveDate() {
        return this.liveDate;
    }

    public void setLiveDate(Date liveDate) {
        this.liveDate = liveDate;
    }

    public String getMatchCascadeNum() {
        return this.matchCascadeNum;
    }

    public void setMatchCascadeNum(String matchCascadeNum) {
        this.matchCascadeNum = matchCascadeNum;
    }

    public int getSs() {
        return this.ss;
    }

    public void setSs(int ss) {
        this.ss = ss;
    }

    public int getSp() {
        return this.sp;
    }

    public void setSp(int sp) {
        this.sp = sp;
    }

    public int getSf() {
        return this.sf;
    }

    public void setSf(int sf) {
        this.sf = sf;
    }

    public int getPs() {
        return this.ps;
    }

    public void setPs(int ps) {
        this.ps = ps;
    }

    public int getPp() {
        return this.pp;
    }

    public void setPp(int pp) {
        this.pp = pp;
    }

    public int getPf() {
        return this.pf;
    }

    public void setPf(int pf) {
        this.pf = pf;
    }

    public int getFs() {
        return this.fs;
    }

    public void setFs(int fs) {
        this.fs = fs;
    }

    public int getFp() {
        return this.fp;
    }

    public void setFp(int fp) {
        this.fp = fp;
    }

    public int getFf() {
        return this.ff;
    }

    public void setFf(int ff) {
        this.ff = ff;
    }
}
